import importlib.util
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

P=Path(__file__).resolve().parents[1]/'scripts'/'shieldcn_visual.py'
spec=importlib.util.spec_from_file_location('visual',P)
visual=importlib.util.module_from_spec(spec)
spec.loader.exec_module(visual)

class VisualTests(unittest.TestCase):
 def test_query_encodes_icon_and_jsonpath(self):
  q=visual.params({'logo':'lu:Zap','query':'$.history[*].skills','color':'ffffff'})
  parsed=parse_qs(q)
  self.assertEqual(parsed['logo'],['lu:Zap'])
  self.assertEqual(parsed['query'],['$.history[*].skills'])
 def test_escape(self):
  self.assertIn('--',visual.escape_segment('Go-lang'))
 def test_adaptive(self):
  html=visual.render('badge/Skills-10-ffffff.svg',{'logoColor':'ffda00'},alt='Skills count')
  self.assertIn('prefers-color-scheme: dark',html)
  self.assertIn('mode=light',html)
  self.assertIn('mode=dark',html)
  self.assertIn('Skills count',html)
  self.assertIn('&amp;',html)
 def test_safe_link(self):
  output=visual.render('badge/a-b-white.svg',{},link='https://example.org?a=1&b=2')
  self.assertIn('a=1&amp;b=2',output)

if __name__=='__main__':unittest.main()
