import json
import os

from quiz import Quiz
from quiz_data import DEFAULT_QUIZZES

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.quizzes = list(DEFAULT_QUIZZES)
        self.best_score = None
        self.load_data()

    # ----- 파일 저장/불러오기 -----

    def _read_disk_state(self):
        """저장 파일에 있는 최신 상태를 읽어온다. 파일이 없거나 손상되었으면 None."""
        if not os.path.exists(self.data_file):
            return None
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            if not quizzes:
                raise ValueError("퀴즈 데이터가 비어 있습니다.")
            return quizzes, data.get("best_score")
        except (json.JSONDecodeError, KeyError, ValueError, OSError):
            return None

    def load_data(self):
        state = self._read_disk_state()
        if state is None:
            if os.path.exists(self.data_file):
                print(
                    "\n[안내] 저장된 데이터 파일이 손상되어 "
                    "기본 퀴즈 데이터로 복구합니다."
                )
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
            self.save_data()
            return
        self.quizzes, self.best_score = state

    def save_data(self, new_quiz=None, achieved_score=None):
        """상태를 저장한다.

        여러 개의 프로그램이 동시에 실행 중일 수 있으므로, 저장 직전에
        파일을 다시 읽어 최신 데이터를 가져온 뒤 그 위에 이번 변경 사항
        (새 퀴즈 / 새로 달성한 점수)만 얹어서 저장한다. 이렇게 하면 다른
        프로그램이 먼저 저장해 둔 내용을 그대로 덮어써서 잃어버리는 것을
        막을 수 있다.
        """
        state = self._read_disk_state()
        quizzes = state[0] if state else list(self.quizzes)
        best_score = state[1] if state else self.best_score

        if new_quiz is not None:
            quizzes.append(new_quiz)

        best_score_updated = False
        if achieved_score is not None and (
            best_score is None or achieved_score > best_score
        ):
            best_score = achieved_score
            best_score_updated = True

        self.quizzes = quizzes
        self.best_score = best_score

        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"\n[오류] 데이터를 저장하지 못했습니다: {e}")

        return best_score_updated

    # ----- 메뉴/화면 -----

    def show_menu(self):
        print("\n" + "=" * 30)
        print("       파이썬 기초 퀴즈 게임")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    # ----- 공통 입력 처리 -----

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

    # ----- 기능: 퀴즈 풀기 -----

    def play_quiz(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        total = len(self.quizzes)
        score = 0
        print(f"\n총 {total}문제를 출제합니다.")
        for i, quiz in enumerate(self.quizzes, start=1):
            quiz.display(i)
            answer = self._read_int(
                "정답 번호를 입력하세요: ", 1, len(quiz.choices)
            )
            if quiz.is_correct(answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
        print(f"\n결과: 총 {total}문제 중 {score}문제를 맞혔습니다.")
        if self.save_data(achieved_score=score):
            print("최고 점수를 갱신했습니다!")

    # ----- 기능: 퀴즈 추가 -----

    def add_quiz(self):
        print("\n[퀴즈 추가]")
        question = self._read_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choice = self._read_text(f"선택지 {i}을(를) 입력하세요: ")
            choices.append(choice)
        answer = self._read_int("정답 번호(1~4)를 입력하세요: ", 1, 4)
        new_quiz = Quiz(question, choices, answer)
        self.save_data(new_quiz=new_quiz)
        print("퀴즈가 추가되었습니다.")

    # ----- 기능: 퀴즈 목록 -----

    def list_quizzes(self):
        print("\n[퀴즈 목록]")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")

    # ----- 기능: 점수 확인 -----

    def show_score(self):
        print("\n[점수 확인]")
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 점수: {self.best_score}")

    # ----- 실행 루프 -----

    def run(self):
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_score,
        }
        print("퀴즈 게임을 시작합니다.")
        while True:
            self.show_menu()
            try:
                choice = self._read_int("메뉴를 선택하세요: ", 1, 5)
                if choice == 5:
                    self.save_data()
                    print("\n게임을 종료합니다. 이용해 주셔서 감사합니다.")
                    break
                actions[choice]()
            except (EOFError, KeyboardInterrupt):
                print("\n\n입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
                self.save_data()
                break
