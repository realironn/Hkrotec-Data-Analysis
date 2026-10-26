"""Keep the editable notebook on the output mount and start authenticated Jupyter."""
import json
import os
from pathlib import Path
import sys

ROOT = Path('/workspace')
NAME = '한국로텍_데이터분석.ipynb'


def prepare():
    if not os.environ.get('JUPYTER_TOKEN', '').strip():
        raise RuntimeError('JUPYTER_TOKEN을 비어 있지 않은 값으로 설정하세요.')
    for directory in [Path(os.environ['HOME']), Path(os.environ['JUPYTER_RUNTIME_DIR'])]:
        directory.mkdir(parents=True, exist_ok=True)
    # Fail before opening a server when mounts or private references are missing.
    for relative in ['raw', 'csv/manifest.csv', 'prepared/five_fold/daily_targets.csv',
                     'prepared/five_fold/fold_assignments.csv',
                     'prepared/한국로텍_분석참고자료.json']:
        if not (ROOT / relative).exists():
            raise FileNotFoundError(f'필수 입력자료 없음: {relative}')
    destination = ROOT / NAME
    if not destination.exists():
        with destination.open('xb') as stream:
            stream.write((Path('/opt/rotec') / NAME).read_bytes())
    import hashlib
    runtime = json.loads(destination.read_text())['metadata']['rotec_runtime']
    reference = ROOT / runtime['private_reference_file']
    if hashlib.sha256(reference.read_bytes()).hexdigest() != runtime['private_reference_sha256']:
        raise ValueError('비공개 참고자료와 노트북의 SHA256이 다릅니다.')
    (ROOT / '분석결과').mkdir(exist_ok=True)


if __name__ == '__main__':
    prepare()
    from jupyter_server.services.contents.manager import ContentsManager
    # Keep mounted inputs available to the notebook while simplifying the file list.
    hidden_names = [*ContentsManager.hide_globs.default(), 'raw', 'csv', 'prepared']
    os.execv(sys.executable, [sys.executable, '-m', 'jupyterlab', '--no-browser',
             '--ServerApp.ip=0.0.0.0', '--ServerApp.port=8888',
             '--ServerApp.port_retries=0', '--ServerApp.root_dir=/workspace',
             '--ServerApp.allow_remote_access=True',
             '--ServerApp.trust_xheaders=True',
             '--ServerApp.use_redirect_file=False',
             '--ServerApp.custom_display_url=http://127.0.0.1:8888',
             '--ContentsManager.hide_globs=' + json.dumps(hidden_names),
             '--LabApp.default_url=/lab/tree/' + NAME])
