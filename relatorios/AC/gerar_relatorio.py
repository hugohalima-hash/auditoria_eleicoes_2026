"""Gera a versão atual do relatório, após executar ritmo/analisar_ritmo.py."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).parent/'ritmo/gerar_relatorio.py'),run_name='__main__')
