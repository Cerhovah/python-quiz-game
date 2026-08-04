"""PySide6로 만든 '나만의 퀴즈 게임' 데스크톱 GUI.

기존 터미널 게임의 퀴즈 풀기·추가·목록·삭제·점수·JSON 저장 기능을
버튼과 화면으로 연결한다. 화면은 이 파일이 맡고, 게임 규칙과 데이터 처리는
gui/core.py가 맡는다. 이 역할 분리 덕분에 GUI 문법은 부가 학습으로 떼어 볼 수 있다.
"""

from __future__ import annotations

import argparse
import os
import signal
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QCloseEvent, QFont
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from gui.core import HINT_PENALTY, QuizRepository, QuizSession


APP_TITLE = "나만의 퀴즈 게임"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


APP_STYLE = """
QWidget {
    color: #EAF0FF;
    font-family: "Apple SD Gothic Neo";
    font-size: 14px;
}
QMainWindow, QWidget#appRoot {
    background: #090E1A;
}
QFrame#sidebar {
    background: #0E1527;
    border-right: 1px solid #202C48;
}
QFrame#card, QFrame#heroCard, QFrame#statCard {
    background: #131D33;
    border: 1px solid #263556;
    border-radius: 18px;
}
QFrame#heroCard {
    background: #151F3B;
    border: 1px solid #344A7A;
}
QFrame#statCard {
    background: #111A2D;
}
QLabel#brandTitle {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 800;
}
QLabel#brandCaption, QLabel#muted, QLabel#fieldLabel {
    color: #91A1BF;
}
QLabel#eyebrow {
    color: #8B7CFF;
    font-size: 12px;
    font-weight: 800;
}
QLabel#pageTitle {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 800;
}
QLabel#heroTitle {
    color: #FFFFFF;
    font-size: 31px;
    font-weight: 850;
}
QLabel#sectionTitle {
    color: #F8FAFF;
    font-size: 19px;
    font-weight: 750;
}
QLabel#statValue {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 850;
}
QLabel#questionText {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 750;
}
QLabel#resultScore {
    color: #A99BFF;
    font-size: 64px;
    font-weight: 900;
}
QLabel#successText {
    color: #52E1C3;
    font-weight: 700;
}
QLabel#warningText {
    color: #FFCC66;
    font-weight: 700;
}
QLabel#errorText {
    color: #FF8095;
    font-weight: 700;
}
QPushButton {
    border: none;
    border-radius: 11px;
    padding: 11px 16px;
    font-weight: 700;
}
QPushButton#navButton {
    background: transparent;
    color: #9BABCA;
    text-align: left;
    padding: 13px 16px;
    border-radius: 10px;
}
QPushButton#navButton:hover {
    background: #17233C;
    color: #FFFFFF;
}
QPushButton#navButton[active="true"] {
    background: #6F5CF4;
    color: #FFFFFF;
}
QPushButton#primaryButton {
    background: #7562F5;
    color: #FFFFFF;
}
QPushButton#primaryButton:hover {
    background: #8876FF;
}
QPushButton#primaryButton:disabled {
    background: #3A4260;
    color: #7F8AA5;
}
QPushButton#secondaryButton {
    background: #1C2945;
    color: #C6D2EB;
    border: 1px solid #344563;
}
QPushButton#secondaryButton:hover {
    background: #253654;
    color: #FFFFFF;
}
QPushButton#dangerButton {
    background: #3C2030;
    color: #FF91A3;
    border: 1px solid #653044;
}
QPushButton#dangerButton:hover {
    background: #5A293C;
    color: #FFD2D9;
}
QLineEdit, QSpinBox, QComboBox, QListWidget, QTableWidget {
    background: #0E172A;
    color: #F4F7FF;
    border: 1px solid #30415F;
    border-radius: 10px;
    padding: 10px 12px;
    selection-background-color: #7562F5;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QListWidget:focus {
    border: 1px solid #8B7CFF;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
}
QComboBox QAbstractItemView {
    background: #111A2D;
    color: #F4F7FF;
    selection-background-color: #7562F5;
}
QListWidget {
    padding: 8px;
}
QListWidget::item {
    background: #141F35;
    border: 1px solid #263856;
    border-radius: 10px;
    padding: 14px;
    margin: 4px;
}
QListWidget::item:hover {
    background: #1A2944;
}
QListWidget::item:selected {
    background: #2C2860;
    border: 1px solid #8072FF;
}
QRadioButton {
    background: #111B30;
    border: 1px solid #2B3B5B;
    border-radius: 12px;
    padding: 14px 16px;
    spacing: 12px;
}
QRadioButton:hover {
    background: #172540;
    border: 1px solid #50658D;
}
QRadioButton:checked {
    background: #292653;
    border: 1px solid #887AFF;
    color: #FFFFFF;
}
QRadioButton::indicator {
    width: 17px;
    height: 17px;
}
QProgressBar {
    background: #1A2440;
    border: none;
    border-radius: 5px;
    height: 9px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background: #7562F5;
    border-radius: 5px;
}
QTableWidget {
    gridline-color: #263856;
    padding: 0;
}
QHeaderView::section {
    background: #17223A;
    color: #9EADCA;
    border: none;
    border-bottom: 1px solid #30415F;
    padding: 10px;
    font-weight: 700;
}
QTableWidget::item {
    padding: 10px;
}
QStatusBar {
    background: #0E1527;
    color: #AAB7CF;
    border-top: 1px solid #202C48;
}
QMessageBox {
    background: #111A2D;
}
"""


def add_shadow(widget: QWidget) -> None:
    """카드에 은은한 그림자를 더해 층을 시각적으로 구분한다."""
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(30)
    shadow.setOffset(0, 10)
    shadow.setColor(QColor(0, 0, 0, 95))
    widget.setGraphicsEffect(shadow)


def make_button(text: str, style_name: str = "primaryButton") -> QPushButton:
    """프로젝트에서 같은 크기와 모양을 쓰는 버튼을 만들어 반환한다."""
    button = QPushButton(text)
    button.setObjectName(style_name)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setMinimumHeight(45)
    return button


def make_card(object_name: str = "card") -> tuple[QFrame, QVBoxLayout]:
    """내용을 담을 둥근 카드와 그 카드의 세로 레이아웃을 함께 반환한다."""
    frame = QFrame()
    frame.setObjectName(object_name)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(26, 24, 26, 24)
    layout.setSpacing(14)
    return frame, layout


def make_page_header(eyebrow: str, title: str, description: str) -> QWidget:
    """모든 페이지 위쪽에 같은 형식의 제목 영역을 만든다."""
    header = QWidget()
    layout = QVBoxLayout(header)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(5)

    eyebrow_label = QLabel(eyebrow.upper())
    eyebrow_label.setObjectName("eyebrow")
    title_label = QLabel(title)
    title_label.setObjectName("pageTitle")
    description_label = QLabel(description)
    description_label.setObjectName("muted")
    description_label.setWordWrap(True)

    layout.addWidget(eyebrow_label)
    layout.addWidget(title_label)
    layout.addWidget(description_label)
    return header


def resolve_state_path(argument_path: str | None) -> Path:
    """소스 실행과 패키지 실행 모두에서 사용할 state.json 위치를 정한다."""
    if argument_path:
        return Path(argument_path).expanduser().resolve()

    environment_path = os.environ.get("QUIZ_GUI_STATE_FILE")
    if environment_path:
        return Path(environment_path).expanduser().resolve()

    if getattr(sys, "frozen", False):
        executable = Path(sys.executable).resolve()
        # macOS 앱의 실행 파일은 QuizGameGUI.app/Contents/MacOS 안에 있다.
        # 앱과 같은 폴더의 state.json을 쓰면 압축을 풀고 바로 실행할 수 있다.
        if executable.parent.name == "MacOS":
            return executable.parents[3] / "state.json"
        return executable.parent / "state.json"

    return PROJECT_ROOT / "state.json"


class QuizGameWindow(QMainWindow):
    """왼쪽 메뉴와 여섯 기능 화면을 연결하는 프로그램의 메인 창."""

    PAGE_ORDER = ["home", "play", "add", "list", "delete", "score"]

    def __init__(self, repository: QuizRepository):
        """데이터 저장소를 받아 모든 위젯을 만들고 첫 화면을 표시한다."""
        super().__init__()
        self.repository = repository
        self.session: QuizSession | None = None
        self.nav_buttons: dict[str, QPushButton] = {}
        self.silent_close = False

        self.setWindowTitle(APP_TITLE)
        self.resize(1180, 760)
        self.setMinimumSize(1020, 680)

        self._build_window()
        self._refresh_all()
        self.show_page("home")
        self.statusBar().showMessage(self.repository.load_notice, 9000)

    def _build_window(self) -> None:
        """사이드바와 페이지 전환 영역을 조립해 창의 큰 레이아웃을 만든다."""
        root = QWidget()
        root.setObjectName("appRoot")
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())

        self.pages = QStackedWidget()
        self.pages.addWidget(self._build_home_page())
        self.pages.addWidget(self._build_play_page())
        self.pages.addWidget(self._build_add_page())
        self.pages.addWidget(self._build_list_page())
        self.pages.addWidget(self._build_delete_page())
        self.pages.addWidget(self._build_score_page())
        root_layout.addWidget(self.pages, 1)

        self.setCentralWidget(root)

    def _build_sidebar(self) -> QWidget:
        """브랜드 제목, 기능 이동 버튼, 종료 버튼이 있는 왼쪽 메뉴를 만든다."""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(238)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 28, 20, 22)
        layout.setSpacing(8)

        brand_row = QHBoxLayout()
        brand_mark = QLabel("Q")
        brand_mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_mark.setFixedSize(42, 42)
        brand_mark.setStyleSheet(
            "background:#7562F5;color:white;border-radius:12px;"
            "font-size:20px;font-weight:900;"
        )
        brand_text = QVBoxLayout()
        brand_title = QLabel("QUIZ LAB")
        brand_title.setObjectName("brandTitle")
        brand_caption = QLabel("Python · Git")
        brand_caption.setObjectName("brandCaption")
        brand_text.addWidget(brand_title)
        brand_text.addWidget(brand_caption)
        brand_row.addWidget(brand_mark)
        brand_row.addLayout(brand_text)
        brand_row.addStretch()
        layout.addLayout(brand_row)
        layout.addSpacing(25)

        navigation = [
            ("home", "⌂   홈"),
            ("play", "▶   퀴즈 풀기"),
            ("add", "+   퀴즈 추가"),
            ("list", "☷   퀴즈 목록"),
            ("delete", "−   퀴즈 삭제"),
            ("score", "★   점수 확인"),
        ]
        for page_name, text in navigation:
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.setProperty("active", False)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(46)
            # clicked 신호가 오면 선택한 페이지 이름을 show_page 메서드에 전달한다.
            button.clicked.connect(
                lambda checked=False, name=page_name: self.show_page(name)
            )
            self.nav_buttons[page_name] = button
            layout.addWidget(button)

        layout.addStretch()

        storage_label = QLabel("●  JSON 자동 저장")
        storage_label.setObjectName("successText")
        layout.addWidget(storage_label)

        exit_button = make_button("안전하게 저장하고 종료", "secondaryButton")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)
        return sidebar

    def _new_page(self) -> tuple[QWidget, QVBoxLayout]:
        """일관된 여백을 가진 빈 페이지를 만든다."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(42, 34, 42, 34)
        layout.setSpacing(24)
        return page, layout

    def _build_home_page(self) -> QWidget:
        """게임 소개, 통계 카드와 빠른 시작 버튼이 있는 홈 화면을 만든다."""
        page, layout = self._new_page()

        hero, hero_layout = make_card("heroCard")
        hero_layout.setContentsMargins(34, 32, 34, 32)
        eyebrow = QLabel("PYTHON × GIT LEARNING GAME")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("배운 내용을,\n게임으로 오래 기억하세요.")
        title.setObjectName("heroTitle")
        subtitle = QLabel(
            "문제 수를 선택하고 무작위 퀴즈에 도전하세요. "
            "힌트·점수·최근 기록은 모두 자동으로 저장됩니다."
        )
        subtitle.setObjectName("muted")
        subtitle.setWordWrap(True)
        subtitle.setMaximumWidth(650)
        start_button = make_button("지금 퀴즈 시작하기  →")
        start_button.setMaximumWidth(230)
        start_button.clicked.connect(lambda: self.show_page("play"))
        hero_layout.addWidget(eyebrow)
        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        hero_layout.addSpacing(6)
        hero_layout.addWidget(start_button)
        add_shadow(hero)
        layout.addWidget(hero)

        stats = QHBoxLayout()
        stats.setSpacing(16)
        self.home_quiz_value = self._add_stat_card(stats, "등록된 퀴즈", "0", "문제")
        self.home_best_value = self._add_stat_card(stats, "최고 점수", "—", "BEST")
        self.home_history_value = self._add_stat_card(stats, "완료한 게임", "0", "회")
        layout.addLayout(stats)

        self.home_notice = QLabel()
        self.home_notice.setObjectName("muted")
        self.home_notice.setWordWrap(True)
        layout.addWidget(self.home_notice)
        layout.addStretch()
        return page

    def _add_stat_card(
        self, row: QHBoxLayout, label: str, initial_value: str, badge: str
    ) -> QLabel:
        """홈 화면 통계 카드 하나를 행에 추가하고 값 라벨을 반환한다."""
        card, card_layout = make_card("statCard")
        top = QHBoxLayout()
        caption = QLabel(label)
        caption.setObjectName("muted")
        badge_label = QLabel(badge)
        badge_label.setObjectName("eyebrow")
        top.addWidget(caption)
        top.addStretch()
        top.addWidget(badge_label)
        value = QLabel(initial_value)
        value.setObjectName("statValue")
        card_layout.addLayout(top)
        card_layout.addWidget(value)
        row.addWidget(card)
        return value

    def _build_play_page(self) -> QWidget:
        """문제 수 선택, 문제 풀이, 결과의 세 화면을 가진 퀴즈 페이지를 만든다."""
        page, layout = self._new_page()
        layout.addWidget(
            make_page_header(
                "Play",
                "퀴즈 풀기",
                "문제는 겹치지 않게 무작위로 출제되며 힌트 1회당 5점이 차감됩니다.",
            )
        )

        self.play_flow = QStackedWidget()
        self.play_setup_page = self._build_play_setup()
        self.play_question_page = self._build_play_question()
        self.play_result_page = self._build_play_result()
        self.play_flow.addWidget(self.play_setup_page)
        self.play_flow.addWidget(self.play_question_page)
        self.play_flow.addWidget(self.play_result_page)
        layout.addWidget(self.play_flow, 1)
        return page

    def _build_play_setup(self) -> QWidget:
        """한 판에서 풀 문제 수를 정하는 시작 카드를 만든다."""
        wrapper = QWidget()
        outer = QVBoxLayout(wrapper)
        outer.setContentsMargins(0, 8, 0, 0)
        outer.addStretch()

        card, card_layout = make_card()
        card.setMaximumWidth(620)
        heading = QLabel("몇 문제에 도전할까요?")
        heading.setObjectName("sectionTitle")
        caption = QLabel("현재 등록된 퀴즈 안에서 원하는 문제 수를 선택하세요.")
        caption.setObjectName("muted")
        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMinimumHeight(48)
        self.count_spin.setSuffix(" 문제")
        self.count_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_quiz_button = make_button("무작위 퀴즈 시작")
        self.start_quiz_button.clicked.connect(self.start_quiz)
        card_layout.addWidget(heading)
        card_layout.addWidget(caption)
        card_layout.addWidget(self.count_spin)
        card_layout.addWidget(self.start_quiz_button)
        add_shadow(card)

        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(card)
        row.addStretch()
        outer.addLayout(row)
        outer.addStretch()
        return wrapper

    def _build_play_question(self) -> QWidget:
        """진행률, 문제, 선택지, 힌트와 채점 버튼을 표시하는 화면을 만든다."""
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        top = QHBoxLayout()
        self.play_step = QLabel("문제 1 / 1")
        self.play_step.setObjectName("eyebrow")
        self.play_hint_count = QLabel("힌트 0회")
        self.play_hint_count.setObjectName("muted")
        top.addWidget(self.play_step)
        top.addStretch()
        top.addWidget(self.play_hint_count)
        layout.addLayout(top)

        self.play_progress = QProgressBar()
        self.play_progress.setRange(0, 100)
        self.play_progress.setTextVisible(False)
        layout.addWidget(self.play_progress)

        card, card_layout = make_card()
        self.play_question = QLabel()
        self.play_question.setObjectName("questionText")
        self.play_question.setWordWrap(True)
        card_layout.addWidget(self.play_question)

        self.choice_group = QButtonGroup(self)
        self.choice_buttons: list[QRadioButton] = []
        for number in range(1, 5):
            radio = QRadioButton(f"{number}. 선택지")
            radio.setCursor(Qt.CursorShape.PointingHandCursor)
            radio.setMinimumHeight(52)
            self.choice_group.addButton(radio, number)
            self.choice_buttons.append(radio)
            card_layout.addWidget(radio)

        self.hint_button = make_button("💡  힌트 보기  ·  −5점", "secondaryButton")
        self.hint_button.clicked.connect(self.show_hint)
        self.hint_text = QLabel("")
        self.hint_text.setWordWrap(True)
        self.hint_text.setObjectName("warningText")
        self.feedback_text = QLabel("")
        self.feedback_text.setWordWrap(True)

        actions = QHBoxLayout()
        actions.addWidget(self.hint_button)
        actions.addStretch()
        self.answer_button = make_button("정답 확인")
        self.answer_button.setMinimumWidth(180)
        self.answer_button.clicked.connect(self.handle_answer_button)
        actions.addWidget(self.answer_button)

        card_layout.addWidget(self.hint_text)
        card_layout.addWidget(self.feedback_text)
        card_layout.addLayout(actions)
        layout.addWidget(card)
        return wrapper

    def _build_play_result(self) -> QWidget:
        """한 판이 끝났을 때 점수와 정답 수, 힌트 차감을 보여 주는 화면을 만든다."""
        wrapper = QWidget()
        outer = QVBoxLayout(wrapper)
        outer.setContentsMargins(0, 8, 0, 0)
        outer.addStretch()

        card, card_layout = make_card("heroCard")
        card.setMaximumWidth(700)
        title = QLabel("퀴즈 완료")
        title.setObjectName("eyebrow")
        self.result_score = QLabel("0점")
        self.result_score.setObjectName("resultScore")
        self.result_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_summary = QLabel("")
        self.result_summary.setObjectName("sectionTitle")
        self.result_summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_detail = QLabel("")
        self.result_detail.setObjectName("muted")
        self.result_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_detail.setWordWrap(True)
        self.result_badge = QLabel("")
        self.result_badge.setObjectName("successText")
        self.result_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons = QHBoxLayout()
        again = make_button("다른 문제로 다시 하기")
        again.clicked.connect(self.reset_play_page)
        score_page = make_button("점수 기록 보기", "secondaryButton")
        score_page.clicked.connect(lambda: self.show_page("score"))
        buttons.addWidget(again)
        buttons.addWidget(score_page)

        card_layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.result_score)
        card_layout.addWidget(self.result_summary)
        card_layout.addWidget(self.result_detail)
        card_layout.addWidget(self.result_badge)
        card_layout.addLayout(buttons)
        add_shadow(card)

        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(card)
        row.addStretch()
        outer.addLayout(row)
        outer.addStretch()
        return wrapper

    def _build_add_page(self) -> QWidget:
        """문제·선택지·정답·선택적 힌트를 입력하는 퀴즈 추가 화면을 만든다."""
        page, layout = self._new_page()
        layout.addWidget(
            make_page_header(
                "Create",
                "퀴즈 추가",
                "문제와 선택지 4개는 필수이며, 힌트는 비워 둘 수 있습니다.",
            )
        )

        card, card_layout = make_card()
        question_label = QLabel("문제")
        question_label.setObjectName("fieldLabel")
        self.add_question = QLineEdit()
        self.add_question.setPlaceholderText("예: Python에서 반복할 때 사용하는 문법은?")
        self.add_question.setMinimumHeight(46)
        card_layout.addWidget(question_label)
        card_layout.addWidget(self.add_question)

        choices_title = QLabel("선택지 4개")
        choices_title.setObjectName("fieldLabel")
        card_layout.addWidget(choices_title)
        choice_grid = QGridLayout()
        choice_grid.setHorizontalSpacing(12)
        choice_grid.setVerticalSpacing(10)
        self.add_choices: list[QLineEdit] = []
        for index in range(4):
            field = QLineEdit()
            field.setPlaceholderText(f"선택지 {index + 1}")
            field.setMinimumHeight(44)
            self.add_choices.append(field)
            choice_grid.addWidget(field, index // 2, index % 2)
        card_layout.addLayout(choice_grid)

        bottom = QHBoxLayout()
        answer_column = QVBoxLayout()
        answer_label = QLabel("정답 번호")
        answer_label.setObjectName("fieldLabel")
        self.add_answer = QComboBox()
        self.add_answer.addItems(["1번", "2번", "3번", "4번"])
        self.add_answer.setMinimumHeight(44)
        answer_column.addWidget(answer_label)
        answer_column.addWidget(self.add_answer)

        hint_column = QVBoxLayout()
        hint_label = QLabel("힌트 · 선택")
        hint_label.setObjectName("fieldLabel")
        self.add_hint = QLineEdit()
        self.add_hint.setPlaceholderText("없으면 비워 두세요")
        self.add_hint.setMinimumHeight(44)
        hint_column.addWidget(hint_label)
        hint_column.addWidget(self.add_hint)
        bottom.addLayout(answer_column, 1)
        bottom.addLayout(hint_column, 3)
        card_layout.addLayout(bottom)

        actions = QHBoxLayout()
        self.add_status = QLabel("")
        self.add_status.setWordWrap(True)
        self.add_save_button = make_button("퀴즈 저장")
        self.add_save_button.setMinimumWidth(160)
        self.add_save_button.clicked.connect(self.add_quiz)
        actions.addWidget(self.add_status, 1)
        actions.addWidget(self.add_save_button)
        card_layout.addLayout(actions)
        layout.addWidget(card)
        layout.addStretch()
        return page

    def _build_list_page(self) -> QWidget:
        """정답을 노출하지 않고 등록된 문제 문장만 보여 주는 목록 화면을 만든다."""
        page, layout = self._new_page()
        layout.addWidget(
            make_page_header(
                "Library",
                "퀴즈 목록",
                "학습 전에 정답이 보이지 않도록 문제 문장만 표시합니다.",
            )
        )
        self.list_count = QLabel("")
        self.list_count.setObjectName("eyebrow")
        self.quiz_list = QListWidget()
        self.quiz_list.setSpacing(3)
        layout.addWidget(self.list_count)
        layout.addWidget(self.quiz_list, 1)
        return page

    def _build_delete_page(self) -> QWidget:
        """문제를 고르고 확인 대화상자를 거쳐 삭제하는 안전한 삭제 화면을 만든다."""
        page, layout = self._new_page()
        layout.addWidget(
            make_page_header(
                "Manage",
                "퀴즈 삭제",
                "삭제할 문제를 선택하세요. 실제 삭제 전에는 한 번 더 확인합니다.",
            )
        )
        self.delete_list = QListWidget()
        self.delete_list.setSpacing(3)
        self.delete_list.itemSelectionChanged.connect(self._update_delete_button)
        self.delete_button = make_button("선택한 퀴즈 삭제", "dangerButton")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_quiz)
        layout.addWidget(self.delete_list, 1)
        layout.addWidget(self.delete_button, 0, Qt.AlignmentFlag.AlignRight)
        return page

    def _build_score_page(self) -> QWidget:
        """최고 점수와 최근 게임 기록 최대 5개를 최신순으로 보여 주는 화면을 만든다."""
        page, layout = self._new_page()
        layout.addWidget(
            make_page_header(
                "Progress",
                "점수 확인",
                "최고 점수와 최근 다섯 번의 게임 기록을 확인할 수 있습니다.",
            )
        )

        score_card, score_layout = make_card("heroCard")
        score_row = QHBoxLayout()
        score_texts = QVBoxLayout()
        caption = QLabel("PERSONAL BEST")
        caption.setObjectName("eyebrow")
        self.score_best = QLabel("아직 기록 없음")
        self.score_best.setObjectName("heroTitle")
        score_texts.addWidget(caption)
        score_texts.addWidget(self.score_best)
        score_texts.addWidget(QLabel("퀴즈를 완료하면 최고 점수가 자동으로 갱신됩니다."))
        score_row.addLayout(score_texts)
        score_row.addStretch()
        trophy = QLabel("★")
        trophy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trophy.setFixedSize(72, 72)
        trophy.setStyleSheet(
            "background:#2C2860;color:#B8ADFF;border-radius:20px;"
            "font-size:32px;font-weight:900;"
        )
        score_row.addWidget(trophy)
        score_layout.addLayout(score_row)
        layout.addWidget(score_card)

        history_title = QLabel("최근 게임 기록")
        history_title.setObjectName("sectionTitle")
        layout.addWidget(history_title)
        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(
            ["날짜", "문제 수", "정답", "점수"]
        )
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.history_table.setAlternatingRowColors(False)
        layout.addWidget(self.history_table, 1)
        return page

    def show_page(self, page_name: str) -> None:
        """사이드바에서 고른 이름에 맞는 화면으로 전환하고 데이터를 새로 표시한다."""
        if page_name not in self.PAGE_ORDER:
            raise ValueError(f"알 수 없는 페이지입니다: {page_name}")

        self.pages.setCurrentIndex(self.PAGE_ORDER.index(page_name))
        for name, button in self.nav_buttons.items():
            button.setProperty("active", name == page_name)
            button.style().unpolish(button)
            button.style().polish(button)

        if page_name == "list":
            self.refresh_quiz_lists()
        elif page_name == "delete":
            self.refresh_quiz_lists()
        elif page_name == "score":
            self.refresh_score()
        elif page_name == "play" and self.session is None:
            self.reset_play_page()

    def _refresh_all(self) -> None:
        """데이터 변경 뒤 홈·퀴즈 수·목록·점수 화면을 한 번에 갱신한다."""
        quiz_count = len(self.repository.quizzes)
        self.home_quiz_value.setText(str(quiz_count))
        self.home_best_value.setText(
            "—" if self.repository.best_score is None else f"{self.repository.best_score}점"
        )
        self.home_history_value.setText(str(len(self.repository.history)))
        self.home_notice.setText(f"●  {self.repository.load_notice}")

        self.count_spin.setMaximum(max(1, quiz_count))
        self.count_spin.setValue(min(max(1, self.count_spin.value()), max(1, quiz_count)))
        self.count_spin.setEnabled(quiz_count > 0)
        self.refresh_quiz_lists()
        self.refresh_score()

    def reset_play_page(self) -> None:
        """진행 중 게임을 지우고 문제 수 선택 화면으로 돌아간다."""
        self.session = None
        quiz_count = len(self.repository.quizzes)
        self.count_spin.setMaximum(max(1, quiz_count))
        self.count_spin.setEnabled(quiz_count > 0)
        self.play_flow.setCurrentWidget(self.play_setup_page)

    def start_quiz(self) -> None:
        """선택한 문제 수로 무작위 세션을 만들고 첫 문제를 표시한다."""
        if not self.repository.quizzes:
            QMessageBox.information(
                self,
                "등록된 퀴즈 없음",
                "등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.",
            )
            return
        self.session = QuizSession(self.repository, self.count_spin.value())
        self.play_flow.setCurrentWidget(self.play_question_page)
        self.render_question()

    def render_question(self) -> None:
        """현재 세션의 문제와 선택지를 위젯에 채우고 입력 상태를 초기화한다."""
        if self.session is None:
            return

        quiz = self.session.current_quiz
        self.play_step.setText(
            f"문제 {self.session.index + 1} / {self.session.total}"
        )
        self.play_progress.setValue(
            round((self.session.index + 1) / self.session.total * 100)
        )
        self.play_question.setText(quiz.question)
        self.play_hint_count.setText(f"힌트 {self.session.hints_used}회")

        # 선택 그룹의 독점 상태를 잠시 풀어야 이전 라디오 선택을 모두 해제할 수 있다.
        self.choice_group.setExclusive(False)
        for number, (radio, choice) in enumerate(
            zip(self.choice_buttons, quiz.choices), start=1
        ):
            radio.setText(f"{number}.  {choice}")
            radio.setChecked(False)
            radio.setEnabled(True)
        self.choice_group.setExclusive(True)

        self.hint_button.setEnabled(True)
        self.hint_button.setText("💡  힌트 보기  ·  −5점")
        self.hint_text.clear()
        self.feedback_text.clear()
        self.feedback_text.setObjectName("muted")
        self.answer_button.setText("정답 확인")
        self.answer_button.setProperty("mode", "answer")

    def show_hint(self) -> None:
        """힌트 버튼 클릭을 세션 로직에 전달하고 차감 횟수를 즉시 표시한다."""
        if self.session is None:
            return
        hint, used = self.session.use_hint()
        if used:
            self.hint_text.setText(f"💡 {hint}")
            self.play_hint_count.setText(f"힌트 {self.session.hints_used}회")
            self.hint_button.setText("💡  힌트 다시 보기  ·  추가 −5점")
        else:
            self.hint_text.setText("💡 이 문제에는 힌트가 없습니다.")

    def handle_answer_button(self) -> None:
        """버튼의 현재 상태에 따라 채점, 다음 문제, 결과 표시 중 하나를 수행한다."""
        if self.session is None:
            return

        mode = self.answer_button.property("mode")
        if mode == "answer":
            selected_number = self.choice_group.checkedId()
            if selected_number == -1:
                self.feedback_text.setObjectName("warningText")
                self.feedback_text.setText("⚠️ 선택지를 하나 골라 주세요.")
                self.feedback_text.style().unpolish(self.feedback_text)
                self.feedback_text.style().polish(self.feedback_text)
                return

            result = self.session.submit_answer(selected_number)
            for radio in self.choice_buttons:
                radio.setEnabled(False)
            self.hint_button.setEnabled(False)

            if result["correct"]:
                self.feedback_text.setObjectName("successText")
                self.feedback_text.setText("✓ 정답입니다! 멋진 선택이에요.")
            else:
                self.feedback_text.setObjectName("errorText")
                self.feedback_text.setText(
                    f"정답은 {result['answer']}번입니다. 다음 문제에서 만회해 보세요."
                )
            self.feedback_text.style().unpolish(self.feedback_text)
            self.feedback_text.style().polish(self.feedback_text)

            if result["is_last"]:
                self.answer_button.setText("결과 확인")
                self.answer_button.setProperty("mode", "result")
            else:
                self.answer_button.setText("다음 문제  →")
                self.answer_button.setProperty("mode", "next")
            return

        if mode == "next":
            self.session.advance()
            self.render_question()
            return

        if mode == "result":
            self.session.advance()
            self.show_quiz_result()

    def show_quiz_result(self) -> None:
        """세션을 마감해 점수와 기록을 저장하고 결과 카드를 채운다."""
        if self.session is None:
            return
        summary = self.session.finish()
        self.result_score.setText(f"{summary['score']}점")
        self.result_summary.setText(
            f"{summary['total']}문제 중 {summary['correct']}문제 정답"
        )
        self.result_detail.setText(
            f"힌트 {summary['hints_used']}회 · {summary['penalty']}점 차감 · "
            "게임 기록 자동 저장"
        )
        self.result_badge.setText(
            "★ 새로운 최고 점수입니다!" if summary["new_best"] else "도전 기록을 저장했습니다."
        )
        if not summary["saved"]:
            self.result_badge.setObjectName("errorText")
            self.result_badge.setText(summary["save_error"])
        else:
            self.result_badge.setObjectName("successText")
        self.result_badge.style().unpolish(self.result_badge)
        self.result_badge.style().polish(self.result_badge)
        self.play_flow.setCurrentWidget(self.play_result_page)
        self._refresh_all()

    def add_quiz(self) -> None:
        """입력 위젯 값을 검사해 새 Quiz 객체로 저장하고 입력칸을 비운다."""
        question = self.add_question.text().strip()
        choices = [field.text().strip() for field in self.add_choices]
        answer = self.add_answer.currentIndex() + 1
        hint_text = self.add_hint.text().strip()
        hint = hint_text or None

        if not question or any(not choice for choice in choices):
            self.add_status.setObjectName("errorText")
            self.add_status.setText("문제와 선택지 4개를 모두 입력해 주세요.")
            self.add_status.style().unpolish(self.add_status)
            self.add_status.style().polish(self.add_status)
            return

        try:
            _, saved, error = self.repository.add_quiz(
                question, choices, answer, hint
            )
        except (TypeError, ValueError) as validation_error:
            self.add_status.setObjectName("errorText")
            self.add_status.setText(str(validation_error))
            self.add_status.style().unpolish(self.add_status)
            self.add_status.style().polish(self.add_status)
            return

        if not saved:
            self.add_status.setObjectName("errorText")
            self.add_status.setText(error)
        else:
            self.add_status.setObjectName("successText")
            self.add_status.setText(
                f"✓ 저장 완료 · 현재 퀴즈 {len(self.repository.quizzes)}개"
            )
            self.add_question.clear()
            for field in self.add_choices:
                field.clear()
            self.add_answer.setCurrentIndex(0)
            self.add_hint.clear()
        self.add_status.style().unpolish(self.add_status)
        self.add_status.style().polish(self.add_status)
        self._refresh_all()

    def refresh_quiz_lists(self) -> None:
        """퀴즈 목록 화면과 삭제 선택 화면을 현재 데이터로 다시 채운다."""
        self.quiz_list.clear()
        self.delete_list.clear()
        self.list_count.setText(f"TOTAL · {len(self.repository.quizzes)} QUESTIONS")

        for number, quiz in enumerate(self.repository.quizzes, start=1):
            text = f"{number:02d}   {quiz.question}"
            self.quiz_list.addItem(QListWidgetItem(text))
            self.delete_list.addItem(QListWidgetItem(text))

        if not self.repository.quizzes:
            empty = QListWidgetItem("등록된 퀴즈가 없습니다. 퀴즈 추가 화면을 이용하세요.")
            empty.setFlags(Qt.ItemFlag.NoItemFlags)
            self.quiz_list.addItem(empty)
            delete_empty = QListWidgetItem("삭제할 퀴즈가 없습니다.")
            delete_empty.setFlags(Qt.ItemFlag.NoItemFlags)
            self.delete_list.addItem(delete_empty)
        self._update_delete_button()

    def _update_delete_button(self) -> None:
        """삭제 목록에서 실제 문제를 골랐을 때만 삭제 버튼을 활성화한다."""
        row = self.delete_list.currentRow()
        self.delete_button.setEnabled(0 <= row < len(self.repository.quizzes))

    def delete_quiz(self) -> None:
        """선택한 문제를 대화상자로 확인한 뒤 삭제하고 JSON에 반영한다."""
        row = self.delete_list.currentRow()
        if not 0 <= row < len(self.repository.quizzes):
            return

        target = self.repository.quizzes[row]
        answer = QMessageBox.question(
            self,
            "퀴즈 삭제 확인",
            f"다음 퀴즈를 정말 삭제할까요?\n\n{target.question}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            self.statusBar().showMessage("삭제를 취소했습니다.", 4000)
            return

        _, saved, error = self.repository.delete_quiz(row)
        if saved:
            self.statusBar().showMessage("퀴즈를 삭제하고 저장했습니다.", 5000)
        else:
            QMessageBox.warning(self, "저장 실패", error)
        self.reset_play_page()
        self._refresh_all()

    def refresh_score(self) -> None:
        """최고 점수와 최근 기록 표를 현재 저장소 상태에 맞게 갱신한다."""
        if self.repository.best_score is None:
            self.score_best.setText("아직 기록 없음")
        else:
            self.score_best.setText(f"{self.repository.best_score}점")

        records = self.repository.recent_history()
        self.history_table.setRowCount(len(records))
        for row, record in enumerate(records):
            values = [
                record["date"],
                f"{record['total']}문제",
                f"{record['correct']}개",
                f"{record['score']}점",
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column > 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, column, item)

        self.history_table.setColumnWidth(0, 200)
        self.history_table.setColumnWidth(1, 120)
        self.history_table.setColumnWidth(2, 120)

    def closeEvent(self, event: QCloseEvent) -> None:
        """종료 버튼·창 닫기·Ctrl+C 모두에서 최신 상태를 저장하고 창을 닫는다."""
        saved, error = self.repository.save()
        if not saved and not self.silent_close:
            QMessageBox.warning(self, "저장 실패", error)
        event.accept()


def parse_arguments() -> argparse.Namespace:
    """일반 실행과 자동 GUI 검수에 사용할 선택 인자를 읽는다."""
    parser = argparse.ArgumentParser(description="나만의 퀴즈 게임 GUI")
    parser.add_argument("--state-file", help="시험용 state.json 경로")
    parser.add_argument("--smoke-test", action="store_true", help="창 생성 자동 시험")
    parser.add_argument("--screenshot", help="GUI 화면을 지정한 PNG로 저장")
    # Finder가 앱 실행 시 추가할 수 있는 macOS 전용 인자는 무시한다.
    arguments, _unknown = parser.parse_known_args()
    return arguments


def main() -> int:
    """QApplication과 메인 창을 만들고 GUI 이벤트 반복을 시작한다."""
    arguments = parse_arguments()
    application = QApplication(sys.argv)
    application.setApplicationName(APP_TITLE)
    application.setOrganizationName("Quiz Lab")
    application.setStyle("Fusion")
    application.setFont(QFont("Apple SD Gothic Neo", 13))
    application.setStyleSheet(APP_STYLE)

    repository = QuizRepository(resolve_state_path(arguments.state_file))
    window = QuizGameWindow(repository)
    window.show()

    # Qt가 실행 중일 때도 Python이 Ctrl+C 신호를 확인하도록 짧은 타이머를 둔다.
    signal.signal(signal.SIGINT, lambda *_args: window.close())
    signal_timer = QTimer(window)
    signal_timer.timeout.connect(lambda: None)
    signal_timer.start(400)

    if arguments.screenshot:
        screenshot_path = Path(arguments.screenshot).expanduser().resolve()

        def capture_window() -> None:
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            saved = window.grab().save(str(screenshot_path), "PNG")
            print(f"GUI screenshot: {'PASS' if saved else 'FAIL'} · {screenshot_path}")
            window.silent_close = True
            window.close()

        QTimer.singleShot(500, capture_window)
    elif arguments.smoke_test:

        def run_smoke_test() -> None:
            # 모든 페이지를 한 번씩 전환해 위젯 조립 오류가 없는지 확인한다.
            for page_name in QuizGameWindow.PAGE_ORDER:
                window.show_page(page_name)
                application.processEvents()
            print("GUI smoke test: PASS")
            window.silent_close = True
            window.close()

        QTimer.singleShot(250, run_smoke_test)

    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
