class QuizEvaluator:

    def evaluate_api(self, game_session, answers):
        score = 0

        for i, q in enumerate(game_session.questions):
            if answers[i] == q.answer:
                score += 1

        game_session.score = score
        return score
