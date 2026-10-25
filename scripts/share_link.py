"""Print a notebook link that recipients can open without entering a login code."""
import argparse
import json
from pathlib import Path
import subprocess
import time
from urllib.parse import quote

parser = argparse.ArgumentParser(description=__doc__)
options = parser.add_mutually_exclusive_group()
options.add_argument('--public-url', action='store_true', help='omit login information for a public document')
options.add_argument('--include-token', action='store_true', help=argparse.SUPPRESS)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
probe = ('import json, os; from urllib.request import build_opener, ProxyHandler; '
         'data=json.loads(build_opener(ProxyHandler({})).open('
         '"http://ngrok:4040/api/tunnels", timeout=3).read()); '
         'data["jupyter_token"]=os.environ["JUPYTER_TOKEN"]; print(json.dumps(data))')
deadline = time.monotonic() + 30
while True:
    result = subprocess.run(['docker', 'compose', 'exec', '-T', 'notebook', 'python', '-c', probe],
                            cwd=root, capture_output=True, text=True, timeout=8)
    try:
        data = json.loads(result.stdout)
        tunnels = data['tunnels']
        base = next(t['public_url'] for t in tunnels if t['public_url'].startswith('https://'))
        break
    except (ValueError, KeyError, StopIteration):
        if time.monotonic() >= deadline:
            raise SystemExit('ngrok 주소를 받지 못했습니다. ngrok 서비스와 계정 인증 설정을 확인하세요.')
        time.sleep(1)
url = base + '/lab/tree/' + quote('한국로텍_데이터분석.ipynb')
if not args.public_url:
    token = data.get('jupyter_token', '').strip()
    if not token:
        raise SystemExit('실행 중인 서버의 로그인 정보를 확인할 수 없습니다.')
    url += '?token=' + quote(token, safe='')
print(url)
