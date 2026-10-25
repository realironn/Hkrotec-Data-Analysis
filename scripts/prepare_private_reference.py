"""Export private references from an existing standalone notebook, outside Git."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-notebook', required=True, type=Path)
parser.add_argument('--data-dir', required=True, type=Path)
args = parser.parse_args()
source = json.loads(args.source_notebook.read_text(encoding='utf-8'))
runtime = source['metadata']['rotec_runtime']
bundle = runtime['embedded_review']
parameters = {}
for cell in source['cells']:
    if cell['cell_type'] != 'code':
        continue
    tree = ast.parse(''.join(cell['source']))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == 'ITEMS' for t in node.targets):
            parameters['items'] = ast.literal_eval(node.value)
        if isinstance(node, ast.List) and len(node.elts) > 1 and isinstance(node.elts[0], ast.Constant) \
                and node.elts[0].value == '전류밀도 이미지 산술 불일치':
            parameters['density_example'] = ast.literal_eval(node.elts[1])
if set(parameters) != {'items', 'density_example'}:
    raise ValueError('기존 노트북에서 분석 매개변수를 찾을 수 없습니다.')
reference = {'embedded_review': bundle, 'analysis_parameters': parameters}
payload = (json.dumps(reference, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
public_nb = Path(__file__).resolve().parents[1] / '한국로텍_데이터분석.ipynb'
expected = json.loads(public_nb.read_text(encoding='utf-8'))['metadata']['rotec_runtime']['private_reference_sha256']
actual = hashlib.sha256(payload).hexdigest()
if actual != expected:
    raise ValueError(f'배포본과 참고자료 버전이 다릅니다. 추출 SHA256: {actual}')
target = args.data_dir.resolve() / 'prepared/한국로텍_분석참고자료.json'
target.parent.mkdir(parents=True, exist_ok=True)
if target.exists():
    if target.read_bytes() != payload:
        raise FileExistsError('다른 참고자료가 이미 있습니다. 덮어쓰지 않습니다.')
else:
    with target.open('xb') as stream:
        stream.write(payload)
    target.chmod(0o600)
print(f'비공개 참고자료 준비 완료: {target}\nSHA256: {actual}')
