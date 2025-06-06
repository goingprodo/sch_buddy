
# 📅 나의 일정관리 시스템

Gradio 기반으로 제작된 **주간 투두리스트 및 일별 체크리스트 웹 애플리케이션**입니다.  
일정 추가, 삭제, 완료 처리 및 메모 기능까지 한눈에 관리할 수 있는 일정 도우미입니다.


## 🔧 주요 기능

- ✅ **주간 투두리스트**: 요일별 오전/오후/저녁 시간대 별 일정 등록 및 삭제
- 📝 **일별 체크리스트**: 할 일 추가, 완료 처리 및 메모 작성 기능
- 🔍 **과거 일정 조회**: 날짜를 입력하면 해당 날짜의 주간/일별 일정 불러오기
- 💾 **자동 저장**: 일정 추가/변경 시 자동으로 JSON 파일로 저장


## 📁 디렉토리 구조


project/
├── main.py              # 애플리케이션 메인 코드
├── requirements.txt     # 필요한 파이썬 패키지 목록
├── make\_venv.bat        # 가상환경 생성용 배치 파일 (Windows)
├── run\_gpu.bat          # 앱 실행용 배치 파일 (Windows)
└── schedule\_data/       # 주간 및 일별 일정 저장 디렉토리


## 📦 설치 방법

1. Python 3.8 이상 설치
2. 가상환경 생성 및 패키지 설치

```bash
python -m venv venv
venv\Scripts\activate   # (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
````

또는 `make_venv.bat` 실행 (Windows 전용)


## ▶️ 실행 방법

```bash
python main.py
```

앱이 실행되면 자동으로 Gradio 웹 UI가 브라우저에 열립니다.
또는 `run_gpu.bat`를 사용할 수도 있습니다 (Windows 전용).


## 🌐 사용 기술

* [Gradio](https://www.gradio.app/)
* Python 표준 라이브러리 (datetime, os, json 등)
* JSON 기반 일정 저장


## 📜 라이선스

이 프로젝트는 **GNU Affero General Public License v3.0 (AGPL-3.0)** 하에 배포됩니다.

```
Copyright (C) 2025 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```



## ✨ 기여

피드백과 기여는 언제든지 환영입니다.
AGPL 라이선스에 따라, 웹 서버에서 수정된 코드를 운영하는 경우 해당 소스코드 공개가 요구됩니다.



✅ 다양한 AI 프로젝트가 궁금하다면 👉 [gptonline.ai/ko](https://gptonline.ai/ko)

```

---

필요하다면 위 내용을 실제 GitHub에 맞는 마크다운 미리보기로 보여드릴 수도 있습니다. 다른 요청사항이 있으신가요?
```
