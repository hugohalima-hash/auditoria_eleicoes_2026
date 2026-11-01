import unittest
from collections import Counter
from relatorios_nacionais.analisar import sequences,stats,histogram_stats,concentration

def session(i,kind='mesario_explicito',epoch=0,vote=True):
 x=dict(tipo=kind,hora='25/10/2026 10:%02d:00'%i,seg=36000+i*60,origem='raiz!logd.dat',urna='1',epoca=epoch,linha=i*10+1,linha_desfecho=i*10+9)
 if vote:x['voto']=x['hora']
 return x
COMMON=dict(uf='AC',municipio='Teste',zona='0001',secao='0001',arquivo='log.jez',admissivel='True')
class ReportTests(unittest.TestCase):
 def test_boundary_never_links(self):
  a=sequences([session(0),session(1,epoch=1),session(2,epoch=1)],COMMON,[100]*30)
  for r in a:self.assertEqual(r['liberacoes'],2);self.assertEqual(r['horarios'],'10:01:00 | 10:02:00')
 def test_suspension_breaks_completed_only(self):
  a=sequences([session(0),session(1,vote=False),session(2)],COMMON,[100]*30)
  self.assertFalse(any(x['apenas_concluidas'] for x in a));self.assertTrue(all(x['liberacoes']==3 for x in a))
 def test_mixed_is_not_mesario_run(self):
  a=sequences([session(0),session(1,'ano_nascimento_sem_evento_biometrico'),session(2)],COMMON,[100]*30)
  self.assertTrue(all(x['grupo']=='conjunto' for x in a));self.assertEqual(a[0]['mesario'],2);self.assertEqual(a[0]['ano'],1)
 def test_interval_is_start_to_start(self):
  a=sequences([session(0),session(1),session(2)],COMMON,[100]*30)
  self.assertEqual(a[0]['intervalos_seg'],'60 | 60');self.assertEqual(a[0]['media_seg'],60)
 def test_small_reference_not_flagged(self):
  a=sequences([session(0),session(1),session(2)],COMMON,[100]*29)
  self.assertFalse(any(x['triagem_ritmo'] for x in a))
 def test_quarantine_not_flagged(self):
  a=sequences([session(0),session(1),session(2)],dict(COMMON,admissivel='False'),[100]*30)
  self.assertFalse(any(x['triagem_ritmo'] for x in a))
 def test_histogram_matches_uncompressed_distribution(self):
  a=[23,45,45,90,100,100,500]
  self.assertEqual(histogram_stats(Counter(a)),stats(a));self.assertEqual(histogram_stats(Counter()),{'n':0})
 def test_empty_sequences_supported(self):self.assertEqual(sequences([],COMMON,[]),[])
 def test_concentration_small_peer_group_excluded(self):
  p=[dict(codigo_municipio='1',municipio='Teste',zona='1',arquivo=str(i),admissivel='True',votos_computados=200,percentual_verificacao=100 if i==0 else 1) for i in range(19)]
  self.assertEqual(concentration(p),([],[],0))
if __name__=='__main__':unittest.main()
