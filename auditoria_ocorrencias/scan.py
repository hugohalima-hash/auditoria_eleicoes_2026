import argparse
import csv
import json
from itertools import groupby
from motor import read_logs
import re
import zipfile
from pathlib import Path

DATES = {"2": "25/10/2026"}
ALERT = "o eleitor identificado já votou"
VOTE = "o voto do eleitor foi computado"
WAIT = "aguardando digitação do identificador do eleitor"
SECTION = re.compile(r"o\d{5}[a-z]{2}(\d{5})(\d{4})(\d{4})-log\.jez$", re.I)


def redact(message):
    return re.sub(r"\b(?:\d[ .-]?){10,}\d\b", "[número omitido]", message)


def events(raw, date):
    result = []
    for line in raw.decode("latin-1").splitlines():
        fields = line.split("\t", 5)
        if len(fields) >= 5 and fields[0].startswith(date + " "):
            result.append((fields[0], fields[3], fields[4].strip()))
    return result


def occurrences(rows):
    previous = None
    pending = []
    for i, (_, module, message) in enumerate(rows):
        msg = message.casefold()
        if module != "VOTA":
            continue
        if msg == VOTE:
            previous = i
        elif msg == ALERT or re.search(r"\bimpedid[oa]\s+de\s+votar\b", msg):
            pending.append((previous, i))
        elif msg == WAIT:
            for start, hit in pending:
                yield start, hit, i
            pending.clear()
    for start, hit in pending:
        yield start, hit, None


def scan(source, out, uf, turn):
    count = logs = empty = 0
    errors = []
    categories = {"ja_votou": 0, "impedimento_explicito": 0}
    sections = set()
    out.mkdir(parents=True, exist_ok=True)
    details = out / f"{uf}-{turn}-ocorrencias.csv"
    report = out / f"{uf}-{turn}.md"
    with zipfile.ZipFile(source) as package, details.open("w", newline="", encoding="utf-8") as table, report.open("w", encoding="utf-8") as md:
        writer = csv.writer(table)
        writer.writerow(["uf", "turno", "municipio_tse", "zona", "secao", "horario", "mensagem", "voto_anterior", "aguarda_seguinte", "arquivo"])
        md.write(f"# {uf} · {turn}º turno\n\nOcorrências de ‘O eleitor identificado já votou’ e mensagens explícitas de impedimento de votar. Eleitor não encontrado não é classificado como impedido. Cada ocorrência corresponde a uma mensagem do log, sem deduplicação por pessoa.\n\n")
        for entry in package.infolist():
            match = SECTION.search(Path(entry.filename).name)
            if not match:
                continue
            logs += 1
            municipality, zone, section = match.groups()
            try:
                lines, _, _ = read_logs(package.read(entry))
                blocks = [
                    events("\n".join(line for _, _, line in block).encode("latin-1"), DATES[turn])
                    for _, block in groupby(lines, key=lambda item: item[0])
                ]
            except (ValueError, OSError, RuntimeError, zipfile.BadZipFile) as error:
                errors.append({"arquivo": entry.filename, "erro": str(error)})
                continue
            if not any(blocks):
                empty += 1
            for rows in blocks:
                for start, hit, end in occurrences(rows):
                    count += 1
                    category = "ja_votou" if rows[hit][2].casefold() == ALERT else "impedimento_explicito"
                    categories[category] += 1
                    sections.add((municipality, zone, section))
                    writer.writerow([uf, turn, municipality, zone, section, rows[hit][0], redact(rows[hit][2]), rows[start][0] if start is not None else "", rows[end][0] if end is not None else "", entry.filename])
                    md.write(f"## Ocorrência {count} · {category} · município TSE {municipality} · zona {zone} · seção {section}\n\nArquivo: {entry.filename}\n\n")
                    if start is None:
                        md.write("Sem voto anterior computado no trecho do turno.\n\n")
                    if end is None:
                        md.write("Sem novo pedido de identificação após o aviso no trecho do turno.\n\n")
                    md.write("~~~text\n")
                    for timestamp, module, message in rows[0 if start is None else start:len(rows) if end is None else end + 1]:
                        safe = redact(message)
                        md.write(f"{timestamp}\t{module}\t{safe}\n")
                    md.write("~~~\n\n")

        md.write(f"## Cobertura\n\n- Arquivos no pacote: {logs}\n- Arquivos com erro: {len(errors)}\n- Arquivos sem linhas da data: {empty}\n- Seções com ocorrências: {len(sections)}\n- Ocorrências: {count}\n- Já votou: {categories['ja_votou']}\n- Impedimento explícito: {categories['impedimento_explicito']}\n\nO log não identifica o eleitor consultado. Trechos podem se sobrepor quando há avisos sucessivos antes de outro voto computado.\n")
    status = {"uf": uf, "logs": logs, "sem_linhas_do_turno": empty, "erros": errors,
              "secoes_com_ocorrencias": len(sections), **categories,
              "status": "incompleto" if errors or logs == empty else "concluido"}
    (out / f"{uf}-status.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    print({k: v for k, v in status.items() if k != "erros"}, flush=True)
    if status["status"] != "concluido":
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("uf")
    parser.add_argument("turn", choices=DATES)
    args = parser.parse_args()
    scan(args.source, args.out, args.uf, args.turn)
