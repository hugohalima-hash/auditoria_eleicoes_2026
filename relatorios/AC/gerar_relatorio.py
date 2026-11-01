"""Gera a apresentação vigente do relatório do Acre."""
from pathlib import Path
from runpy import run_path

if __name__ == '__main__':
    run_path(str(Path(__file__).parent / 'revisao' / 'gerar_relatorio_revisado.py'), run_name='__main__')
