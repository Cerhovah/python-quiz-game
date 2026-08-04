"""실제 PySide6 위젯의 클릭 신호가 기능 메서드에 연결됐는지 확인하는 테스트."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QMessageBox

from gui.app import APP_STYLE, QuizGameWindow
from gui.core import QuizRepository


class QuizGuiInteractionTest(unittest.TestCase):
    """화면을 직접 표시하지 않는 상태에서 버튼 클릭 흐름을 자동 조작한다."""

    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])
        cls.application.setStyle("Fusion")
        cls.application.setStyleSheet(APP_STYLE)

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        state_path = Path(self.temp_directory.name) / "state.json"
        self.repository = QuizRepository(state_path)
        self.window = QuizGameWindow(self.repository)
        self.window.silent_close = True
        self.window.show()
        self.application.processEvents()

    def tearDown(self):
        self.window.close()
        self.application.processEvents()
        self.temp_directory.cleanup()

    def test_navigation_button_changes_page(self):
        self.window.nav_buttons["add"].click()
        self.application.processEvents()

        self.assertEqual(self.window.pages.currentIndex(), 2)

    def test_hint_answer_and_result_buttons_complete_game(self):
        self.window.nav_buttons["play"].click()
        self.window.count_spin.setValue(1)
        self.window.start_quiz_button.click()
        self.application.processEvents()

        session = self.window.session
        self.assertIsNotNone(session)
        correct_answer = session.current_quiz.answer

        self.window.hint_button.click()
        self.window.choice_buttons[correct_answer - 1].setChecked(True)
        self.window.answer_button.click()
        self.window.answer_button.click()
        self.application.processEvents()

        self.assertEqual(len(self.repository.history), 1)
        self.assertEqual(self.repository.history[0]["score"], 95)
        self.assertEqual(
            self.window.play_flow.currentWidget(), self.window.play_result_page
        )

    def test_add_button_saves_new_quiz(self):
        self.window.nav_buttons["add"].click()
        self.window.add_question.setText("GUI의 화면 부품을 무엇이라고 할까요?")
        for field, value in zip(
            self.window.add_choices,
            ["위젯", "브랜치", "딕셔너리", "커밋"],
        ):
            field.setText(value)
        self.window.add_answer.setCurrentIndex(0)
        self.window.add_hint.setText("버튼과 입력칸을 함께 부르는 말입니다.")

        self.window.add_save_button.click()
        self.application.processEvents()

        self.assertEqual(len(self.repository.quizzes), 6)
        self.assertTrue(self.repository.state_path.exists())
        self.assertIn("저장 완료", self.window.add_status.text())

    def test_delete_button_uses_confirmation_and_saves(self):
        self.window.nav_buttons["delete"].click()
        self.window.delete_list.setCurrentRow(0)
        self.application.processEvents()

        with patch.object(
            QMessageBox,
            "question",
            return_value=QMessageBox.StandardButton.Yes,
        ):
            self.window.delete_button.click()
        self.application.processEvents()

        self.assertEqual(len(self.repository.quizzes), 4)
        self.assertTrue(self.repository.state_path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
