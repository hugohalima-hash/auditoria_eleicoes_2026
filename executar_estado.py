"""Executa uma UF, confere contagens e empacota resultados rastreáveis."""
import argparse
import csv
import hashlib
import json
import os
import random
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from lote import UFS, URL
from motor import ENGINE_SHA256
from integridade import verified


def command(*args):
    subprocess.run([sys.executable,*map(str,args)],check=True)


def execute(uf):
    root=Path('resultados')/uf
    diagnostics=Path('conferencias')/uf
    diagnostics.mkdir(parents=True,exist_ok=True)
    status={'uf':uf,'status':'iniciado','sha256_motor':ENGINE_SHA256,
        'commit_fonte':os.getenv('GITHUB_SHA','execucao_local'),
        'url_pacote':URL.format(uf=uf),'acuracia_certificada':None}
    try:
        command('auditar.py','--ufs',uf,'--saida','resultados','--pasta-download','downloads',
                '--estados-simultaneos','1','--conexoes','4','--processos','1','--limite-memoria-mib','2048')
        if not verified(root,ENGINE_SHA256):raise RuntimeError('manifesto inválido')
        summary=json.loads((root/'resumo.json').read_text())
        if summary['erros'] or summary['arquivos_processados']!=summary['logs_no_pacote']:
            raise RuntimeError('processamento incompleto')
        package=Path('downloads')/URL.format(uf=uf).rsplit('/',1)[-1]
        command('conferir_contagens.py',package,'--referencia',diagnostics/'contagens.csv',
                '--resumo',diagnostics/'conferencia.json','--resultados',root/'urnas.csv')
        command('anomalias.py','--resultados','resultados','--saida','triagem')
        status['status']='processado_e_conferido'
        status['arquivos_processados']=summary['arquivos_processados']
        status['ressalva']='Triagem exploratória; conferência de contagens não certifica acurácia semântica de 99,9%.'
        # Preserva os originais de todos os casos em quarentena e controles
        # determinísticos. O pacote bruto completo segue na fonte oficial.
        quarantine=list(csv.DictReader(open('triagem/quarentena.csv',encoding='utf-8-sig')))
        selected={r['arquivo'] for r in quarantine if r['uf']==uf}
        with zipfile.ZipFile(package) as archive:
            logs=sorted(n for n in archive.namelist() if n.lower().endswith(('.jez','.logjez')))
            selected.update(random.Random(20261031).sample(logs,min(100,len(logs))))
            original=Path('originais')/uf;original.mkdir(parents=True,exist_ok=True)
            refs=[]
            for name in sorted(selected):
                if Path(name).name!=name:raise ValueError('nome de log inesperado')
                raw=archive.read(name);(original/name).write_bytes(raw)
                refs.append({'arquivo':name,'sha256':hashlib.sha256(raw).hexdigest(),
                             'motivo':'quarentena' if any(r['arquivo']==name and r['uf']==uf for r in quarantine) else 'controle'})
            (original/'manifesto_amostras.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2))
    except Exception as error:
        status['status']='falhou';status['erro']=f'{type(error).__name__}: {error}'
        raise
    finally:
        status['atualizacao_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        (diagnostics/'execucao.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
        output=Path('pacotes');output.mkdir(exist_ok=True)
        filename=output/f"{uf}-tentativa{os.getenv('GITHUB_RUN_ATTEMPT','1')}.zip"
        sums=[]
        with zipfile.ZipFile(filename,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
            for folder in [root,diagnostics,Path('triagem'),Path('originais')/uf]:
                if not folder.exists():continue
                for path in sorted(folder.rglob('*')):
                    if path.is_file() and path.suffix in ('.json','.csv','.jez','.logjez'):
                        archive.write(path,path.as_posix())
                        sums.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.as_posix())
            archive.writestr('SHA256SUMS.txt','\n'.join(sums)+'\n')
        print('PACOTE',filename,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('uf',choices=UFS)
    execute(p.parse_args().uf)
