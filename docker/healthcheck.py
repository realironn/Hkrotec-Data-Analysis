"""Check the authenticated API, not just a login-page response."""
import json
import os
from urllib.request import Request, urlopen

request = Request('http://127.0.0.1:8888/api/status',
                  headers={'Authorization': 'token ' + os.environ['JUPYTER_TOKEN']})
with urlopen(request, timeout=4) as response:
    assert response.status == 200
    assert 'kernels' in json.load(response)
