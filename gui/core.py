"""GUI와 터미널에서 공통으로 이해할 수 있는 퀴즈 게임 핵심 로직.

이 파일은 버튼이나 창을 전혀 만들지 않는다. 퀴즈 데이터 저장, 추가, 삭제,
무작위 출제, 힌트 차감, 점수와 기록 계산만 담당한다. 화면 코드와 게임 규칙을
분리하면 디자인을 바꾸더라도 점수 계산과 JSON 구조를 안전하게 유지할 수 있다.
"""

from __future__ import annotations

import datetime
import json
import random
from pathlib import Path
from typing import Any

from quiz import Quiz


# 기존 터미널 게임과 같은 규칙을 상수로 모아 두었다.
HINT_PENALTY = 5
RECENT_HISTORY_COUNT = 5


def create_default_quizzes() -> list[Quiz]:
    """설계도에서 승인된 기본 퀴즈 5개를 새 객체 목록으로 반환한다."""
    return [
        Quiz(
            "파이썬의 창시자는?",
            ["리누스 토르발스", "귀도 반 로섬", "제임스 고슬링", "브렌던 아이크"],
            2,
            "네덜란드 출신입니다.",
        ),
        Quiz(
            "변경 내용을 기록 한 장으로 확정해 저장하는 깃 명령은?",
            ["add", "push", "commit", "clone"],
            3,
            "'확정하다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "파이썬에서 리스트를 만들 때 쓰는 괄호는?",
            ["( )", "[ ]", "{ }", "< >"],
            2,
            "모서리가 각진 대괄호입니다.",
        ),
        Quiz(
            "원격 저장소의 새 변경 사항을 내 컴퓨터로 가져오는 깃 명령은?",
            ["pull", "push", "merge", "init"],
            1,
            "'당겨온다'는 뜻입니다.",
        ),
        Quiz(
            "이 게임이 데이터를 저장할 때 쓰는 파일 형식은?",
            ["TXT", "CSV", "XML", "JSON"],
            4,
            "자바스크립트 객체 표기법의 줄임말입니다.",
        ),
    ]


def validate_quiz_data(data: Any) -> Quiz:
    """JSON의 퀴즈 딕셔너리를 검사하고 안전한 Quiz 객체로 바꾼다.

    매개변수:
        data: JSON에서 읽은 퀴즈 한 문제의 값.
    반환값:
        검사를 통과한 Quiz 객체.
    예외:
        구조가 다르면 TypeError 또는 ValueError를 발생시켜 저장 파일 복구로 이어진다.
    """
    if not isinstance(data, dict):
        raise TypeError("퀴즈 항목은 딕셔너리여야 합니다.")

    question = data.get("question")
    choices = data.get("choices")
    answer = data.get("answer")
    hint = data.get("hint")

    if not isinstance(question, str) or not question.strip():
        raise ValueError("문제 문장이 올바르지 않습니다.")
    if (
        not isinstance(choices, list)
        or len(choices) != 4
        or any(not isinstance(choice, str) or not choice.strip() for choice in choices)
    ):
        raise ValueError("선택지는 내용이 있는 문자열 4개여야 합니다.")
    # bool도 Python 내부에서는 int의 하위 종류이므로 type(...) is int로 정확히 구분한다.
    if type(answer) is not int or not 1 <= answer <= 4:
        raise ValueError("정답 번호는 1~4의 정수여야 합니다.")
    if hint is not None and not isinstance(hint, str):
        raise ValueError("힌트는 문자열 또는 null이어야 합니다.")

    return Quiz(
        question.strip(),
        [choice.strip() for choice in choices],
        answer,
        hint.strip() if isinstance(hint, str) and hint.strip() else None,
    )


def validate_history(history: Any) -> list[dict[str, Any]]:
    """게임 기록 목록의 필수 열쇠와 자료형을 검사해 반환한다."""
    if not isinstance(history, list):
        raise TypeError("history는 리스트여야 합니다.")

    checked: list[dict[str, Any]] = []
    for record in history:
        if not isinstance(record, dict):
            raise TypeError("각 게임 기록은 딕셔너리여야 합니다.")

        date = record.get("date")
        total = record.get("total")
        correct = record.get("correct")
        score = record.get("score")
        if not isinstance(date, str) or not date.strip():
            raise ValueError("기록 날짜가 올바르지 않습니다.")
        if type(total) is not int or total < 1:
            raise ValueError("기록의 문제 수가 올바르지 않습니다.")
        if type(correct) is not int or not 0 <= correct <= total:
            raise ValueError("기록의 정답 수가 올바르지 않습니다.")
        if type(score) is not int or not 0 <= score <= 100:
            raise ValueError("기록의 점수가 올바르지 않습니다.")

        checked.append(
            {"date": date, "total": total, "correct": correct, "score": score}
        )
    return checked


class QuizRepository:
    """퀴즈·최고 점수·게임 기록을 메모리와 JSON 파일에서 관리한다."""

    def __init__(self, state_path: Path | str):
        """저장 경로를 기억하고 파일 또는 기본 데이터로 상태를 초기화한다."""
        self.state_path = Path(state_path)
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.history: list[dict[str, Any]] = []
        self.load_notice = ""
        self.load()

    def _restore_defaults(self, notice: str) -> None:
        """파일이 없거나 손상됐을 때 세 상태를 안전한 기본값으로 되돌린다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.history = []
        self.load_notice = notice

    def load(self) -> None:
        """UTF-8 JSON 파일을 읽고 구조를 검사해 프로그램 상태를 복원한다."""
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise TypeError("최상위 JSON 값은 딕셔너리여야 합니다.")

            quizzes_data = data["quizzes"]
            best_score = data["best_score"]
            if not isinstance(quizzes_data, list):
                raise TypeError("quizzes는 리스트여야 합니다.")
            if best_score is not None and (
                type(best_score) is not int or not 0 <= best_score <= 100
            ):
                raise ValueError("최고 점수가 올바르지 않습니다.")

            self.quizzes = [validate_quiz_data(item) for item in quizzes_data]
            self.best_score = best_score
            self.history = validate_history(data.get("history", []))
            self.load_notice = (
                f"저장된 데이터 · 퀴즈 {len(self.quizzes)}개 · "
                f"기록 {len(self.history)}회"
            )
        except FileNotFoundError:
            self._restore_defaults("저장 파일이 없어 기본 퀴즈 5개로 시작했습니다.")
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            self._restore_defaults("저장 파일이 손상되어 기본 퀴즈로 안전하게 복구했습니다.")

    def save(self) -> tuple[bool, str]:
        """현재 상태를 기존 터미널 게임과 같은 JSON 구조로 저장한다.

        반환값은 (성공 여부, 오류 설명)이다. GUI는 이 결과를 이용해 저장 실패를
        대화상자로 안내할 수 있다.
        """
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True, ""
        except OSError as error:
            return False, f"저장 중 문제가 발생했습니다: {error}"

    def add_quiz(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str | None,
    ) -> tuple[Quiz, bool, str]:
        """입력값을 검사해 퀴즈를 추가하고 즉시 저장한다."""
        new_quiz = validate_quiz_data(
            {
                "question": question,
                "choices": choices,
                "answer": answer,
                "hint": hint,
            }
        )
        self.quizzes.append(new_quiz)
        saved, error = self.save()
        return new_quiz, saved, error

    def delete_quiz(self, index: int) -> tuple[Quiz, bool, str]:
        """0부터 시작하는 위치의 퀴즈를 삭제하고 즉시 저장한다."""
        if not 0 <= index < len(self.quizzes):
            raise IndexError("삭제할 퀴즈 번호가 범위를 벗어났습니다.")
        deleted = self.quizzes.pop(index)
        saved, error = self.save()
        return deleted, saved, error

    def recent_history(self) -> list[dict[str, Any]]:
        """최근 게임 기록 최대 5개를 최신순으로 반환한다."""
        return list(reversed(self.history[-RECENT_HISTORY_COUNT:]))

    def record_game(
        self,
        total: int,
        correct: int,
        score: int,
        played_at: str | None = None,
    ) -> dict[str, Any]:
        """한 판 결과를 기록하고 최고 점수를 갱신한 뒤 저장한다."""
        date = played_at or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        record = {"date": date, "total": total, "correct": correct, "score": score}
        self.history.append(record)

        new_best = self.best_score is None or score > self.best_score
        if new_best:
            self.best_score = score

        saved, error = self.save()
        return {
            "record": record,
            "new_best": new_best,
            "saved": saved,
            "save_error": error,
        }


class QuizSession:
    """현재 진행 중인 퀴즈 한 판의 순서와 점수 상태를 관리한다."""

    def __init__(
        self,
        repository: QuizRepository,
        count: int,
        sampler: Any = None,
    ):
        """전체 퀴즈에서 겹치지 않게 count개를 뽑아 새 게임을 준비한다."""
        if not repository.quizzes:
            raise ValueError("등록된 퀴즈가 없습니다.")
        if type(count) is not int or not 1 <= count <= len(repository.quizzes):
            raise ValueError("문제 수가 올바른 범위를 벗어났습니다.")

        random_source = sampler or random
        self.repository = repository
        self.selected: list[Quiz] = random_source.sample(repository.quizzes, count)
        self.index = 0
        self.correct_count = 0
        self.hints_used = 0
        self.answered = False
        self.completed = False
        self.answer_result: dict[str, Any] | None = None
        self.summary: dict[str, Any] | None = None

    @property
    def total(self) -> int:
        """이번 판에서 풀 문제 수를 반환한다."""
        return len(self.selected)

    @property
    def current_quiz(self) -> Quiz:
        """화면에 표시해야 할 현재 Quiz 객체를 반환한다."""
        return self.selected[self.index]

    def use_hint(self) -> tuple[str | None, bool]:
        """현재 문제의 힌트를 반환하고 실제 힌트가 있으면 사용 횟수를 늘린다."""
        if self.answered:
            raise RuntimeError("이미 답한 문제에서는 힌트를 사용할 수 없습니다.")
        if self.current_quiz.hint is None:
            return None, False
        self.hints_used += 1
        return self.current_quiz.hint, True

    def submit_answer(self, answer: int) -> dict[str, Any]:
        """현재 문제의 답을 한 번만 채점하고 화면에 필요한 결과를 반환한다."""
        if self.answered:
            raise RuntimeError("현재 문제는 이미 채점했습니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4여야 합니다.")

        correct = self.current_quiz.check_answer(answer)
        if correct:
            self.correct_count += 1
        self.answered = True
        self.answer_result = {
            "correct": correct,
            "answer": self.current_quiz.answer,
            "is_last": self.index == self.total - 1,
        }
        return self.answer_result

    def advance(self) -> bool:
        """다음 문제로 이동한다. 마지막 문제였다면 완료 상태로 바꾸고 False를 반환한다."""
        if not self.answered:
            raise RuntimeError("현재 문제에 먼저 답해야 합니다.")
        if self.index == self.total - 1:
            self.completed = True
            return False

        self.index += 1
        self.answered = False
        self.answer_result = None
        return True

    def finish(self) -> dict[str, Any]:
        """최종 점수를 계산하고 기록·최고 점수를 저장해 결과 요약을 반환한다."""
        if self.summary is not None:
            return self.summary
        if not self.completed:
            if self.index == self.total - 1 and self.answered:
                self.completed = True
            else:
                raise RuntimeError("모든 문제를 풀기 전에는 결과를 만들 수 없습니다.")

        score = max(
            0,
            round(self.correct_count / self.total * 100)
            - self.hints_used * HINT_PENALTY,
        )
        saved_result = self.repository.record_game(
            self.total,
            self.correct_count,
            score,
        )
        self.summary = {
            "total": self.total,
            "correct": self.correct_count,
            "hints_used": self.hints_used,
            "penalty": self.hints_used * HINT_PENALTY,
            "score": score,
            **saved_result,
        }
        return self.summary
