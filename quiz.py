# quiz.py
# ─────────────────────────────────────────────
# 역할: 퀴즈 한 문제의 데이터와 동작을 표현하는 Quiz 클래스를 담는 파일이다.
# 문제 하나가 가져야 할 문제 문장, 선택지, 정답 번호, 힌트를 한 객체로 묶는다.
# 게임 전체 흐름과 퀴즈 한 문제의 규칙을 분리하면 각 역할을 이해하고 수정하기 쉬워진다.
# ─────────────────────────────────────────────


class Quiz:
    """문제, 선택지 4개, 정답 번호, 힌트를 한데 묶어 관리하는 클래스."""

    def __init__(self, question, choices, answer, hint=None):
        # 역할: Quiz 객체가 만들어질 때 한 문제에 필요한 네 가지 속성을 저장한다.
        # 매개변수: question은 문제 문자열, choices는 선택지 문자열 4개가 든 리스트,
        # answer는 정답 번호 정수, hint는 힌트 문자열 또는 None이다.
        # 반환값: __init__은 값을 반환하지 않고 새 객체의 속성을 준비한다.
        # self는 지금 만들어지는 Quiz 객체 자기 자신을 가리킨다.
        # hint=None은 힌트를 전달하지 않아도 퀴즈를 만들 수 있게 하는 기본값이다.
        self.question = question  # 문제 내용 (문자열, str)
        self.choices = choices  # 선택지 4개 (문자열을 담은 리스트, list)
        self.answer = answer  # 정답 번호 1~4 (정수, int)
        self.hint = hint  # 힌트 내용 (문자열 또는 값이 없음을 뜻하는 None)

    def display(self, number=None):
        # 역할: 문제 번호, 문제 문장, 선택지 4개를 보기 좋은 형식으로 출력한다.
        # 매개변수: number는 화면에 표시할 문제 순번이며, 생략하면 기본값 None이 된다.
        # 반환값: 화면에 내용을 출력하기만 하므로 별도의 값을 반환하지 않는다.
        if number is not None:
            # f-string은 중괄호 안의 number 값을 문자열에 끼워 넣는다.
            print(f"[문제 {number}]")

        print(self.question)
        print()

        # enumerate는 리스트의 각 값과 순번을 함께 꺼낸다.
        # start=1을 지정해 파이썬의 기본 순번 0 대신 사용자에게 익숙한 1부터 표시한다.
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

        print()

    def check_answer(self, user_answer):
        # 역할: 사용자가 입력한 번호와 이 퀴즈의 정답 번호가 같은지 확인한다.
        # 매개변수: user_answer는 사용자가 선택한 정답 번호 정수다.
        # 반환값: 두 번호가 같으면 True, 다르면 False인 불리언(bool)을 반환한다.
        return user_answer == self.answer

    def to_dict(self):
        # 역할: Quiz 객체의 네 속성을 JSON 저장에 알맞은 딕셔너리로 변환한다.
        # 매개변수: self는 변환할 현재 Quiz 객체를 가리킨다.
        # 반환값: question, choices, answer, hint 열쇠를 가진 딕셔너리를 반환한다.
        # JSON은 객체를 직접 저장할 수 없으므로 기본 자료형인 딕셔너리로 바꾸는 과정이 필요하다.
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        # 역할: JSON에서 읽은 딕셔너리를 다시 Quiz 객체로 변환한다.
        # 매개변수: cls는 Quiz 클래스 자체, data는 퀴즈 정보가 든 딕셔너리다.
        # 반환값: data의 값을 사용해 새로 만든 Quiz 객체를 반환한다.
        # @classmethod를 붙이면 아직 객체가 없어도 Quiz.from_dict(딕셔너리) 형태로 호출할 수 있다.
        # data.get("hint")는 hint 열쇠가 없어도 KeyError 대신 None을 주어 옛 데이터도 읽게 한다.
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint"),
        )


if __name__ == "__main__":
    # 이 파일을 python3 quiz.py로 직접 실행했을 때만 아래 자체 시험이 동작한다.
    # 다른 파일이 Quiz 클래스를 import할 때는 시험 코드가 자동으로 실행되지 않는다.
    sample = Quiz(
        "파이썬의 창시자는?",
        ["리누스 토르발스", "귀도 반 로섬", "제임스 고슬링", "브렌던 아이크"],
        2,
        "네덜란드 출신입니다.",
    )
    sample.display(1)
    print("2를 골랐을 때 →", sample.check_answer(2))
    print("딕셔너리 변환 →", sample.to_dict())
