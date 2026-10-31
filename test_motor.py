import io
import unittest
import zipfile
from pathlib import Path
from motor import analyze, extract, read_logs, expected_starts

DAY='25/10/2026'

def line(t,msg,unit='12345678'):
    return f'{DAY} {t}\tINFO\t{unit}\tVOTA\t{msg}\tABCDEF'

def archive(text,nested=None):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('logd.dat',text.encode('latin-1'))
        if nested:
            for n,r in nested.items():z.writestr(n,r)
    return b.getvalue()

class MotorTests(unittest.TestCase):
    def test_recursive_reader_releases_text_without_cyclic_gc(self):
        import gc
        import tracemalloc
        text=(line('08:00:00','Evento informativo '+('x'*200))+'\n')*400
        raw=archive(text)
        gc.collect();gc.disable();tracemalloc.start()
        try:
            for _ in range(100):extract(raw,DAY)
            current,_=tracemalloc.get_traced_memory()
            self.assertLess(current,2*1024*1024)
        finally:
            tracemalloc.stop();gc.enable();gc.collect()

    def test_alternative_mesario_categories(self):
        text='\n'.join([line('08:00:00','Capturada a digital do mesário'),
            line('08:00:01','Não encontrou digital coletada em nenhum dos arquivos, vai salvar a digital em novo arquivo.'),
            line('08:00:02','Eleitor foi habilitado'),line('08:00:03','O voto do eleitor foi computado'),
            line('08:00:04','Digital coletada bate com uma digital gravada após o registro inicial de mesário. Não é possível associar a habilitação a um mesário.'),
            line('08:00:05','Eleitor foi habilitado'),line('08:00:06','O voto do eleitor foi computado')])
        r,runs,w,ss,_=analyze('o03221sp7145501370001-log.jez',archive(text),DAY)
        self.assertEqual(r['com_evento_mesario'],2)
        self.assertEqual(r['indefinida'],0)
        self.assertEqual(r['maior_sequencia_mesario'],2)
        self.assertEqual(w,[])

    def test_cancelled_attempt_does_not_leak_category(self):
        text='\n'.join([line('08:00:00','Mesário 123 habilitou o eleitor'),
            line('08:00:01','Habilitação cancelada durante a captura de digital do mesário'),
            line('08:00:02','Eleitor foi habilitado'),line('08:00:03','O voto do eleitor foi computado')])
        ss,_,_=extract(archive(text),DAY)
        self.assertEqual(ss[0]['tipo'],'indefinida')

    def test_nested_duplicates_preserve_multiplicity(self):
        ln=line('08:00:00','O voto do eleitor foi computado')
        raw=archive(ln+'\n'+ln,{'123456782510202608000001MI.jez':archive(ln+'\n'+ln)})
        ls,n,dup=read_logs(raw)
        self.assertEqual(len(ls),2)
        self.assertEqual(n,2)
        self.assertEqual(dup,2)

    def test_unknown_interrupts_run(self):
        msgs=[]
        for i,kind in enumerate(['Mesário 123 habilitou o eleitor',None,'Mesário 123 habilitou o eleitor']):
            if kind:msgs.append(line(f'08:0{i}:00',kind))
            msgs.append(line(f'08:0{i}:01','Eleitor foi habilitado'))
            msgs.append(line(f'08:0{i}:02','O voto do eleitor foi computado'))
        r,_,_,_,_=analyze('test.jez',archive('\n'.join(msgs)),DAY)
        self.assertEqual(r['maior_sequencia_mesario'],1)

    def test_expected_starts_against_enumeration(self):
        import itertools
        n,k,r=6,3,2
        counts=[]
        for pos in itertools.combinations(range(n),k):
            seq=[i in pos for i in range(n)]
            counts.append(sum(all(seq[i:i+r]) and (i==0 or not seq[i-1]) for i in range(n-r+1)))
        self.assertAlmostEqual(expected_starts(n,k,r),sum(counts)/len(counts))

    def test_uploaded_log_reconciliation(self):
        p=Path('../../inputs/o03221sp7145501370001-log.jez')
        if not p.exists():self.skipTest('amostra externa não disponível')
        r,_,w,_,_=analyze(p.name,p.read_bytes(),DAY)
        self.assertEqual((r['habilitacoes'],r['votos_computados'],r['votos_vinculados']),(189,189,189))
        self.assertEqual((r['biometrica'],r['com_evento_mesario'],r['ano_nascimento_sem_evento_biometrico']),(164,23,2))
        self.assertEqual(w,[])

if __name__=='__main__':unittest.main()
