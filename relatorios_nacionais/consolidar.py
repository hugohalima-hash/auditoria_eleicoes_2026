"""Consolida apenas relatórios completos e verificados das 28 unidades."""
import csv,json,zipfile
from pathlib import Path
from integridade import digest
from lote import UFS
from relatorios_nacionais.nomes import NAMES

def consolidate(source,out):
 source=Path(source);out=Path(out);out.mkdir(parents=True,exist_ok=True);summaries=[];rows=[]
 for uf in UFS:
  status=json.loads((source/f'{uf}_status.json').read_text());assert status['status']=='concluido',(uf,status)
  p=source/f'{uf}_resumo.json';assert digest(p)==status['sha256_arquivos'][p.name],uf
  s=json.loads(p.read_text());assert s['uf']==uf and s['validacao']['contagens_reconciliadas']==s['logs'] and s['validacao']['maximos_conferidos']==2*s['logs'];summaries.append(s)
  row=dict(uf=uf,unidade=NAMES[uf],logs=s['logs'],votos_totais=sum(s['total_votos'].values()),votos_mesario=s['total_votos'].get('mesario',0),votos_ano=s['total_votos'].get('ano',0),concentracao_secoes=s['concentracao']['secoes_sinalizadas'],concentracao_votos=s['concentracao']['votos_conjunto'])
  for g in ['mesario','conjunto']:
   for k in ['ge2','ge3','maximo','triadas_ritmo']:row[g+'_'+k]=s['sequencias'][g].get(k,0)
  rows.append(row)
 assert len({s['motor'] for s in summaries})==1
 with (out/'Resumo_28_Unidades.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 total={k:sum(x[k] for x in rows) for k in ['logs','votos_totais','votos_mesario','votos_ano','concentracao_secoes','concentracao_votos','mesario_ge2','mesario_ge3','mesario_triadas_ritmo','conjunto_ge2','conjunto_ge3','conjunto_triadas_ritmo']}
 (out/'Resumo_Nacional_Ritmo.json').write_text(json.dumps(dict(status='28_unidades_concluidas',totais=total,unidades=summaries),ensure_ascii=False,indent=2))
 lines=['# Relatórios nacionais - liberações sucessivas','','28 unidades concluídas e conferidas: 26 estados, Distrito Federal e exterior. Os números são de triagem exploratória, não contagem de fraudes.','','| Unidade | Votos mesário | Votos ano | Séries mesário 3+ | Séries mesário rápidas | Séries conjunto rápidas | Seções concentradas |','|---|---:|---:|---:|---:|---:|---:|']
 for r in rows:lines.append('| '+' | '.join(map(str,[r['unidade'],r['votos_mesario'],r['votos_ano'],r['mesario_ge3'],r['mesario_triadas_ritmo'],r['conjunto_triadas_ritmo'],r['concentracao_secoes']]))+' |')
 lines += ['','O intervalo é medido entre liberações de eleitores consecutivos, dentro da mesma zona e seção. A duração de digitação do voto não é critério de suspeita. A referência rápida é o percentil 10 dos pares biométricos da própria seção, com mínimo de trinta pares e série de três ou mais liberações concluídas, em seção admissível. Comparação exploratória, sem ajuste por fila, horário, perfil ou múltiplas comparações.','','Cada unidade possui PDF e Markdown, dados integrais de pares e sequências, todos os trechos selecionados e logs originais de todas as seções selecionadas por ritmo ou concentração. Os exemplos no PDF não substituem os anexos integrais.']
 (out/'Indice_Relatorios_Nacionais.md').write_text('\n'.join(lines)+'\n');return total
if __name__=='__main__':
 import sys;print(consolidate(sys.argv[1],sys.argv[2]))
