class QuizEvaluator:

    def evaluate(self, game_session):
        score = 0

        for q in game_session.questions:
            print("\n" + q.question)

            for i, option in enumerate(q.options):
                print(f"{chr(65+i)}) {option}")

            user_answer = input().strip().upper()
            selected_option = q.options[ord(user_answer) - 65]

            if selected_option == q.answer:
                score += 1

        game_session.score = score
        return score
