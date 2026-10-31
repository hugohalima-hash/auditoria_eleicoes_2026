#!/usr/bin/env python3
"""Auditor Eleitoral Independente 2026 — versão 2, análise de logs públicos."""
import argparse
import threading
from pathlib import Path
from lote import UFS, main

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--arquivos',nargs='*',type=Path,default=[])
    ap.add_argument('--ufs',nargs='*',choices=UFS)
    ap.add_argument('--brasil',action='store_true')
    ap.add_argument('--saida',type=Path,default=Path('resultados_v2'))
    ap.add_argument('--data',default='25/10/2026')
    ap.add_argument('--pasta-download',type=Path,default=Path('downloads'))
    ap.add_argument('--conexoes',type=int,default=4,choices=range(1,17))
    ap.add_argument('--estados-simultaneos',type=int,default=1,choices=range(1,5))
    ap.add_argument('--processos',type=int,default=1,choices=range(1,5),help='processos de análise por UF; padrão 1 para limitar memória')
    ap.add_argument('--limite-memoria-mib',type=int,default=1536,choices=[0,1024,1536,2048])
    ap.add_argument('--apagar-pacotes',action='store_true',help='apaga ZIPs baixados após processamento sem erros; preserva hashes e relatórios')
    ap.add_argument('--eventos',action='store_true',help='exporta habilitações dos arquivos locais, sem identificação pessoal')
    args=ap.parse_args()
    threading.stack_size(1024*1024)
    if args.limite_memoria_mib and args.limite_memoria_mib+args.estados_simultaneos*args.processos*768>6656:
        ap.error('a soma dos limites principal e auxiliares excede o orçamento de 6,5 GiB; reduza estados ou processos')
    if args.limite_memoria_mib:
        try:
            import resource
            cap=args.limite_memoria_mib*1024*1024
            resource.setrlimit(resource.RLIMIT_AS,(cap,cap))
        except ImportError:
            pass
    raise SystemExit(main(args))
