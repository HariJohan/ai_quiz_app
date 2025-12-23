from game.game_manager import GameManager
from ai.ai_service import AIService
from game.quiz_evaluator import QuizEvaluator
from models.game_session import GameSession

def main():
    print("Enter 1 to Create Quiz")
    start = input().strip()

    if start != "1":
        print("Invalid option")
        return

    game_manager = GameManager()
    topic = game_manager.choose_topic()

    if not topic:
        return

    ai_service = AIService()
    questions = ai_service.get_questions(topic)

    game_session = GameSession(topic, questions)

    print(f"\nGame Created Successfully!")
    print(f"Game ID: {game_session.game_id}")
    print(f"Topic: {game_session.topic}")

    evaluator = QuizEvaluator()
    evaluator.evaluate(game_session)

    print(f"\nFinal Score: {game_session.score} / {len(game_session.questions)}")
    print(f"Game ID: {game_session.game_id}")

if __name__ == "__main__":
    main()
