# game.py
# ─────────────────────────────────────────────
# 역할: 퀴즈 게임의 기본 데이터, 메뉴, 입력 검증, 문제 출제와 전체 실행 흐름을 관리한다.
# 현재 7단계에서는 등록된 퀴즈 개수와 문제 문구를 번호가 붙은 목록으로 확인할 수 있다.
# 삭제, 최고 점수, 파일 저장 기능은 이후 단계에서 차례로 연결한다.
# ─────────────────────────────────────────────

from quiz import Quiz  # quiz.py 파일에서 퀴즈 한 문제를 표현하는 Quiz 클래스를 가져온다.


class QuizGame:
    """퀴즈 목록을 보관하고 게임 전체의 실행 흐름을 관리하는 클래스."""

    def __init__(self):
        # 역할: QuizGame 객체가 만들어질 때 필요한 초기 상태를 준비한다.
        # 매개변수: self는 지금 만들어지는 QuizGame 객체 자기 자신을 가리킨다.
        # 반환값: __init__은 값을 반환하지 않고 객체의 속성만 준비한다.
        # 현재는 기본 퀴즈 5개로 시작하며, 9단계에서 파일의 데이터를 불러오는 방식으로 교체한다.
        self.quizzes = self.get_default_quizzes()

    def get_default_quizzes(self):
        # 역할: 프로그램을 처음 시작할 때 사용할 기본 퀴즈 5개를 만든다.
        # 매개변수: self는 이 메서드를 호출한 QuizGame 객체를 가리킨다.
        # 반환값: Quiz 객체 5개를 순서대로 담은 리스트를 반환한다.
        # Quiz 클래스에 문제·선택지·정답·힌트를 넘기면 서로 독립된 한 문제 객체가 만들어진다.
        default_quizzes = [
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
        return default_quizzes

    def show_menu(self):
        # 역할: 사용자가 선택할 수 있는 1번부터 6번까지의 메뉴를 화면에 출력한다.
        # 매개변수: self는 이 메서드를 호출한 QuizGame 객체를 가리킨다.
        # 반환값: 화면에 글자를 출력하기만 하므로 반환값은 없다.
        print("========================================")
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 퀴즈 삭제")
        print("5. 점수 확인")
        print("6. 종료")
        print("========================================")

    def get_number_input(self, prompt, min_num, max_num):
        # 역할: 안내문을 보여 주고, 정해진 범위 안의 정수가 입력될 때까지 다시 묻는다.
        # 매개변수: prompt는 입력 안내문, min_num은 최솟값, max_num은 최댓값이다.
        # 반환값: 모든 검증을 통과한 정수 하나를 반환한다.
        # while True는 올바른 입력이 들어오는 횟수를 미리 알 수 없어서 사용하는 무한 반복문이다.
        while True:
            # input()의 결과는 항상 문자열이다. strip()은 앞뒤 공백을 제거한다.
            user_input = input(prompt).strip()

            # 빈 문자열을 먼저 검사하면 int() 변환 전에 알맞은 안내를 따로 보여 줄 수 있다.
            if user_input == "":
                print("⚠️ 아무것도 입력되지 않았습니다. 다시 입력하세요.")
                continue

            try:
                # int()는 숫자 모양의 문자열을 실제 정수로 바꾼다.
                number = int(user_input)
            except ValueError:
                # 숫자로 바꿀 수 없는 문자열이면 프로그램을 끝내지 않고 다시 입력받는다.
                print("⚠️ 숫자를 입력하세요.")
                continue

            # 두 경계 중 하나라도 벗어나면 허용 범위를 안내하고 다시 반복한다.
            if number < min_num or number > max_num:
                # f-string은 중괄호 안의 값을 문자열에 넣어 범위를 동적으로 보여 준다.
                print(f"⚠️ {min_num}~{max_num} 사이의 숫자를 입력하세요.")
                continue

            # 여기까지 왔다는 것은 빈 입력, 변환 실패, 범위 오류를 모두 통과했다는 뜻이다.
            return number

    def get_text_input(self, prompt):
        # 역할: 안내문을 보여 주고, 내용이 있는 문자열이 입력될 때까지 다시 묻는다.
        # 매개변수: prompt는 사용자에게 보여 줄 문자열 입력 안내문이다.
        # 반환값: 앞뒤 공백을 제거했고 빈 문자열이 아닌 글자를 반환한다.
        # 글자 입력도 성공 횟수를 알 수 없으므로 while True로 올바른 입력까지 반복한다.
        while True:
            # strip()으로 공백만 입력한 경우도 빈 입력과 똑같이 처리한다.
            text = input(prompt).strip()

            if text == "":
                print("⚠️ 아무것도 입력되지 않았습니다. 다시 입력하세요.")
                continue

            return text

    def play_quiz(self):
        # 역할: 저장된 퀴즈를 순서대로 출제하고 정답 수와 백분율 점수를 보여 준다.
        # 매개변수: self는 퀴즈 목록을 가진 현재 QuizGame 객체를 가리킨다.
        # 반환값: 화면 출력과 게임 상태 진행만 담당하므로 별도의 값을 반환하지 않는다.
        if not self.quizzes:
            # 빈 리스트는 조건식에서 False이므로 not을 붙여 퀴즈가 없는 상태를 찾는다.
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total_questions = len(self.quizzes)
        correct_count = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total_questions}문제)")

        # for 반복은 출제할 퀴즈 수가 리스트 길이로 정해져 있을 때 알맞다.
        # enumerate는 각 Quiz 객체와 1부터 시작하는 화면용 문제 번호를 함께 꺼낸다.
        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(number)
            answer = self.get_number_input("정답 입력 (1~4): ", 1, 4)

            if quiz.check_answer(answer):
                print("✅ 정답입니다!")
                # 정답인 경우에만 맞힌 수를 1 증가시켜 최종 점수 계산에 사용한다.
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        print("=" * 40)
        # 맞힌 비율에 100을 곱하고 round로 반올림해 문제 수와 무관한 백분율 점수를 만든다.
        score = round(correct_count / total_questions * 100)
        print(
            f"🏆 결과: {total_questions}문제 중 "
            f"{correct_count}문제 정답! ({score}점)"
        )
        # 최고 점수와 비교하는 기능은 8단계에서 추가한다.
        print("=" * 40)

    def add_quiz(self):
        # 역할: 사용자에게 문제, 선택지 4개, 정답 번호를 받아 새 퀴즈를 목록에 추가한다.
        # 매개변수: self는 새 퀴즈를 보관할 현재 QuizGame 객체를 가리킨다.
        # 반환값: self.quizzes를 직접 변경하고 안내를 출력하므로 별도의 값을 반환하지 않는다.
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.get_text_input("문제를 입력하세요: ")

        # 선택지는 여러 개이므로 빈 리스트를 먼저 만들고, 입력받을 때마다 뒤에 붙인다.
        choices = []
        # range(1, 5)는 1, 2, 3, 4를 만들어 선택지를 정확히 네 번 입력받게 한다.
        for i in range(1, 5):
            choice = self.get_text_input(f"선택지 {i}: ")
            # append는 기존 리스트 끝에 새로운 값 하나를 추가한다.
            choices.append(choice)

        answer = self.get_number_input("정답 번호 (1~4): ", 1, 4)

        # 힌트 입력은 11단계에서 추가하므로 지금은 Quiz의 hint 기본값 None을 사용한다.
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        # 파일 저장 연결은 9단계에서 추가하므로 현재는 실행 중인 목록에만 남는다.
        print(f"✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)")

    def show_quiz_list(self):
        # 역할: 등록된 퀴즈의 개수와 각 문제 문구를 번호가 붙은 목록으로 보여 준다.
        # 매개변수: self는 화면에 표시할 퀴즈 목록을 가진 현재 QuizGame 객체를 가리킨다.
        # 반환값: 목록을 출력할 뿐이며, 퀴즈가 없을 때도 안내 후 별도의 값을 반환하지 않는다.
        if not self.quizzes:
            # 빈 목록에서 반복하지 않고 사용자가 이해할 수 있는 안내를 먼저 보여 준다.
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)

        # enumerate는 Quiz 객체와 1부터 시작하는 화면용 목록 번호를 함께 꺼낸다.
        for i, quiz in enumerate(self.quizzes, start=1):
            # 목록에서는 정답이 미리 드러나지 않도록 선택지·정답·힌트는 출력하지 않는다.
            print(f"[{i}] {quiz.question}")

        print("-" * 40)

    def run(self):
        # 역할: 메뉴 표시와 사용자 선택을 반복하고, 종료 입력이나 입력 중단을 안전하게 처리한다.
        # 매개변수: self는 현재 실행 중인 QuizGame 객체를 가리킨다.
        # 반환값: 게임 흐름을 실행하고 끝낼 뿐 별도의 값을 반환하지 않는다.
        # try가 while 전체를 감싸므로 메뉴 표시 중 어느 입력에서 중단되어도 한곳에서 처리할 수 있다.
        try:
            while True:
                self.show_menu()
                choice = self.get_number_input("선택: ", 1, 6)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 6:
                    print("게임을 종료합니다. 안녕히 가세요!")
                    break
                else:
                    # 4~5번의 실제 기능은 이후 단계에서 하나씩 연결한다.
                    print("아직 준비 중인 기능입니다.")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C는 KeyboardInterrupt, 입력 스트림 종료는 EOFError를 일으킨다.
            # 이 두 예외는 번호 입력 메서드가 아닌 전체 실행 흐름에서 한 번에 처리한다.
            print("\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
