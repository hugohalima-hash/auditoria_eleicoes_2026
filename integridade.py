"""Manifesto de integridade dos resultados; não autentica assinaturas do TSE."""
import hashlib
import json
from pathlib import Path

REQUIRED = ('resumo.json','urnas.csv','sequencias.csv','avisos.csv',
            'erros.csv','lacunas_cobertura.csv')


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def manifest(folder, engine):
    folder=Path(folder)
    files=list(REQUIRED)
    if (folder/'config_oficial.json').exists():
        files.append('config_oficial.json')
    return {'schema':1,'sha256_motor':engine,
            'arquivos':{name:digest(folder/name) for name in files}}


def verified(folder, engine):
    try:
        folder=Path(folder)
        m=json.loads((folder/'manifesto.json').read_text())
        if m.get('schema')!=1 or m.get('sha256_motor')!=engine:
            return False
        hashes=m.get('arquivos',{})
        if not set(REQUIRED).issubset(hashes):
            return False
        # Do not allow manifest paths to escape the result directory.
        if any(Path(name).name != name for name in hashes):
            return False
        return all(digest(folder/name)==value for name,value in hashes.items())
    except (OSError,ValueError,TypeError,AttributeError):
        return False
