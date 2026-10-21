# Windows에서 노트북 실행하기

처음 한 번 설치한 뒤에는 노트북을 열어 순서대로 실행하시면 됩니다.
**회사 자료와 비공개 분석참고자료는 담당자에게 별도로 받아야 합니다.**

## 1. 저장소 다운로드

1. [저장소 첫 화면](https://github.com/realironn/Hkrotec-Data-Analysis)에서 초록색 **Code** 버튼을 누릅니다.
2. **Download ZIP**을 누릅니다.
3. 내려받은 ZIP을 모두 압축 해제합니다. ZIP 안에서 바로 실행하지 않습니다.

## 2. 자료 배치

압축을 푼 폴더 안에 기존 `raw`, `csv`, `prepared` 폴더를 넣습니다.
별도로 받은 `한국로텍_분석참고자료.json`은 `prepared` 폴더 안에 넣습니다.

```text
Hkrotec-Data-Analysis-main/
    README.md
    requirements.txt
    한국로텍_데이터분석.ipynb
    raw/
    csv/
    prepared/
        한국로텍_분석참고자료.json
```

기존에 받은 나머지 자료 폴더가 함께 있어도 실행할 수 있습니다. 같은 파일을 중복 집계하지 않습니다.

## 3. Python 3.14 준비

1. [Python 공식 다운로드 페이지](https://www.python.org/downloads/)에서 Windows용 Python Install Manager를 설치합니다.
2. Windows 시작 메뉴에서 **PowerShell**을 엽니다.
3. 다음 명령을 실행합니다.

```powershell
py install 3.14
py -3.14 --version
```

`Python 3.14.x`가 나오면 준비되었습니다. 이미 3.14를 사용 중이면 설치는 건너뜁니다.
기존 Python Launcher를 사용하는 PC에서는 `py install` 명령이 없을 수 있습니다. 이 경우 Python 3.14 설치 프로그램으로 설치한 뒤 버전을 확인합니다.

공식 설치 설명: [Windows에서 Python 사용하기](https://docs.python.org/3.14/using/windows.html)

## 4. 실행 환경 만들기

1. 파일 탐색기에서 **노트북과 requirements.txt가 있는 폴더**를 엽니다.
2. 탐색기 주소창에 `powershell`을 입력하고 Enter를 누릅니다.
3. 아래 명령을 한 줄씩 복사해 실행합니다.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m notebook "한국로텍_데이터분석.ipynb"
```

첫 설치에는 인터넷이 필요합니다. 설치가 끝날 때까지 기다려 주세요.
위 명령은 실행 환경을 활성화하지 않고 Python 경로를 직접 사용하므로 PowerShell 실행 정책을 바꾸지 않아도 됩니다.

공식 Jupyter 설치 설명: [Installing Jupyter](https://jupyter.org/install)

## 5. 노트북 실행

1. 브라우저에서 노트북이 열리면 **Python 3 (ipykernel)**을 선택합니다.
2. 상단의 **Run → Run All Cells**를 누릅니다. 각 코드 셀의 ▶ 버튼을 위에서부터 순서대로 눌러도 됩니다.
3. 첫 코드 셀은 필요한 라이브러리를 확인하고 설치합니다. 이미 설치된 항목은 다시 설치하지 않습니다.
4. 마지막 셀에 **분석 완료**가 표시되면 결과를 확인합니다.

커널 재시작 안내가 나오면 재시작한 뒤 처음부터 실행합니다. 실행 중에는 PowerShell 창을 닫지 않습니다.

## 6. 결과 확인과 다음 실행

파일 탐색기에서 `분석결과/한국로텍_분석보고서.html`을 엽니다.

| 결과 | 위치 |
| --- | --- |
| 분석 보고서 | `분석결과/한국로텍_분석보고서.html` |
| 세부 계산표 | `분석결과/tables` |
| 그래프 | `분석결과/figures` |

다음부터는 같은 폴더에서 아래 명령만 실행하면 됩니다.

```powershell
.\.venv\Scripts\python.exe -m notebook "한국로텍_데이터분석.ipynb"
```

이전 결과를 남겨야 한다면 다시 실행하기 전에 `분석결과` 폴더를 복사합니다.
사용을 마칠 때는 노트북을 저장하고 PowerShell에서 **Ctrl+C**를 누릅니다.

## 오류가 날 때

| 화면에 보이는 내용 | 확인할 사항 |
| --- | --- |
| `py` 명령을 찾을 수 없음 | Python 설치를 마친 뒤 PowerShell을 새로 엽니다. |
| Python 3.14 환경을 선택하라는 안내 | 가상환경을 3.14로 만들었는지 확인합니다. |
| raw·csv·prepared 폴더를 찾을 수 없음 | 세 폴더와 노트북을 같은 위치에 둡니다. |
| 분석참고자료 파일이 없음 | 별도로 받은 JSON을 `prepared` 안에 넣습니다. |
| 원본이 검토 기준과 다름 | 입력자료를 임의로 바꾸지 말고 파일명과 오류 내용을 분석 담당자에게 전달합니다. |
| 브라우저가 자동으로 열리지 않음 | PowerShell에 표시된 Jupyter 주소를 같은 PC의 브라우저에서 엽니다. |
| 설치 오류 | 인터넷 연결을 확인하고 설치 명령을 다시 실행합니다. |
