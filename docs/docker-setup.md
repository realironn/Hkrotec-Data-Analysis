# Docker·Jupyter 서버 실행

이 문서는 서버를 설치·운영하는 담당자용입니다. 공유받은 링크로 이용하는 분은 [사용 안내](./user-guide.md)를 참고합니다.

Python 3.14, 분석 패키지와 한글 글꼴을 이미지에 설치합니다. 회사 자료는 서버에 두고 읽기 전용으로 연결합니다. 편집한 노트북과 결과는 별도 출력 폴더에 보관하므로 컨테이너를 다시 만들어도 유지됩니다.

## 1. 입력자료 준비

Docker Engine과 Docker Compose v2가 설치된 Linux 서버에서 저장소를 받습니다.

```bash
git clone https://github.com/realironn/Hkrotec-Data-Analysis.git
cd Hkrotec-Data-Analysis
```

회사 자료 폴더에는 다음 파일이 필요합니다. 자료를 Git 저장소나 Docker 이미지에 복사하지 않습니다.

```text
회사자료/
├── raw/                      # 원본 95개
├── csv/                      # 변환 CSV 109개, manifest.csv 포함
└── prepared/
    ├── five_fold/            # 기존 준비 CSV 6개
    └── 한국로텍_분석참고자료.json
```

기존 단독 실행용 노트북만 있는 경우, 그 안에 포함된 참고자료를 다음과 같이 분리할 수 있습니다. 원본 노트북과 기존 입력파일은 변경하지 않으며 `prepared`에 JSON 하나를 추가합니다. 내장 참고자료가 없는 공개용 노트북은 추출 원본으로 사용할 수 없습니다.

```bash
python3 scripts/prepare_private_reference.py \
  --source-notebook '/회사자료/한국로텍_최종/04_노트북_실행용/한국로텍_데이터분석.ipynb' \
  --data-dir '/회사자료'
```

추출한 JSON의 SHA256이 현재 배포본과 같아야 합니다. 이전 배포본의 JSON을 사용 중이면 위 명령으로 현재 노트북에 맞는 파일을 별도 자료 폴더에 준비합니다. 참고자료에는 회사 측정값과 이미지가 있으므로 비공개로 보관합니다.

## 2. 서버 설정

```bash
cp .env.example .env
chmod 600 .env
mkdir -p server-output
id -u
id -g
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

`.env`에서 다음 값을 편집합니다.

| 변수 | 설정 |
| --- | --- |
| `ROTEC_DATA_DIR` | 회사 자료 폴더의 절대 경로. `raw`, `csv`, `prepared`의 상위 폴더 |
| `ROTEC_OUTPUT_DIR` | 출력 폴더. 기본값 `./server-output` |
| `ROTEC_UID`, `ROTEC_GID` | `id -u`, `id -g`로 확인한 실행 담당자 번호 |
| `JUPYTER_TOKEN` | 위 명령으로 생성한 로그인 토큰 |
| `ROTEC_PORT` | 서버 내부 접속 포트. 기본값 `8890` |
| `NGROK_AUTHTOKEN` | ngrok 계정의 authtoken. Jupyter 로그인 토큰과 다름 |

입력자료를 읽을 권한과 출력 폴더에 쓸 권한이 필요합니다. `ROTEC_DATA_DIR`과 `ROTEC_OUTPUT_DIR`는 서로 다른 폴더로 지정합니다. `.env`와 `server-output`은 Git에서 제외됩니다. Docker 빌드에는 코드와 패키지 목록만 전달합니다.

## 3. 실행·전체 분석 확인

```bash
docker compose config --quiet
docker compose up -d --build notebook
docker compose ps
docker compose exec -T notebook python /opt/rotec/run_notebook.py
```

내부 주소는 `http://127.0.0.1:8890`입니다. 로그인할 때 `.env`의 `JUPYTER_TOKEN`을 입력합니다. 브라우저에서 Run → Run All Cells로 실행해도 같습니다. Docker에서는 첫 셀이 설치된 버전을 확인하고 패키지를 다시 설치하지 않습니다.

전체 실행 결과는 `server-output/분석결과/한국로텍_분석보고서.html`, 계산표는 `tables`, 그래프는 `figures`에 저장합니다. `한국로텍_데이터분석_실행완료.ipynb`에는 실행 결과가 남고, 실패 시 `한국로텍_데이터분석_실패기록.ipynb`가 저장됩니다. `server-validation.json`의 `passed`는 모든 셀이 오류 없이 끝났다는 뜻입니다. 분석 품질 검증 항목은 `tables/verification.csv`에서 별도로 확인합니다.

첫 전체 실행 때 출력 폴더 안에 `추가자료/입력`과 `추가자료/양식`이 만들어집니다. 여기에 정해진 CSV·Excel 양식으로 새 자료를 넣으면 다음 전체 실행에서 읽고, 검사 결과가 있는 자료를 포함해 모델을 다시 학습합니다. 입력 자료와 결과·모델은 출력 폴더에 보존하며 Git에서 제외합니다. [추가자료 양식과 학습 방식](./additional-data.md)

Jupyter의 파일 목록에는 분석 노트북, `분석결과`, `추가자료`와 입력자료 폴더인 `raw`, `csv`, `prepared`를 표시합니다. 입력자료는 읽기 전용으로 연결하며, 이용자가 원본과 변환·검증자료를 열람하거나 내려받을 수 있습니다.

운영 백업·검증용 파일과 로그는 출력 폴더 밖의 `server-admin`에 보관합니다. `server-admin`은 Git과 Docker 빌드에서 제외됩니다. 출력 폴더에는 이용자가 사용할 노트북과 결과·추가자료, `공유용_노트북_링크.txt`를 둡니다.

이미지의 노트북은 처음 실행할 때만 출력 폴더에 복사합니다. 이후 편집본은 보존합니다. 코드를 업데이트할 때는 출력 폴더의 기존 노트북을 `server-admin`에 백업하고 해당 파일을 제거한 뒤 컨테이너를 다시 생성합니다.

## 4. ngrok 실행 링크 만들기

ngrok 계정의 [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)을 `.env`의 `NGROK_AUTHTOKEN`에 넣습니다. [ngrok Docker 공식 안내](https://ngrok.com/download/docker)

```bash
docker compose --profile share up -d ngrok
python3 scripts/share_link.py
```

이 명령은 실행 중인 서버의 접속 정보가 포함된 HTTPS 노트북 주소를 출력합니다. 이 주소 전체를 전달하면 이용자는 로그인 코드를 입력하지 않고 열 수 있습니다. 공유할 사람에게 별도로 전달하며, 공개 GitHub 문서에는 넣지 않습니다.

Jupyter 파일 목록에서도 링크를 확인할 수 있도록 출력 폴더에 저장합니다. 기본 출력 폴더를 사용하는 경우 아래 명령을 실행합니다. 접속 주소나 로그인 토큰을 바꾸면 다시 실행해 파일을 갱신합니다.

```bash
python3 scripts/share_link.py > server-output/공유용_노트북_링크.txt
```

접속 정보를 뺀 기본주소만 확인하려면 아래 명령을 사용합니다. 이 기본주소는 로그인 화면이 나오므로 이용자에게 전달할 접속용 링크로 사용하지 않습니다.

```bash
python3 scripts/share_link.py --public-url
```

ngrok 관리 API는 서버 내부 `127.0.0.1:4041`에 연결됩니다. 요청 본문 검사는 꺼 두었습니다. ngrok 주소의 유지 여부는 계정의 도메인 설정에 따르므로, 재시작 후 위 명령으로 실제 주소를 확인합니다. 공유 종료 시에는 `docker compose --profile share stop ngrok`을 실행합니다.

교수님께 전달할 문구:

> 한국로텍 GitHub와 실제 데이터 실행용 노트북 링크를 공유드립니다. GitHub에는 코드와 설치·활용 가이드를 정리했습니다. 연구실 서버의 Docker 환경에 실제 회사 데이터를 연결해 두어, 별도 설치나 SSH 접속 없이 브라우저에서 분석을 실행하실 수 있습니다. 링크에서 노트북을 열고 Run → Run All Cells를 선택하면 되며, 결과는 분석결과 폴더에서 확인하실 수 있습니다.

## 5. 운영

```bash
docker compose ps
docker compose exec -T notebook python /opt/rotec/docker/healthcheck.py
docker compose stop notebook
docker compose start notebook
docker compose --profile share down
```

컨테이너를 내려도 입력자료와 출력 폴더는 남습니다. 재실행은 같은 결과 폴더를 갱신합니다. 동시에 여러 사람이 독립 분석을 해야 하면 별도 출력 폴더·포트·Compose 프로젝트를 사용하거나 JupyterHub를 구성합니다.

구성 근거: [Docker 읽기 전용 bind mount](https://docs.docker.com/engine/storage/bind-mounts/), [Jupyter 토큰 인증](https://jupyter-server.readthedocs.io/en/latest/operators/security.html).

[처음 안내로 돌아가기](../README.md)
