# game.py
# ─────────────────────────────────────────────
# 역할: 퀴즈 게임의 메뉴, 입력 검증, 전체 실행 흐름을 관리하는 파일이다.
# 현재 2단계에서는 메뉴 뼈대와 안전한 번호 입력 기능까지만 구현한다.
# 퀴즈 데이터와 실제 메뉴별 기능은 이후 단계에서 차례로 추가한다.
# ─────────────────────────────────────────────


class QuizGame:
    """퀴즈 게임 전체의 상태와 실행 흐름을 관리하는 클래스."""

    def __init__(self):
        # 역할: QuizGame 객체가 만들어질 때 필요한 초기 상태를 준비한다.
        # 매개변수: self는 지금 만들어지는 QuizGame 객체 자기 자신을 가리킨다.
        # 반환값: __init__은 값을 반환하지 않고 객체의 속성만 준비한다.
        # self.quizzes는 여러 퀴즈를 순서대로 담을 리스트이며, 데이터는 다음 단계에서 채운다.
        self.quizzes = []

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

    def run(self):
        # 역할: 메뉴 표시와 사용자 선택을 반복하고, 종료 입력이나 입력 중단을 안전하게 처리한다.
        # 매개변수: self는 현재 실행 중인 QuizGame 객체를 가리킨다.
        # 반환값: 게임 흐름을 실행하고 끝낼 뿐 별도의 값을 반환하지 않는다.
        # try가 while 전체를 감싸므로 메뉴 표시 중 어느 입력에서 중단되어도 한곳에서 처리할 수 있다.
        try:
            while True:
                self.show_menu()
                choice = self.get_number_input("선택: ", 1, 6)

                if choice == 6:
                    print("게임을 종료합니다. 안녕히 가세요!")
                    break

                # 1~5번의 실제 기능은 이후 단계에서 하나씩 연결한다.
                print("아직 준비 중인 기능입니다.")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C는 KeyboardInterrupt, 입력 스트림 종료는 EOFError를 일으킨다.
            # 이 두 예외는 번호 입력 메서드가 아닌 전체 실행 흐름에서 한 번에 처리한다.
            print("\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
