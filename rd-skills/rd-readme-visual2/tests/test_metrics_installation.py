"""End-to-end smoke tests for deployable target repository metric assets."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install_metrics


class MetricsIntegrationTests(unittest.TestCase):
    def test_install_and_count_without_duplicate_history(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
            (repo / 'skills/demo').mkdir(parents=True)
            (repo / 'skills/demo/SKILL.md').write_text('---\nname: demo\n---\n')
            (repo / 'scripts').mkdir(exist_ok=True)
            (repo / 'scripts/runner.py').write_text('print(1)\n')
            install_metrics.install(repo)
            self.assertTrue((repo / '.readme-metrics.json').exists())
            self.assertTrue((repo / '.github/workflows/readme-metrics.yml').exists())
            self.assertTrue((repo / 'scripts/repo_metrics.py').exists())
            subprocess.run(['git', 'add', '-A'], cwd=repo, check=True)
            for date in ('2026-11-20', '2026-11-20', '2026-11-21'):
                subprocess.run([sys.executable, 'scripts/repo_metrics.py', '--date', date], cwd=repo,
                               check=True, stdout=subprocess.DEVNULL)
            latest = json.loads((repo / 'stats/badges.json').read_text())
            history = json.loads((repo / 'stats/history.json').read_text())['history']
            self.assertEqual(latest['skills'], 1)
            self.assertEqual(latest['scripts'], 2)  # original plus installed metric collector
            self.assertEqual(len(history), 2)
            self.assertEqual([x['date'] for x in history], ['2026-11-20', '2026-11-21'])

    def test_does_not_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            (repo / '.git').mkdir()
            (repo / '.readme-metrics.json').write_text('{"custom":true}')
            install_metrics.install(repo)
            self.assertEqual(json.loads((repo / '.readme-metrics.json').read_text()), {'custom': True})


if __name__ == '__main__':
    unittest.main()
