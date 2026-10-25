"""Execute every notebook cell and preserve partial output on failure."""
import argparse
import json
from pathlib import Path
import time

import nbformat
from nbclient import NotebookClient

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--workspace', type=Path, default=Path('/workspace'))
parser.add_argument('--timeout', type=int, default=1800, help='timeout per cell in seconds')
args = parser.parse_args()
root = args.workspace.resolve()
source = root / '한국로텍_데이터분석.ipynb'
target = root / '분석결과' / '한국로텍_데이터분석_실행완료.ipynb'
target.parent.mkdir(parents=True, exist_ok=True)
notebook = nbformat.read(source, as_version=4)


def progress(cell, cell_index):
    if cell.cell_type == 'code':
        print(f'셀 {cell_index + 1}/{len(notebook.cells)} 실행', flush=True)


client = NotebookClient(notebook, timeout=args.timeout, kernel_name='python3',
                        resources={'metadata': {'path': str(root)}},
                        on_cell_start=progress)
started = time.monotonic()
status_file = target.parent / 'server-validation.json'
status_file.write_text(json.dumps({'status': 'running'}, indent=2) + '\n', encoding='utf-8')
try:
    client.execute()
except BaseException as error:
    failure_file = target.with_name('한국로텍_데이터분석_실패기록.ipynb')
    nbformat.write(notebook, failure_file)
    status_file.write_text(json.dumps({
        'status': 'failed', 'elapsed_seconds': round(time.monotonic() - started, 1),
        'error_type': type(error).__name__, 'executed_notebook': failure_file.name,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise
else:
    nbformat.write(notebook, target)
    summary = {
        'status': 'passed', 'elapsed_seconds': round(time.monotonic() - started, 1),
        'code_cells': sum(c.cell_type == 'code' for c in notebook.cells),
        'executed_notebook': target.name,
    }
    status_file.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False), flush=True)
