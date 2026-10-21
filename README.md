# 한국로텍 데이터 분석

검사·생산·도금액·약품·전력 기록을 분석하는 Jupyter Notebook입니다.
현재 배포본은 CPU로 실행하며, GPU는 사용하지 않습니다.

## 바로가기

| 목적 | 링크 |
| --- | --- |
| 노트북 내용 보기 | [한국로텍 데이터 분석 노트북](./한국로텍_데이터분석.ipynb) |
| 노트북 파일 다운로드 | [노트북 다운로드](https://raw.githubusercontent.com/realironn/Hkrotec-Data-Analysis/refs/heads/main/%ED%95%9C%EA%B5%AD%EB%A1%9C%ED%85%8D_%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D.ipynb) |
| 내 Windows PC에서 실행 | [Windows 설치·실행 가이드](./docs/windows-setup.md) |
| 서버에 설치 | [서버 담당자용 준비 안내](./docs/server-setup.md) |
| 브라우저에서 서버 노트북 실행 | **준비 중입니다. 서버 주소가 확정되면 이 항목에 접속 링크를 추가합니다.** |

GitHub의 노트북 화면은 내용을 보는 화면입니다. 코드를 실행하려면 내 PC의 Jupyter 또는 준비된 서버에 접속해야 합니다. [GitHub 노트북 안내](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#working-with-jupyter-notebook-files-on-github)

## 분석 내용

- 날짜별 검사수량과 불량기록 집계
- 대표품목의 전류·전압·온도·처리시간 비교
- 도금액 성분과 약품 사용량의 날짜별 관계 분석
- 월별 약품량과 전력량 비교
- 시간순 예측 검증과 계산표·그래프·보고서 저장

상관관계는 원인이나 권장 작업조건을 뜻하지 않습니다. 품번·LOT 연결과 측정 기준 등 현재 자료의 한계는 노트북에 표시합니다.

## 실행에 필요한 자료

**회사 자료는 공개 저장소에 포함하지 않습니다.** 담당자가 별도로 제공하는 아래 자료를 노트북과 같은 위치에 배치해 주세요.

```text
한국로텍_데이터분석.ipynb
raw/
csv/
prepared/
    한국로텍_분석참고자료.json
```

`raw`, `csv`, `prepared`는 기존 분석 입력자료입니다. `한국로텍_분석참고자료.json`에는 원본 대조에 필요한 이미지 분류표와 기준 문서가 들어 있습니다. 공개용 노트북에서는 이 자료를 파일로 분리했습니다.

**저장소만 다운로드한 상태에서는 실제 분석을 실행할 수 없습니다.** 서버 이용자는 운영자가 위 자료를 배치한 뒤 접속 링크를 받으면 됩니다.

## 실행과 결과 확인

검증한 환경은 **Windows, Python 3.14**입니다. 현재 배포본은 같은 환경을 재현하도록 버전을 확인합니다. Python 3.14가 분석 방법 자체의 필수 조건이라는 뜻은 아닙니다.

1. [Windows 가이드](./docs/windows-setup.md)에 따라 Jupyter를 준비합니다.
2. 노트북을 열고 첫 코드 셀부터 순서대로 실행합니다.
3. `분석결과/한국로텍_분석보고서.html`을 엽니다.

세부 계산표는 `분석결과/tables`, 그래프는 `분석결과/figures`에 저장합니다. 다시 실행하면 같은 결과 폴더를 갱신합니다. 원본 입력자료는 변경하지 않습니다.

서버에서의 이용 방법과 운영체제별 확인사항은 [서버 준비 안내](./docs/server-setup.md)에 정리했습니다.
