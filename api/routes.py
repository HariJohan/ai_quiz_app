from fastapi import APIRouter, HTTPException
from ai.ai_service import AIService
from models.game_session import GameSession
from storage.in_memory_store import game_sessions
from game.quiz_evaluator import QuizEvaluator
from game.game_manager import GameManager
from api.websocket import broadcast_event
from fastapi import HTTPException
from storage.in_memory_store import game_sessions
from api.websocket import broadcast_event

router = APIRouter()

ai_service = AIService()
game_manager = GameManager()

@router.get("/game/status")
def game_status(game_id: str):
    game = game_sessions.get(game_id)

    if not game:
        raise HTTPException(404, "Game not found")

    return {
        "game_id": game_id,
        "player_count": len(game.players), 
        "status": game.status,
        "players": game.players,
        "host": game.players[0]["name"] if game.players else None
    }






@router.post("/game/create")
def create_game(player_name: str, topic: str):
    game = game_manager.create_game(player_name, topic, questions=[])

    return {
        "game_id": game.game_id,
        "player": player_name,
        "topic": topic,
        "status": game.status
    }


# JOIN GAME
@router.post("/game/join")
def join_game(game_id: str, player_name: str):
    try:
        game = game_manager.join_game(game_id, player_name)
        return {
            "message": "Player joined successfully",
            "game_id": game.game_id,
            "players": game.players,
            "status": game.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# START GAME (HOST ONLY)
@router.post("/game/start")
def start_game(game_id: str):
    game = game_sessions.get(game_id)

    if not game:
        raise HTTPException(400, "Game not found")

    if len(game.players) < 2:
        raise HTTPException(400, "Waiting for second player")

    if game.status == "STARTED":
        raise HTTPException(400, "Game already started")

    # AI QUESTIONS GENERATED HERE
    game.questions = ai_service.get_questions(game.topic)
    game.current_question_index = 0
    game.status = "STARTED"

    q = game.questions[0]
    return {
        "status": "STARTED",
        "question_number": 1,
        "question": q.question,
        "options": q.options
    }



@router.post("/game/answer")
async def submit_answer(game_id: str, player_name: str, answer: str):
    game = game_sessions.get(game_id)

    # Game validation
    if not game or game.status != "STARTED":
        raise HTTPException(status_code=400, detail="Game not active")

    # Find player
    player = next((p for p in game.players if p["name"] == player_name), None)
    if not player:
        raise HTTPException(status_code=400, detail="Invalid player")

    # Prevent double submission
    if player["submitted"]:
        raise HTTPException(status_code=400, detail="Answer already submitted")

    #  SAFE question access
    if game.current_question_index >= len(game.questions):
        raise HTTPException(status_code=400, detail="No more questions")

    current_q = game.questions[game.current_question_index]

    # Check answer
    if answer == current_q.answer:
        player["score"] += 1

    player["submitted"] = True

    # Wait until BOTH players submit
    if not all(p["submitted"] for p in game.players):
        return {
            "status": "WAITING",
            "message": "Waiting for other player"
        }

    # Reset submission flags
    for p in game.players:
        p["submitted"] = False

    game.current_question_index += 1

    # GAME FINISHED
    if game.current_question_index >= len(game.questions):
        game.status = "FINISHED"

        # Decide winner
        scores = sorted(game.players, key=lambda x: x["score"], reverse=True)
        if scores[0]["score"] == scores[1]["score"]:
            game.winner = "DRAW"
        else:
            game.winner = scores[0]["name"]

        await broadcast(game_id, {
            "type": "GAME_OVER",
            "winner": game.winner,
            "players": game.players
        })

        return {
            "status": "FINISHED",
            "winner": game.winner,
            "players": game.players
        }

    # NEXT QUESTION
    await broadcast(game_id, {
        "type": "NEXT_QUESTION",
        "question_number": game.current_question_index + 1
    })

    return {
        "status": "NEXT",
        "question_number": game.current_question_index + 1
    }


@router.get("/game/question")
def get_question(game_id: str):
    game = game_sessions.get(game_id)

    if not game:
        raise HTTPException(status_code=400, detail="Invalid game ID")

    # Game finished → tell frontend clearly
    if game.status == "FINISHED":
        return {
            "status": "FINISHED",
            "winner": game.winner,
            "players": game.players
        }

    # Game not started yet
    if game.status != "STARTED":
        raise HTTPException(status_code=400, detail="Game not started")

    index = game.current_question_index

    # Safety guard (should never happen, but defensive coding)
    if index >= len(game.questions):
        game.status = "FINISHED"
        return {
            "status": "FINISHED",
            "winner": game.winner,
            "players": game.players
        }

    q = game.questions[index]

    return {
        "status": "QUESTION",
        "question_number": index + 1,
        "question": q.question,
        "options": q.options
    }


@router.get("/game/result")
def get_result(game_id: str):
    game = game_sessions.get(game_id)

    return {
        "player1": game.player1_score,
        "player2": game.player2_score,
        "winner": game.get_winner()
    }
