"""Executa o complemento estadual sobre a publicação nacional congelada."""
import argparse,hashlib,json,os,shutil,subprocess,time,urllib.request,zipfile
from pathlib import Path
from integridade import digest
from lote import UFS,download
from relatorios_nacionais.analisar import analyze
from relatorios_nacionais.relatorio import generate
REFERENCE='auditoria-v3-41263277696'

def obtain(url,path):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AuditorEleitoralIndependente/3.0'}),timeout=60) as response,path.with_suffix('.part').open('wb') as f:shutil.copyfileobj(response,f)
 path.with_suffix('.part').replace(path)
def reference(uf,work,metadata):
 asset=next(a for a in metadata['assets'] if a['name']==f'{uf}-tentativa1.zip');sha=asset.get('digest','');assert sha.startswith('sha256:'),'Publicação sem hash'
 path=work/'publicado.zip'
 if not path.exists():obtain(asset['browser_download_url'],path)
 assert digest(path)==sha.split(':',1)[1],'Hash GitHub divergente'
 root=work/'publicado';root.mkdir(exist_ok=True)
 with zipfile.ZipFile(path) as z:
  for line in z.read('SHA256SUMS.txt').decode().splitlines():
   expected,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==expected,name
  for info in z.infolist():
   dest=(root/info.filename).resolve();assert dest.is_relative_to(root.resolve())
  z.extractall(root)
 return root,asset

def execute(uf,work,downloads,metadata):
 work=Path(work)/uf;work.mkdir(parents=True,exist_ok=True);out=work/'entrega';out.mkdir(exist_ok=True);status=dict(uf=uf,status='iniciado',commit=os.getenv('GITHUB_SHA','local'),referencia=REFERENCE)
 try:
  root,asset=reference(uf,work,metadata);package=download(uf,Path(downloads),workers=4)
  summary=analyze(uf,package,root,out)
  pdfmeta=generate(uf,out);summary['pdf']=pdfmeta
  previews=out/'previas';previews.mkdir(exist_ok=True)
  subprocess.run(['pdftoppm','-f','1','-l','1','-scale-to','1000','-png',str(out/f'Relatorio_{uf}.pdf'),str(previews/'capa')],check=True)
  summary['publicacao_referencia']=asset;summary['commit_complemento']=status['commit'];summary['sha256_scripts']={str(p):digest(p) for p in sorted(Path('relatorios_nacionais').glob('*.py'))}
  (out/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));shutil.copy(out/'resumo.json',out/f'{uf}_resumo.json')
  package_path=out/f'{uf}_Dados_e_Trechos.zip';checks=[]
  with zipfile.ZipFile(package_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
   paths=sorted(out.glob('*.csv'))+sorted(out.glob('*.csv.gz'))+sorted((out/'trechos').glob('*.txt'))+[out/'resumo.json',out/f'Relatorio_{uf}.md']
   for p in paths:
    arc=str(p.relative_to(out));z.write(p,arc);checks.append(digest(p)+'  '+arc)
   z.writestr('SHA256SUMS.txt','\n'.join(checks)+'\n')
  status.update(status='concluido',logs=summary['logs'],pdf=pdfmeta,sha256_arquivos={p.name:digest(p) for p in [package_path,out/f'{uf}_Logs_Integrais.zip',out/f'Relatorio_{uf}.pdf',out/f'{uf}_resumo.json']})
 except Exception as error:
  status.update(status='falhou',erro=f'{type(error).__name__}: {error}');raise
 finally:
  status['atualizacao_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(out/f'{uf}_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2));print(json.dumps(status,ensure_ascii=False),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('uf',choices=UFS);p.add_argument('--work',default='trabalho_relatorios');p.add_argument('--downloads',default='downloads');p.add_argument('--metadados',default='fonte_relatorios.json');a=p.parse_args();execute(a.uf,a.work,a.downloads,json.loads(Path(a.metadados).read_text()))
