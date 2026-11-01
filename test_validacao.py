"""Regressões dos defeitos observados, fronteiras e conservação de eventos."""
import csv
import io
import json
import random
import tempfile
import unittest
import zipfile
from pathlib import Path
from motor import analyze, extract, read_logs, ENGINE_SHA256, VERSION
from test_motor import archive, line, DAY
from anomalias import scan
from integridade import manifest, verified, REQUIRED


def parse(messages):
    return extract(archive('\n'.join(line(f'08:{i//60:02d}:{i%60:02d}',m,u) for i,(m,u) in enumerate(messages))), DAY)


class LifecycleTests(unittest.TestCase):
    def test_biometric_evidence_after_habilitation(self):
        ss,w,m=parse([('Eleitor foi habilitado','U1'),('Tipo de habilitação do eleitor [biométrica]','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(ss[0]['tipo'],'biometrica');self.assertFalse(w)
        self.assertTrue(m['admissivel_estatistica'])

    def test_late_mesario_evidence(self):
        ss,w,m=parse([('Eleitor foi habilitado','U1'),('Mesário 123 habilitou o eleitor','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(ss[0]['tipo'],'mesario_explicito');self.assertFalse(w)

    def test_explicit_suspension_is_explained_without_vote(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [biométrica]','U1'),('Eleitor foi habilitado','U1'),('Eleitor foi suspenso pelo mesário','U1'),('Eleitor foi suspenso e não confirmou nenhum voto','U1')])
        self.assertEqual(ss[0]['desfecho'],'suspensa_sem_voto')
        self.assertEqual(m['suspensas_sem_voto'],1);self.assertFalse(w)
        self.assertEqual(m['ciclos_sem_desfecho_explicado'],0)
        self.assertTrue(m['admissivel_estatistica'])

    def test_partial_suspension_waits_for_computed_event(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [biométrica]','U1'),('Eleitor foi habilitado','U1'),('Eleitor votou parcialmente e em seguida foi suspenso','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(ss[0]['desfecho'],'voto_computado');self.assertEqual(m['suspensoes_parciais'],1)
        self.assertFalse(w)

    def test_partial_suspension_never_invents_vote(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [biométrica]','U1'),('Eleitor foi habilitado','U1'),('Eleitor votou parcialmente e em seguida foi suspenso','U1')])
        self.assertNotIn('voto',ss[0]);self.assertEqual(m['votos_computados'],0)
        self.assertFalse(m['admissivel_estatistica'])

    def test_device_transition_cannot_link_vote(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [biométrica]','U1'),('Eleitor foi habilitado','U1'),('O voto do eleitor foi computado','U2')])
        self.assertNotIn('voto',ss[0]);self.assertEqual(m['votos_sem_habilitacao'],1)
        self.assertFalse(m['admissivel_estatistica'])

    def test_device_transition_cannot_carry_evidence(self):
        ss,w,m=parse([('Mesário 123 habilitou o eleitor','U1'),('Eleitor foi habilitado','U2'),('O voto do eleitor foi computado','U2')])
        self.assertEqual(ss[0]['tipo'],'indefinida')

    def test_new_attempt_cannot_receive_previous_vote(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [biométrica]','U1'),('Eleitor foi habilitado','U1'),('Aguardando digitação do identificador do eleitor','U1'),('O voto do eleitor foi computado','U1')])
        self.assertNotIn('voto',ss[0]);self.assertEqual(m['votos_sem_habilitacao'],1)

    def test_pre_habilitation_cancel_does_not_count_as_voter(self):
        ss,w,m=parse([('Mesário 123 habilitou o eleitor','U1'),('Habilitação cancelada durante reconhecimento biométrico','U1'),('Eleitor foi habilitado','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(len(ss),1);self.assertEqual(ss[0]['tipo'],'indefinida')
        self.assertEqual(m['tentativas_canceladas_antes_habilitacao'],1)

    def test_conflicting_evidence_is_quarantined(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [biométrica]','U1'),('Mesário 123 habilitou o eleitor','U1'),('Eleitor foi habilitado','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(ss[0]['tipo'],'indefinida');self.assertFalse(m['admissivel_estatistica'])

    def test_reboot_closes_cycle(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [biométrica]','U1'),('Eleitor foi habilitado','U1'),('Urna desligada pela chave','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(ss[0]['desfecho'],'interrompida');self.assertEqual(m['votos_sem_habilitacao'],1)

    def test_clock_regression_cannot_link_vote(self):
        raw=archive('\n'.join([line('08:00:00','Tipo de habilitação do eleitor [biométrica]'),line('08:02:00','Eleitor foi habilitado'),line('08:01:00','O voto do eleitor foi computado')]))
        ss,w,m=extract(raw,DAY);self.assertNotIn('voto',ss[0]);self.assertEqual(m['regressoes_relogio'],1)

    def test_invalid_timestamp_does_not_crash_or_bridge_cycle(self):
        raw=archive('\n'.join([line('08:00:00','Tipo de habilitação do eleitor [biométrica]'),line('08:00:01','Eleitor foi habilitado'),line('99:99:99','Evento'),line('08:00:03','O voto do eleitor foi computado')]))
        ss,w,m=extract(raw,DAY);self.assertEqual(m['linhas_dia_malformadas'],1)
        self.assertNotIn('voto',ss[0]);self.assertEqual(m['votos_sem_habilitacao'],1)

    def test_other_day_cannot_bridge_cycle(self):
        raw=archive('\n'.join([line('08:00:00','Tipo de habilitação do eleitor [biométrica]'),line('08:00:01','Eleitor foi habilitado'),line('08:00:02','Evento').replace(DAY,'26/10/2026'),line('08:00:03','O voto do eleitor foi computado')]))
        ss,w,m=extract(raw,DAY)
        self.assertNotIn('voto',ss[0]);self.assertEqual(ss[0]['desfecho'],'fronteira_data')
        self.assertEqual(m['votos_sem_habilitacao'],1);self.assertFalse(m['admissivel_estatistica'])

    def test_distinct_blocks_never_join_cycles_or_drop_isolated_lines(self):
        shared=line('08:00:01','Eleitor foi habilitado')
        raw=archive(shared+'\n'+line('08:00:02','O voto do eleitor foi computado'),{'old.jez':archive(line('08:00:00','Tipo de habilitação do eleitor [biométrica]')+'\n'+shared)})
        ls,blocks,dups=read_logs(raw);self.assertEqual(len(ls),4);self.assertEqual(dups,0)
        ss,w,m=extract(raw,DAY);self.assertEqual(len(ss),2);self.assertFalse(m['admissivel_estatistica'])
        self.assertNotIn('voto',ss[0])

    def test_duplicate_whole_blocks_keep_intrablock_multiplicity(self):
        t='\n'.join([line('08:00:00','O voto do eleitor foi computado')]*2)
        ls,n,dup=read_logs(archive(t,{'old.jez':archive(t)}))
        self.assertEqual((len(ls),n,dup),(2,2,2))

    def test_truncated_archive_fails_closed(self):
        with self.assertRaises(zipfile.BadZipFile):extract(archive('abc')[:20],DAY)

    def test_unknown_type_excluded(self):
        ss,w,m=parse([('Tipo de habilitação do eleitor [novo tipo]','U1'),('Eleitor foi habilitado','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(ss[0]['tipo'],'tipo_outro');self.assertFalse(m['admissivel_estatistica'])

    def test_negated_or_quoted_authorization_is_not_evidence(self):
        ss,w,m=parse([('Falha: mesário 123 habilitou o eleitor? Não.','U1'),('Eleitor foi habilitado','U1'),('O voto do eleitor foi computado','U1')])
        self.assertEqual(ss[0]['tipo'],'indefinida');self.assertFalse(m['admissivel_estatistica'])

    def test_generated_mixed_outcomes_conserve_counts(self):
        rng=random.Random(20261031);messages=[];expected=[]
        for _ in range(500):
            messages.append(('Aguardando digitação do identificador do eleitor','U1'))
            late=rng.choice([True,False]);end=rng.choice(['vote','suspend','cancel'])
            if not late:messages.append(('Tipo de habilitação do eleitor [biométrica]','U1'))
            messages.append(('Eleitor foi habilitado','U1'))
            if late:messages.append(('Tipo de habilitação do eleitor [biométrica]','U1'))
            messages.append(({'vote':'O voto do eleitor foi computado','suspend':'Eleitor foi suspenso e não confirmou nenhum voto','cancel':'Votação cancelada'}[end],'U1'));expected.append(end)
        ss,w,m=parse(messages)
        self.assertEqual(len(ss),500);self.assertFalse(w)
        self.assertTrue(all(s['tipo']=='biometrica' for s in ss))
        self.assertEqual(m['votos_computados'],expected.count('vote'))
        self.assertEqual(m['suspensas_sem_voto'],expected.count('suspend'))
        self.assertEqual(m['canceladas_sem_voto'],expected.count('cancel'))
        self.assertEqual(m['residuo_conservacao_habilitacoes'],0)
        self.assertEqual(m['residuo_conservacao_votos'],0)

    def test_real_regression_excerpts(self):
        cases=json.loads((Path(__file__).parent/'validacao/casos_reais.json').read_text())
        self.assertGreaterEqual(len(cases),10)
        for case in cases:
            with self.subTest(case=case['arquivo'],line=case['linha_alvo']):
                raw=archive('\n'.join(line(e['hora'][11:],e['mensagem'],'U1') for e in case['eventos']))
                ss,w,m=extract(raw,DAY)
                target=[s for s in ss if s['hora']==case['hora_alvo']]
                self.assertEqual(len(target),1)
                self.assertEqual(target[0]['tipo'],case['tipo_esperado'])
                self.assertEqual(target[0]['desfecho'],case['desfecho_esperado'])
                self.assertEqual(bool(target[0].get('suspensao_parcial')),case.get('suspensao_parcial',False))


class QualityGateTests(unittest.TestCase):
    def test_old_version_and_unresolved_sections_cannot_enter_peer_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'resultados';root.mkdir();out=Path(tmp)/'out'
            old=root/'OLD';old.mkdir();(old/'resumo.json').write_text(json.dumps({'versao_motor':'2.1'}));(old/'urnas.csv').write_text('arquivo\n')
            current=root/'NEW';current.mkdir();(current/'resumo.json').write_text(json.dumps({'versao_motor':VERSION,'sha256_motor':ENGINE_SHA256,'arquivos_processados':20,'logs_no_pacote':20}))
            rows=[dict(arquivo=f'file{i}',municipio='1',zona='1',secao=str(i),habilitacoes=200,com_evento_mesario=190 if i==19 else 10,votos_computados=200,votos_vinculados=200,admissivel_estatistica=i!=19,maior_sequencia_mesario=100 if i==19 else 1) for i in range(20)]
            with (current/'urnas.csv').open('w') as f:
                w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
            (current/'sequencias.csv').write_text('arquivo,grupo,tamanho\n')
            for name in REQUIRED:
                if not (current/name).exists():(current/name).write_text('arquivo\n')
            (current/'manifesto.json').write_text(json.dumps(manifest(current,ENGINE_SHA256)))
            result=scan(root,out)
            self.assertEqual(result['ufs_excluidas_versao_antiga'],['OLD'])
            self.assertEqual(result['secoes_em_quarentena'],1)
            self.assertEqual(result['alertas'],0)
            self.assertIsNone(result['acuracia_certificada'])

    def test_tampered_or_incomplete_result_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            self.assertFalse(verified(p,ENGINE_SHA256))
            for name in REQUIRED:(p/name).write_text('original')
            (p/'manifesto.json').write_text(json.dumps(manifest(p,ENGINE_SHA256)))
            self.assertTrue(verified(p,ENGINE_SHA256))
            (p/'urnas.csv').write_text('modificado')
            self.assertFalse(verified(p,ENGINE_SHA256))


if __name__=='__main__':unittest.main()
