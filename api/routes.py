from fastapi import APIRouter
from ai.ai_service import AIService
from models.game_session import GameSession
from storage.in_memory_store import game_sessions
from game.quiz_evaluator import QuizEvaluator

router = APIRouter()
ai_service = AIService()
evaluator = QuizEvaluator()


@router.post("/game/create")
def create_game(topic: str):
    questions = ai_service.get_questions(topic)
    game = GameSession(topic, questions)
    game_sessions[game.game_id] = game

    return {
        "game_id": game.game_id,
        "topic": topic,
        "total_questions": len(questions)
    }


@router.post("/game/submit")
def submit_answers(game_id: str, answers: list[str]):
    game = game_sessions.get(game_id)

    if not game:
        return {"error": "Invalid game ID"}

    score = evaluator.evaluate_api(game, answers)

    return {
        "game_id": game_id,
        "score": score,
        "total": len(game.questions)
    }
