import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.quizzes = []
        self.best_score = None

    def show_menu(self):
        print("\n" + "=" * 30)
        print("       파이썬 기초 퀴즈 게임")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def _read_int(self, prompt, min_value, max_value):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print("입력이 비어 있습니다. 다시 입력해 주세요.")
                continue
            try:
                value = int(raw)
            except ValueError:
                print("숫자만 입력해 주세요.")
                continue
            if value < min_value or value > max_value:
                print(f"{min_value}~{max_value} 사이의 숫자를 입력해 주세요.")
                continue
            return value

    def _read_text(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print("입력이 비어 있습니다. 다시 입력해 주세요.")
                continue
            return raw

    def play_quiz(self):
        print("\n(퀴즈 풀기 기능은 준비 중입니다.)")

    def add_quiz(self):
        print("\n(퀴즈 추가 기능은 준비 중입니다.)")

    def list_quizzes(self):
        print("\n(퀴즈 목록 기능은 준비 중입니다.)")

    def show_score(self):
        print("\n(점수 확인 기능은 준비 중입니다.)")

    def run(self):
        print("퀴즈 게임을 시작합니다.")
        while True:
            self.show_menu()
            try:
                choice = self._read_int("메뉴를 선택하세요: ", 1, 5)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("\n게임을 종료합니다. 이용해 주셔서 감사합니다.")
                    break
            except (EOFError, KeyboardInterrupt):
                print("\n\n입력이 중단되었습니다. 안전하게 종료합니다.")
                break
