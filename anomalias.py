"""Triagem descritiva de exceções; nenhum alerta constitui prova de fraude."""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median, quantiles
from motor import write_csv


def upper(values):
    """Limite exploratório de Tukey (3 IQR), não teste de significância."""
    q1, _, q3 = quantiles(values, n=4, method='inclusive')
    return q3 + 3 * (q3 - q1)


def scan(root, out):
    out.mkdir(parents=True, exist_ok=True)
    alerts = []
    stats = []
    completed = []
    for folder in sorted(root.iterdir()):
        if not (folder / 'resumo.json').exists() or not (folder / 'urnas.csv').exists():
            continue
        summary = json.loads((folder / 'resumo.json').read_text())
        if summary.get('arquivos_processados') != summary.get('logs_no_pacote'):
            continue
        completed.append(folder.name)
        with (folder / 'urnas.csv').open(encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))
        groups = defaultdict(list)
        names = {}
        config = folder / 'config_oficial.json'
        if config.exists():
            for abr in json.loads(config.read_text()).get('abr', []):
                for mun in abr.get('mu', []):
                    names[str(mun['cd']).zfill(5)] = mun.get('nm', '')
        def emit(row, code, value, reference='', context=''):
            alerts.append(dict(uf=folder.name, municipio=row.get('municipio', ''),
                municipio_nome=names.get(row.get('municipio', ''), ''),
                zona=row.get('zona', ''), secao=row.get('secao', ''),
                arquivo=row.get('arquivo', ''), alerta=code, valor=value,
                referencia=reference, contexto=context))
        for row in rows:
            def n(key):
                return int(row.get(key, 0) or 0)
            total = n('habilitacoes')
            if total >= 100:
                groups[(row['municipio'], row['zona'])].append(row)
            for key in ('eventos_ajuste_relogio', 'linhas_dia_malformadas', 'indefinida', 'avisos'):
                if n(key):
                    emit(row, key, n(key), context='Alerta técnico; pode exigir revisão do analisador ou do registro.')
            if n('votos_computados') != n('votos_vinculados'):
                emit(row, 'votos_sem_vinculo_no_analisador', n('votos_computados') - n('votos_vinculados'))
            if total != n('votos_vinculados'):
                emit(row, 'habilitacoes_sem_voto_vinculado', total - n('votos_vinculados'),
                    context='Pode incluir cancelamentos ou registros incompletos; não é contagem de votos irregulares.')
            if n('blocos_log') > 1:
                emit(row, 'multiplos_blocos_log', n('blocos_log'),
                    context='Contexto de possível substituição; múltiplos blocos não provam troca de urna.')
            if n('maior_sequencia_mesario') >= 10:
                emit(row, 'sequencia_mesario_ge_10', n('maior_sequencia_mesario'),
                    context='Limiar de triagem fixo; não é probabilidade de fraude.')
        for key, peers in groups.items():
            if len(peers) < 20:
                continue
            metrics = {
                'proporcao_mesario': lambda r: int(r['com_evento_mesario']) / int(r['habilitacoes']),
                'volume_habilitacoes': lambda r: int(r['habilitacoes']),
            }
            for metric, measure in metrics.items():
                values = [measure(r) for r in peers]
                boundary = upper(values)
                baseline = median(values)
                stats.append(dict(uf=folder.name, municipio=key[0], zona=key[1],
                    metrica=metric, secoes=len(peers), mediana=baseline, limite_superior=boundary))
                for row in peers:
                    value = measure(row)
                    # Evita alertas por diferenças triviais quando IQR=0.
                    minimum = baseline + (0.10 if metric == 'proporcao_mesario' else 50)
                    if value > max(boundary, minimum):
                        emit(row, metric + '_acima_pares', round(value, 6), round(boundary, 6),
                            f'{len(peers)} seções com >=100 habilitações no mesmo município e zona; mediana={baseline:.6f}. Sem ajuste por eleitores aptos ou perfil biométrico.')
        with (folder / 'sequencias.csv').open(encoding='utf-8-sig') as f:
            for run in csv.DictReader(f):
                if run['grupo'] != 'mesario' or int(run['tamanho']) < 10:
                    continue
                count = int(run['tamanho'])
                duration = int(run['duracao_seg'])
                average = duration / (count - 1)
                if average < 30:
                    # Não chama de duração do voto: mede início a início.
                    from motor import section
                    emit({**section(run['arquivo']), 'arquivo': run['arquivo']},
                        'intervalo_medio_habilitacoes_menor_30s', round(average, 3), 30,
                        f"Série de {count}; {run['inicio']} a {run['fim']}; linhas {run['linha_inicio']}–{run['linha_fim']}. Não mede o tempo de cada voto.")
    fields = ['uf', 'municipio', 'municipio_nome', 'zona', 'secao', 'arquivo', 'alerta', 'valor', 'referencia', 'contexto']
    write_csv(out / 'alertas.csv', alerts, fields)
    write_csv(out / 'referencias_comparacao.csv', stats,
        ['uf', 'municipio', 'zona', 'metrica', 'secoes', 'mediana', 'limite_superior'])
    counts = Counter(r['alerta'] for r in alerts)
    result = {'ufs_incluidas': completed, 'alertas': len(alerts),
        'secoes_com_alerta': len({(r['uf'], r['arquivo']) for r in alerts}),
        'por_tipo': dict(counts), 'ressalva': 'Triagem exploratória, sem conclusão de fraude. Múltiplos alertas podem pertencer à mesma seção.'}
    (out / 'resumo.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resultados', type=Path, default=Path('resultados'))
    parser.add_argument('--saida', type=Path, default=Path('alertas'))
    args = parser.parse_args()
    print(json.dumps(scan(args.resultados, args.saida), ensure_ascii=False, indent=2))
