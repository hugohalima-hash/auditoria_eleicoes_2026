"""Reconstitui o corpus público a partir do ZIP oficial, verificando cada SHA-256."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pacote',type=Path)
    parser.add_argument('--manifesto',type=Path,default=Path('validacao/resultado_corpus.json'))
    parser.add_argument('--saida',type=Path,default=Path('validacao/amostras'))
    args=parser.parse_args()
    files=json.loads(args.manifesto.read_text())['arquivos']
    args.saida.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.pacote) as archive:
        for item in files:
            name=item['arquivo']
            if Path(name).name!=name:raise ValueError('nome de arquivo inválido')
            raw=archive.read(name)
            if hashlib.sha256(raw).hexdigest()!=item['sha256']:
                raise ValueError('hash divergente: '+name)
            (args.saida/name).write_bytes(raw)
    print(f'{len(files)} logs reconstituídos e verificados.')
