"""Read the local ngrok agent API and print a shareable notebook link."""
import argparse
import json
from pathlib import Path
import subprocess
import time
from urllib.parse import quote

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--include-token', action='store_true', help='include the private Jupyter login token')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
probe = ('from urllib.request import build_opener, ProxyHandler; '
         'print(build_opener(ProxyHandler({})).open('
         '"http://ngrok:4040/api/tunnels", timeout=3).read().decode())')
deadline = time.monotonic() + 30
while True:
    result = subprocess.run(['docker', 'compose', 'exec', '-T', 'notebook', 'python', '-c', probe],
                            cwd=root, capture_output=True, text=True, timeout=8)
    try:
        tunnels = json.loads(result.stdout)['tunnels']
        base = next(t['public_url'] for t in tunnels if t['public_url'].startswith('https://'))
        break
    except (ValueError, KeyError, StopIteration):
        if time.monotonic() >= deadline:
            raise SystemExit('ngrok 주소를 받지 못했습니다. ngrok 서비스와 계정 인증 설정을 확인하세요.')
        time.sleep(1)
url = base + '/lab/tree/' + quote('한국로텍_데이터분석.ipynb')
if args.include_token:
    env_file = root / '.env'
    settings = dict(line.split('=', 1) for line in env_file.read_text().splitlines()
                    if line and not line.startswith('#') and '=' in line)
    url += '?token=' + quote(settings['JUPYTER_TOKEN'].strip(), safe='')
print(url)
