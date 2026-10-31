"""Consolida apenas UFs efetivamente processadas, sem imputar dados ausentes."""
import argparse
import csv
import hashlib
import json
import time
import zipfile
from pathlib import Path
from lote import UFS, atomic_json
from motor import VERSION, write_csv, section

def number(n):
    return f'{n:,}'.replace(',','.')

def consolidate(root,destination):
    destination.mkdir(parents=True,exist_ok=True)
    results=[];rank=[];distribution=[]
    for uf in UFS:
        p=root/uf/'resumo.json'
        if not p.exists():continue
        result=json.loads(p.read_text())
        if result.get('versao_motor')!=VERSION:continue
        results.append(result)
        names={}
        config=root/uf/'config_oficial.json'
        if config.exists():
            for abr in json.loads(config.read_text()).get('abr',[]):
                for mun in abr.get('mu',[]):
                    names[str(mun['cd']).zfill(5)]=mun.get('nm','')
        local_runs=[]
        with (root/uf/'sequencias.csv').open(encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                local_runs.append(row)
                if row.get('grupo')=='mesario':
                    ids=section(row['arquivo'])
                    rank.append({'uf':uf,'municipio':ids.get('municipio',''),
                        'municipio_nome':names.get(ids.get('municipio',''),''),
                        'zona':ids.get('zona',''),'secao':ids.get('secao',''),**row})
        for group in ['mesario','sem_biometria']:
            selected=[r for r in local_runs if r['grupo']==group]
            dist={'uf':uf,'grupo':group}
            for threshold in [2,3,5,10,20]:
                matching=[r for r in selected if int(r['tamanho'])>=threshold]
                dist['sequencias_ge_'+str(threshold)]=len(matching)
                dist['secoes_ge_'+str(threshold)]=len({r['arquivo'] for r in matching})
            distribution.append(dist)
    pending=sorted(set(UFS)-{r['uf'] for r in results})
    summary={'versao_motor':VERSION,'atualizacao_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        'ufs_processadas':[r['uf'] for r in results],'ufs_pendentes':pending,
        'status_execucao':'todas_ufs_processadas' if not pending else 'parcial',
        'ressalva':'Processamento de logs não equivale a auditoria integral da eleição; leia a metodologia.'}
    for k in ['arquivos_processados','erros','habilitacoes','votos_computados','votos_vinculados',
        'com_evento_mesario','com_evento_mesario_com_voto','sem_evento_biometrico',
        'sem_evento_biometrico_com_voto','biometrica','mesario_explicito',
        'digital_mesario_gravada','digital_mesario_sem_associacao','ano_nascimento_sem_evento_biometrico',
        'tipo_outro','indefinida','avisos','linhas_dia_malformadas','secoes_principais_config_oficial',
        'secoes_oficiais_com_log_processado','secoes_config_sem_log_processado']:
        summary[k]=sum(r.get(k,0) for r in results)
    for k in ['maior_sequencia_mesario','maior_sequencia_sem_biometria']:
        summary[k]=max((r[k] for r in results),default=0)
    rank.sort(key=lambda r:(-int(r['tamanho']),r['uf'],r['arquivo'],r['inicio']))
    write_csv(destination/'ranking_sequencias_mesario.csv',rank)
    write_csv(destination/'distribuicao_sequencias_por_estado.csv',distribution)
    fields=list(dict.fromkeys(k for r in results for k in r))
    write_csv(destination/'resumo_por_estado.csv',results,fields)
    atomic_json(destination/'resumo_nacional.json',summary)
    md=['# Auditor Eleitoral Independente 2026 — relatório de execução','',
        '**Escopo:** logs públicos do segundo turno de 25/10/2026, durante todo o dia. Motor '+VERSION+'.','',
        f"**Situação:** {len(results)} de 28 UFs processadas (26 estados, Distrito Federal e exterior).",
        f"**Arquivos de log processados:** {number(summary['arquivos_processados'])}.",
        f"**Erros de leitura:** {number(summary['erros'])}; **habilitações indefinidas:** {number(summary['indefinida'])}; **avisos:** {number(summary['avisos'])}.",'']
    if pending:md+=['**UFs pendentes:** '+', '.join(pending)+'.','']
    md+=['## Resultados por estado','',
        'As contagens abaixo são de habilitações e de eventos de voto vinculados pelo analisador. As categorias permanecem distintas.','',
        '| UF | Logs | Cobertura da lista principal | Habilitações com eventos de mesário | Destas, com voto vinculado | Maior série de habilitações com eventos de mesário | Maior série no grupo ampliado | Indefinidas |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in results:
        coverage=f"{r['cobertura_config_pct']:.2f}%" if 'cobertura_config_pct' in r else 'não verificada'
        md.append('| '+ ' | '.join([r['uf'],number(r['arquivos_processados']),coverage,
            number(r['com_evento_mesario']),number(r['com_evento_mesario_com_voto']),
            str(r['maior_sequencia_mesario']),str(r['maior_sequencia_sem_biometria']),number(r['indefinida'])])+' |')
    md+=['','## Totais das UFs processadas','',
        f"- Habilitações: {number(summary['habilitacoes'])}.",
        f"- Eventos de voto computado: {number(summary['votos_computados'])}.",
        f"- Habilitações com eventos de mesário: {number(summary['com_evento_mesario'])}; com voto vinculado: {number(summary['com_evento_mesario_com_voto'])}.",
        f"- Grupo ampliado sem evento biométrico reconhecido: {number(summary['sem_evento_biometrico'])}; com voto vinculado: {number(summary['sem_evento_biometrico_com_voto'])}.",'',
        '## Quantas sequências foram identificadas','',
        'Contagens de séries máximas consecutivas de habilitações. Uma série de dez também entra nas faixas de pelo menos três e cinco; as faixas não devem ser somadas.','',
        '| Grupo | Séries de 3 ou mais | Séries de 5 ou mais | Séries de 10 ou mais |',
        '|---|---:|---:|---:|']
    for group,label in [('mesario','Com eventos de mesário'),('sem_biometria','Grupo ampliado sem evento biométrico')]:
        ds=[r for r in distribution if r['grupo']==group]
        md.append('| '+' | '.join([label,*[number(sum(r['sequencias_ge_'+str(t)] for r in ds)) for t in [3,5,10]]])+' |')
    md += ['',
        '## Maiores sequências de habilitações com eventos de mesário','',
        'Ranking descritivo; não é classificação de fraude. Datas e horários são os registrados pelos equipamentos. O CSV contém todos os casos, referências às linhas e categorias.','',
        '| UF | Município | Zona / seção | Habilitações | Votos vinculados | Início | Fim |',
        '|---|---|---|---:|---:|---|---|']
    for r in rank[:20]:
        md.append('| '+' | '.join([r['uf'],r['municipio_nome'] or r['municipio'],r['zona']+' / '+r['secao'],r['tamanho'],r['votos_vinculados'],r['inicio'],r['fim']])+' |')
    md+=['','## Como interpretar','',
        'O grupo de eventos de mesário reúne: mensagem explícita de habilitação; captura seguida de gravação de digital de mesário; ou indicação de que a habilitação não pode ser associada a um mesário. Essa última mensagem não significa, isoladamente, que o voto foi irregular.',
        '',
        'O grupo ampliado acrescenta confirmações do ano de nascimento sem evento biométrico reconhecido na tentativa. É uma inferência do log; não informa se o eleitor tinha biometria cadastrada. Não se deve equiparar esse total ao indicador específico do BU sobre biometria cadastrada não reconhecida.',
        '',
        'Uma habilitação pode não terminar em voto computado. Por isso, as colunas de habilitação e de voto vinculado são separadas. Avisos e categorias indefinidas estão listados e não foram convertidos automaticamente em liberações por mesário.',
        '',
        'A cobertura compara as seções identificadas nos logs com as seções principais da configuração oficial. Seções agregadas são separadas. Seções não instaladas ou com apuração por cédulas podem exigir exame distinto. Uma cobertura de 100% não elimina ressalvas de classificação.',
        '',
        'O processamento lê logs aninhados de equipamentos substituídos e elimina cópias de linhas por multiplicidade máxima. São registrados CRC de leitura e SHA-256 por log. Não há autenticação de assinaturas criptográficas nesta ferramenta.',
        '',
        '**Limites da conclusão:** sequências e frequências descrevem os registros publicados. Não demonstram a identidade ou a presença física dos votantes, não revelam o candidato escolhido e não comprovam fraude. Este trabalho não verifica hardware, software instalado, documentos de identificação, assinaturas dos cadernos de votação ou intenção de voto.',
        '',
        '## Fontes e reprodução','',
        '- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao).',
        '- Configurações oficiais de seções, pleito 3221, preservadas por UF junto aos resultados.',
        '- O arquivo `fontes_estaduais.json` registra os endereços dos pacotes e os metadados observados.',
        '- Código, comando de execução, testes e metodologia detalhada acompanham a entrega.',
        '',
        '```bash','MALLOC_ARENA_MAX=2 python auditar.py --brasil --saida resultados --estados-simultaneos 1 --conexoes 4 --processos 1 --limite-memoria-mib 1536 --apagar-pacotes',
        'python consolidar.py --resultados resultados --saida entrega','```','']
    (destination/'relatorio_auditoria_2026.md').write_text('\n'.join(md),encoding='utf-8')
    sums=[]
    with zipfile.ZipFile(destination/'resultados_auditoria_2026.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for r in results:
            for p in sorted((root/r['uf']).iterdir()):
                if p.suffix in ['.csv','.json'] and p.name not in ['progresso.json','falha.json']:
                    z.write(p,r['uf']+'/'+p.name)
                    sums.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+r['uf']+'/'+p.name)
        for name in ['fontes_estaduais.json']:
            p=root/name
            if p.exists():z.write(p,name)
        for name in ['ranking_sequencias_mesario.csv','distribuicao_sequencias_por_estado.csv','resumo_por_estado.csv','resumo_nacional.json','relatorio_auditoria_2026.md']:
            p=destination/name;z.write(p,name)
            sums.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+name)
        z.writestr('SHA256SUMS.txt','\n'.join(sums)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print('ZIP_BYTES', (destination/'resultados_auditoria_2026.zip').stat().st_size)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--resultados',type=Path,default=Path('resultados_v2'))
    p.add_argument('--saida',type=Path,default=Path('entrega'))
    args=p.parse_args();consolidate(args.resultados,args.saida)
