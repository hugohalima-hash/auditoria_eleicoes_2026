import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
import lote

class Response(io.BytesIO):
    def __init__(self,data=b'',status=200,headers=None):
        super().__init__(data)
        self.status=status
        self.headers=headers or {}

class DownloadTests(unittest.TestCase):
    def test_streamed_export_preserves_events_and_reuses_only_matching_cache(self):
        from test_motor import archive,line,DAY
        from integridade import verified
        from motor import ENGINE_SHA256
        import csv
        text='\n'.join(line(f'08:0{i}:0{j}',msg) for i in range(2)
            for j,msg in enumerate(['Mesário 123 habilitou o eleitor','Eleitor foi habilitado','O voto do eleitor foi computado']))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);source=p/'estado.zip';out=p/'resultado'
            with zipfile.ZipFile(source,'w') as z:
                for sec in ['0001','0002']:
                    z.writestr('o03221ac010070001'+sec+'-log.jez',archive(text))
            result=lote.process_archive(source,out,DAY,uf='LOCAL')
            self.assertEqual(result['habilitacoes'],4)
            self.assertEqual(result['votos_computados'],4)
            with (out/'sequencias.csv').open(encoding='utf-8-sig') as f:
                runs=list(csv.DictReader(f))
            self.assertEqual(len(runs),4)
            self.assertTrue(all(r['tamanho']=='2' and r['votos_vinculados']=='2' for r in runs))
            self.assertTrue(verified(out,ENGINE_SHA256))
            with patch.object(lote,'analyze',side_effect=AssertionError('cache compatível deveria ser reutilizado')):
                self.assertEqual(lote.process_archive(source,out,DAY,uf='LOCAL')['habilitacoes'],4)

    def test_parallel_ranges_reconstruct_zip_and_cache_final_file(self):
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w',zipfile.ZIP_STORED) as z:
            z.writestr('teste.dat',b'x'*(17*1024*1024))
        raw=buf.getvalue();calls=[]
        def fake(url,headers=None,method='GET'):
            calls.append((method,headers))
            if method=='HEAD':return Response(headers={'Content-Length':str(len(raw)),'ETag':'teste'})
            a,b=map(int,headers['Range'].removeprefix('bytes=').split('-'))
            return Response(raw[a:b+1],206,{'Content-Range':f'bytes {a}-{b}/{len(raw)}'})
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)
            with patch.object(lote,'request',fake):
                path=lote.download('AC',dest,2)
                self.assertEqual(path.read_bytes(),raw)
                n=len(calls)
                self.assertEqual(lote.download('AC',dest,2),path)
                self.assertEqual(len(calls),n)

    def test_server_ignoring_range_is_rejected_before_read(self):
        def fake(url,headers=None,method='GET'):
            if method=='HEAD':return Response(headers={'Content-Length':'32','ETag':'teste'})
            return Response(b'nao e zip',status=200)
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(lote,'request',fake):
                with self.assertRaisesRegex(RuntimeError,'não confirmou faixa'):
                    lote.download('AC',Path(temp),1)
            self.assertFalse((Path(temp)/'bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip').exists())

if __name__=='__main__':unittest.main()
