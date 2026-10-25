"""Check that the published distribution contains code and usable local links."""
from pathlib import Path
import ast
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
nb = json.loads((ROOT/'한국로텍_데이터분석.ipynb').read_text(encoding='utf-8'))
runtime = nb['metadata']['rotec_runtime']
assert 'embedded_review' not in runtime, 'Private image/reference payload must remain outside Git.'
assert 'progress' not in runtime, 'Internal correspondence must remain outside Git.'
assert runtime['private_reference_file'] == 'prepared/한국로텍_분석참고자료.json'
assert len(runtime['private_reference_sha256']) == 64
code_cells = 0
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        tree = ast.parse(''.join(cell['source']))
        assert not cell.get('outputs'), 'Remove execution outputs before publishing.'
        assert cell.get('execution_count') is None
        assert not any(isinstance(node, ast.Constant) and isinstance(node.value, str)
                       and len(node.value) > 20000 for node in ast.walk(tree)), 'Unexpected embedded payload.'
        code_cells += 1
assert code_cells == 18
lock = [line.strip() for line in (ROOT/'requirements.txt').read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith('#')]
assert lock == runtime['requirements_lock'], 'Notebook and server installation versions differ.'
assert any(line.startswith('pywinpty==') and 'sys_platform' in line for line in lock)

checked_links = 0
for document in [ROOT/'README.md', *sorted((ROOT/'docs').glob('*.md'))]:
    content = document.read_text(encoding='utf-8')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith('#'):
            continue
        path = (document.parent / unquote(parsed.path)).resolve()
        assert path.is_relative_to(ROOT), f'Local link leaves repository: {target}'
        assert path.is_file(), f'Broken local link: {document.name}: {target}'
        checked_links += 1

private_paths = ['raw/source.xlsx','csv/source.csv','prepared/한국로텍_분석참고자료.json',
                 '분석결과/한국로텍_분석보고서.html','.env','private/company.json',
                 'server-output/한국로텍_데이터분석.ipynb','.ngrok-authtoken']
result = subprocess.run(['git','check-ignore','-z','--stdin'],
                        input=('\0'.join(private_paths)+'\0').encode('utf-8'),
                        capture_output=True, cwd=ROOT)
assert len([p for p in result.stdout.split(b'\0') if p]) == len(private_paths), 'Private paths are not all ignored.'
print(f'PASS: {code_cells} code cells, {checked_links} local links, {len(private_paths)} private paths ignored.')
