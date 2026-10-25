# 서버 담당자용 준비 안내

공유받은 링크로 결과를 보거나 분석을 실행하는 분은 [사용 안내](./user-guide.md)를 참고합니다.

서버에서는 [Docker·Jupyter 실행 가이드](./docker-setup.md)의 구성을 사용할 수 있습니다. 실제 데이터 읽기 전용 연결, 결과 보관, 전체 셀 실행과 ngrok 링크 공유 방법을 포함합니다. 이 문서의 나머지 내용은 Python을 직접 설치할 때의 안내입니다.

실제 외부 접속 주소는 운영자가 ngrok을 시작한 뒤 확인합니다. 로그인 토큰이 들어간 링크는 공개 README에 추가하지 않습니다.

## 배치할 파일

회사별로 전용 작업 폴더를 만들고 아래 파일을 배치합니다.

```text
한국로텍_작업폴더/
    한국로텍_데이터분석.ipynb
    requirements.txt
    raw/
    csv/
    prepared/
        한국로텍_분석참고자료.json
```

- 노트북과 requirements.txt는 이 저장소에서 받습니다.
- 입력자료 3개 폴더와 분석참고자료 JSON은 담당자가 별도로 제공합니다.
- 원본자료·분석참고자료·실행 결과를 공개 Git 저장소에 올리지 않습니다.

공개용 노트북은 측정값과 이미지 묶음을 외부 JSON에서 읽습니다. 기존에 전달한 단독 실행용 노트북과 공개용 노트북은 이 자료 로딩 방식에 차이가 있습니다.

## 실행 환경

검증한 환경은 **Windows와 Linux Docker, Python 3.14**입니다. Linux Docker에서는 2026-10-25에 실제 데이터로 코드 셀 18개와 분석 검증 15개를 통과했습니다. 분석은 CPU에서 실행하며 GPU는 사용하지 않습니다.

Windows 서버에서는 [Windows 설치·실행 가이드](./windows-setup.md)의 환경 준비 방법을 그대로 사용할 수 있습니다.
Linux에 직접 설치한다면 Python 3.14 환경, 필요한 패키지와 한글 폰트를 준비한 뒤 전체 실행을 확인합니다. Docker 이미지는 이 환경을 포함합니다.

requirements.txt는 `pywinpty`를 Windows에서만 설치하도록 구분합니다. Linux에서 한글 그래프를 그릴 때는 Noto Sans CJK 또는 나눔고딕 계열의 폰트가 필요합니다.

## 서버 시작

아래는 Python 3.14가 준비된 Linux 서버의 명령 예시입니다. 작업 폴더에서 실행합니다.

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m notebook --no-browser --ServerApp.ip=127.0.0.1 --ServerApp.port=8888 --ServerApp.root_dir=.
```

Windows에서는 마지막 명령의 `.venv/bin/python`을 `.\.venv\Scripts\python.exe`로 바꿉니다.

Jupyter의 기본 인증을 유지합니다. 외부 접속은 운영 환경에 맞는 HTTPS 주소와 인증을 통해 제공해 주세요. 토큰이나 비밀번호는 공개 README에 적지 않습니다. 여러 업체가 같은 서버를 이용한다면 JupyterHub 등의 사용자별 환경으로 자료와 실행 세션을 구분합니다.

공식 안내: [Jupyter 서버 운영](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html), [Jupyter 인증](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)

## 공유할 링크

서버 주소를 정한 뒤, 운영자가 해당 노트북을 열어 확인한 **노트북 페이지의 주소**를 전달합니다. 일반적인 경로는 다음과 같습니다.

```text
/notebooks/한국로텍_데이터분석.ipynb
```

JupyterHub에서는 사용자별 주소 앞부분이 달라질 수 있습니다. 주소를 추정해서 안내하지 말고 로그인 후 노트북을 직접 열어 확인합니다.
로그인 정보는 허가된 이용자에게 별도로 전달합니다.

## 제공 전 확인

1. 담당자 계정으로 접속해 노트북이 열리는지 확인합니다.
2. 첫 코드 셀부터 모든 셀을 실행합니다.
3. `분석결과/한국로텍_분석보고서.html`과 계산표·그래프가 저장되는지 확인합니다.
4. 확인한 접속 링크를 README에 추가합니다.

GitHub 열람 링크가 실제 서버 실행 링크를 대신하지 않습니다.
