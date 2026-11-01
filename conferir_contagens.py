"""Conferência de eventos com leitor independente; não valida classes semânticas."""
import argparse
import csv
import hashlib
import json
import zipfile
from pathlib import Path
from validar_corpus import direct_count
from integridade import digest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pacote',type=Path)
    parser.add_argument('--referencia',type=Path,default=Path('validacao/contagens_independentes.csv'))
    parser.add_argument('--resultados',type=Path)
    parser.add_argument('--resumo',type=Path,default=Path('validacao/conferencia_contagens.json'))
    args=parser.parse_args()
    context_path=args.referencia.with_suffix('.origem.json')
    source={'sha256_pacote':digest(args.pacote),
            'sha256_leitor_independente':digest(Path(__file__).with_name('validar_corpus.py'))}
    try:
        previous=json.loads(context_path.read_text())
    except (OSError,ValueError):
        previous={}
    reusable=(args.referencia.exists() and all(previous.get(k)==v for k,v in source.items())
              and previous.get('sha256_referencia')==digest(args.referencia))
    if not reusable:
        args.referencia.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(args.pacote) as archive,args.referencia.open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['arquivo','sha256','aplicavel','habilitacoes','votos_computados'])
            writer.writeheader()
            for name in archive.namelist():
                if not name.lower().endswith(('.jez','.logjez')):continue
                raw=archive.read(name);ref=direct_count(raw)
                writer.writerow({'arquivo':name,'sha256':hashlib.sha256(raw).hexdigest(),
                    'aplicavel':ref is not None,'habilitacoes':ref['habilitacoes'] if ref is not None else '',
                    'votos_computados':ref['votos_computados'] if ref is not None else ''})
        context_path.write_text(json.dumps({**source,'sha256_referencia':digest(args.referencia)},indent=2))
    rows=list(csv.DictReader(args.referencia.open()))
    summary={'logs_na_referencia':len(rows),'logs_aplicaveis':sum(r['aplicavel']=='True' for r in rows),
        **source,
        'sha256_referencia':hashlib.sha256(args.referencia.read_bytes()).hexdigest(),
        'comparacao_executada':False,'divergencias':[],'acuracia_semantica_certificada':None,
        'limite':'A contagem é independente do leitor do motor e compara eventos literais apenas em logs com um único bloco distinto; não certifica classificação de biometria nem vínculo individual.'}
    if args.resultados:
        output={r['arquivo']:r for r in csv.DictReader(args.resultados.open(encoding='utf-8-sig'))}
        summary['comparacao_executada']=True
        if set(output)!={r['arquivo'] for r in rows}:
            summary['divergencias'].append({'erro':'inventarios_diferentes'})
        for ref in rows:
            if ref['aplicavel']!='True':continue
            got=output.get(ref['arquivo'])
            if got is None:continue
            for key in ['sha256','habilitacoes','votos_computados']:
                if ref[key]!=got[key]:summary['divergencias'].append({'arquivo':ref['arquivo'],'campo':key,'referencia':ref[key],'motor':got[key]})
    args.resumo.write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    raise SystemExit(bool(summary['divergencias']))
