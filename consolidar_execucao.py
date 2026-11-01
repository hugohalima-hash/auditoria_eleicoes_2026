"""Confere e combina os pacotes estaduais de uma execução GitHub Actions."""
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from lote import UFS
from motor import ENGINE_SHA256
from integridade import verified

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pasta',type=Path);a=p.parse_args()
    selected={}
    for path in a.pasta.glob('*-tentativa*.zip'):
        uf,attempt=path.stem.split('-tentativa')
        if uf in UFS and (uf not in selected or int(attempt)>selected[uf][0]):selected[uf]=(int(attempt),path)
    if set(selected)!=set(UFS):raise RuntimeError('Faltam pacotes: '+str(set(UFS)-set(selected)))
    dest=Path('estados_consolidados');dest.mkdir(exist_ok=True)
    for uf,(_,path) in sorted(selected.items()):
        with zipfile.ZipFile(path) as z:
            sums={}
            for line in z.read('SHA256SUMS.txt').decode().splitlines():
                digest,name=line.split('  ',1);sums[name]=digest
            for info in z.infolist():
                if info.is_dir() or info.filename=='SHA256SUMS.txt':continue
                target=dest/info.filename
                if not target.resolve().is_relative_to(dest.resolve()):raise ValueError('caminho inválido')
                raw=z.read(info)
                if hashlib.sha256(raw).hexdigest()!=sums.get(info.filename):raise ValueError('hash divergente')
                # Triagens estaduais usam os mesmos nomes; a nacional é
                # recalculada e essas cópias não são combinadas por sobrescrita.
                if info.filename.startswith('triagem/'):continue
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        status=json.loads((dest/'conferencias'/uf/'execucao.json').read_text())
        if status.get('status')!='processado_e_conferido':raise RuntimeError('UF incompleta: '+uf)
        if not verified(dest/'resultados'/uf,ENGINE_SHA256):raise RuntimeError('Manifesto inválido: '+uf)
    subprocess.run([sys.executable,'consolidar.py','--resultados',str(dest/'resultados'),'--saida','entrega_nacional'],check=True)
    subprocess.run([sys.executable,'anomalias.py','--resultados',str(dest/'resultados'),'--saida','triagem_nacional'],check=True)
    with zipfile.ZipFile('entrega_nacional/triagem_nacional.zip','w',zipfile.ZIP_DEFLATED) as z:
        for folder in [Path('triagem_nacional'),dest/'conferencias',dest/'originais']:
            for path in sorted(folder.rglob('*')):
                if path.is_file():z.write(path,path.as_posix())
