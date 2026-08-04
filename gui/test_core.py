"""GUI 핵심 로직이 기존 게임 규칙을 지키는지 확인하는 자동 테스트."""

import json
import tempfile
import unittest
from pathlib import Path

from quiz import Quiz

from gui.core import QuizRepository, QuizSession


class FirstItemsSampler:
    """무작위 결과 대신 앞에서부터 뽑아 테스트 결과를 항상 같게 만든다."""

    @staticmethod
    def sample(items, count):
        return list(items[:count])


class QuizRepositoryTest(unittest.TestCase):
    """JSON 불러오기·저장·추가·삭제·손상 복구를 확인한다."""

    def test_missing_file_starts_with_five_default_quizzes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            repository = QuizRepository(path)

            self.assertEqual(len(repository.quizzes), 5)
            self.assertIsNone(repository.best_score)
            self.assertEqual(repository.history, [])
            self.assertIn("기본 퀴즈", repository.load_notice)

    def test_add_save_reload_and_delete(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            repository = QuizRepository(path)

            new_quiz, saved, error = repository.add_quiz(
                "GUI에서 버튼 클릭을 전달하는 기능은?",
                ["변수", "신호", "반복문", "JSON"],
                2,
                "클릭했다는 소식을 메서드에 전합니다.",
            )
            self.assertTrue(saved, error)
            self.assertEqual(new_quiz.answer, 2)
            self.assertEqual(len(repository.quizzes), 6)

            reloaded = QuizRepository(path)
            self.assertEqual(len(reloaded.quizzes), 6)
            self.assertEqual(reloaded.quizzes[-1].question, new_quiz.question)

            deleted, saved, error = reloaded.delete_quiz(5)
            self.assertTrue(saved, error)
            self.assertEqual(deleted.question, new_quiz.question)
            self.assertEqual(len(reloaded.quizzes), 5)

    def test_damaged_json_recovers_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text("{손상된 JSON", encoding="utf-8")

            repository = QuizRepository(path)

            self.assertEqual(len(repository.quizzes), 5)
            self.assertIsNone(repository.best_score)
            self.assertIn("손상", repository.load_notice)

    def test_saved_json_keeps_korean_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            repository = QuizRepository(path)
            saved, error = repository.save()

            self.assertTrue(saved, error)
            text = path.read_text(encoding="utf-8")
            self.assertIn("파이썬의 창시자는?", text)
            data = json.loads(text)
            self.assertEqual(set(data), {"quizzes", "best_score", "history"})

    def test_blank_choice_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = QuizRepository(Path(directory) / "state.json")

            with self.assertRaises(ValueError):
                repository.add_quiz("문제", ["1", "2", "", "4"], 1, None)


class QuizSessionTest(unittest.TestCase):
    """무작위 선택·힌트 차감·채점·최고 점수·기록 저장을 확인한다."""

    def test_session_calculates_hint_penalty_and_records_result(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = QuizRepository(Path(directory) / "state.json")
            session = QuizSession(repository, 2, sampler=FirstItemsSampler())

            hint, used = session.use_hint()
            self.assertTrue(used)
            self.assertIsNotNone(hint)
            self.assertTrue(session.submit_answer(2)["correct"])
            self.assertTrue(session.advance())

            self.assertFalse(session.submit_answer(1)["correct"])
            self.assertFalse(session.advance())
            summary = session.finish()

            # 2문제 중 1문제 정답은 50점, 힌트 한 번으로 5점이 빠져 45점이다.
            self.assertEqual(summary["score"], 45)
            self.assertEqual(summary["penalty"], 5)
            self.assertTrue(summary["new_best"])
            self.assertEqual(repository.best_score, 45)
            self.assertEqual(len(repository.history), 1)

    def test_missing_hint_does_not_reduce_score(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = QuizRepository(Path(directory) / "state.json")
            repository.quizzes = [Quiz("문제", ["1", "2", "3", "4"], 1, None)]
            session = QuizSession(repository, 1, sampler=FirstItemsSampler())

            hint, used = session.use_hint()

            self.assertIsNone(hint)
            self.assertFalse(used)
            self.assertEqual(session.hints_used, 0)

    def test_count_outside_quiz_range_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = QuizRepository(Path(directory) / "state.json")

            with self.assertRaises(ValueError):
                QuizSession(repository, len(repository.quizzes) + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

