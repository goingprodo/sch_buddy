다음은 사용자가 제공한 코드 기반의 프로젝트에 대한 `README.md` 초안입니다. 이 문서는 프로젝트의 기능, 설치 방법, 실행 방법 등을 포함하고 있습니다.

> 📢 다양한 프로젝트를 위한 AI 도우미, [gptonline.ai/ko](https://gptonline.ai/ko/)도 확인해보세요!

---

```markdown
# 📅 나의 일정관리 시스템

Gradio 기반으로 제작된 **주간 투두리스트 및 일별 체크리스트 웹 애플리케이션**입니다.  
일정 추가, 삭제, 완료 처리 및 메모 기능까지 한눈에 관리할 수 있는 일정 도우미입니다.

---

## 🔧 주요 기능

- ✅ **주간 투두리스트**: 요일별 오전/오후/저녁 시간대 별 일정 등록 및 삭제
- 📝 **일별 체크리스트**: 할 일 추가, 완료 처리 및 메모 작성 기능
- 🔍 **과거 일정 조회**: 날짜를 입력하면 해당 날짜의 주간/일별 일정 불러오기
- 💾 **자동 저장**: 일정 추가/변경 시 자동으로 JSON 파일로 저장

---

## 📁 디렉토리 구조

```

project/
├── main.py              # 애플리케이션 메인 코드
├── requirements.txt     # 필요한 파이썬 패키지 목록
├── make\_venv.bat        # 가상환경 생성용 배치 파일 (Windows)
├── run\_gpu.bat          # 앱 실행용 배치 파일 (Windows)
└── schedule\_data/       # 주간 및 일별 일정 저장 디렉토리

````

---

## 📦 설치 방법

1. Python 3.8 이상 설치
2. 가상환경 생성 및 패키지 설치

```bash
python -m venv venv
venv\Scripts\activate   # (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
````

또는 `make_venv.bat` 실행 (Windows 전용)

---

## ▶️ 실행 방법

```bash
python main.py
```

앱이 실행되면 자동으로 Gradio 웹 UI가 브라우저에 열립니다.
또는 `run_gpu.bat`를 사용할 수도 있습니다 (Windows 전용).

---

## 🌐 사용 기술

* [Gradio](https://www.gradio.app/) - 웹 UI 구축
* Python 표준 라이브러리 (datetime, os, json 등)
* JSON 기반의 일정 저장 및 불러오기

---

## 📌 주의사항

* 일정은 `schedule_data/week`와 `schedule_data/day` 하위 폴더에 JSON 파일로 저장됩니다.
* 날짜 형식은 반드시 `YYYY-MM-DD` 형태를 따라야 합니다.

---

## 📎 미리보기

> 웹 UI는 다음과 같은 탭으로 구성됩니다:

* 📊 주간 투두리스트
* 📋 일별 체크리스트
* 📂 데이터 조회

---

## ✨ 기여

피드백 및 기능 제안은 언제든 환영입니다!
이 프로젝트는 개인 일정관리 도구로 개발되었으며, 오픈소스로 자유롭게 확장 가능합니다.

---

✅ 더 많은 인공지능 앱을 보고 싶다면 👉 [https://gptonline.ai/ko/](https://gptonline.ai/ko/)

```

---

필요하시면 마크다운 형태 대신 HTML이나 PDF 형식으로도 변환해드릴 수 있습니다. 추가 요청 사항 있으신가요?
```
