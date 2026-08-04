# 🎯 나만의 퀴즈 게임 — GUI 확장판

이 브랜치는 완성된 터미널 퀴즈 게임을 `PySide6` 데스크톱 화면으로 확장한 버전입니다.
과제 원본과 전체 개발 기록은 아래 `main` 브랜치를 기준 문서로 사용합니다.

> **기준 프로젝트:** [터미널 퀴즈 게임 (`main` 브랜치)](https://github.com/Cerhovah/python-quiz-game/tree/main)

![나만의 퀴즈 게임 GUI 홈 화면](docs/screenshots/gui_home.png)

## 바로 실행하기

macOS Intel용 실행본은 [`release/QuizGameGUI-macOS-Intel.zip`](release/QuizGameGUI-macOS-Intel.zip)에 있습니다.

1. ZIP 파일을 내려받아 압축을 풉니다.
2. 압축을 푼 폴더의 `QuizGameGUI.app`을 더블 클릭합니다.
3. 같은 폴더의 `state.json`에 퀴즈와 점수 기록이 저장됩니다.

처음 실행할 때 macOS 보안 경고가 나오면 앱을 우클릭하고 **열기**를 선택합니다.
이 실행본은 별도 개발자 서명을 하지 않은 학습용 앱입니다.

## 소스로 실행하기

Python 3.10 이상이 필요합니다. 프로젝트 루트에서 다음 명령을 순서대로 실행합니다.

```bash
python3 -m venv .gui-venv
source .gui-venv/bin/activate
python -m pip install PySide6
python -m gui.app
```

기존 터미널 버전은 이 브랜치에서도 `python3 main.py`로 실행할 수 있습니다.

## 제공 기능

- 문제 수 선택과 겹치지 않는 무작위 출제
- 선택지 버튼 채점, 힌트 보기와 점수 차감
- 퀴즈 추가·목록·삭제
- 최고 점수와 최근 게임 기록
- UTF-8 `state.json` 저장·불러오기와 손상 복구

## 구조와 문서

- `gui/app.py`: PySide6 창, 화면 구성, 버튼 동작
- `gui/core.py`: 퀴즈 규칙, 점수 계산, JSON 저장
- `gui/test_core.py`: 핵심 로직 자동 테스트
- `gui/test_gui.py`: 실제 위젯 상호작용 자동 테스트
- [`gui/README.md`](gui/README.md): GUI 구현과 학습 포인트 상세 설명
- [`main` 브랜치 README](https://github.com/Cerhovah/python-quiz-game/blob/main/README.md): 터미널 원본의 기능·구조·Git 작업 기록

GUI는 원본 과제의 선택적 확장판입니다. 기능 명세와 제출 기준의 단일 기준 문서는
`main` 브랜치 README이며, 이 문서는 GUI 실행과 유지보수에 필요한 정보만 관리합니다.

## 개발 중 트러블슈팅

### 1. clone 저장소에서 커밋과 pull이 발생하지 않음

- **증상:** clone 폴더에서 커밋했지만 `nothing to commit`, `Everything up-to-date`가 나오고,
  원본 폴더의 `git pull`도 `Already up to date`로 끝났습니다.
- **원인:** clone 폴더의 `README.md` 경로를 터미널에서 직접 실행해 `permission denied`가 발생했고,
  실제 편집과 저장은 이루어지지 않았습니다. 변경 파일이 없으므로 Git도 새 커밋을 만들 수 없었습니다.
- **해결:** VS Code에서 clone 폴더의 README를 실제로 열어 한 줄을 추가하고 저장한 뒤,
  clone 폴더에서 commit·push하고 원본 폴더에서 pull해 `Fast-forward` 반영을 확인했습니다.
- **재발 방지:** 작업 전 `pwd`, 저장 후 `git diff`, 커밋 전 `git status`를 확인해
  현재 위치와 실제 변경 내용을 각각 검증합니다.

### 2. 스크린샷 파일명과 실제 화면 내용이 뒤바뀜

- **증상:** 제출용 PNG 7개가 모두 존재했지만 `env.png`에는 Git 그래프가,
  `menu.png`에는 점수 화면이 들어가는 등 파일명과 내용이 맞지 않았습니다.
- **원인:** 파일 개수와 이름만 확인하고 각 이미지를 직접 열어 내용까지 대조하지 않았습니다.
- **해결:** 7개 이미지를 하나씩 열어 제출 체크리스트와 비교하고 잘못 붙은 이름을 바로잡았습니다.
  개발 환경 화면은 VS Code 프로젝트 탐색기와 터미널의 Python 버전·Git 사용자명이 함께 보이도록 다시 촬영했습니다.
- **재발 방지:** 이미지 산출물은 `파일 존재 여부 → 파일명 → 실제 화면 내용` 순서로 검수하고,
  마지막에 Git 추적 대상이 정확히 7개인지 다시 확인합니다.

### 3. macOS 기본 Python 버전이 GUI 요구사항보다 낮음

- **증상:** 공용 Mac의 기본 `python3`는 3.9.6이어서 Python 3.10 이상을 요구하는 GUI 코드와
  PySide6 실행 환경의 기준을 충족하지 못했습니다.
- **원인:** 운영체제에 기본으로 연결된 Python과 프로젝트에서 사용할 Python을 같은 환경으로 간주했습니다.
- **해결:** Python 3.12.13으로 독립 가상환경을 만들고 그 안에 PySide6와 테스트 도구를 설치했습니다.
  이후 문법 검사와 핵심·GUI 상호작용 테스트를 같은 가상환경에서 실행했습니다.
- **재발 방지:** 개발 시작 시 `python3 --version`과 실제 가상환경의 `python --version`을 모두 확인하고,
  외부 라이브러리는 프로젝트별 가상환경에만 설치합니다.

## 테스트

PySide6가 설치된 가상환경에서 다음 명령으로 핵심 로직과 화면 상호작용을 함께 검사합니다.

```bash
QT_QPA_PLATFORM=offscreen python -m unittest gui.test_core gui.test_gui -v
```
