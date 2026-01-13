from storage.in_memory_store import game_sessions
from models.game_session import GameSession


class GameManager:

    # Create Game (Player 1)
    def create_game(self,player_name: str, topic: str, questions: list):
        game = GameSession(topic, questions)
        game.players.append({
        "name": player_name,
        "score": 0,
        "submitted":False
        })
        
        game_sessions[game.game_id] = game #gamesession object is stored 
        return game


    # Join Game (Player 1 / 2)
    def join_game(self, game_id: str, player_name: str):
        game = game_sessions.get(game_id)#gamesession object is retrieved

        if not game:#if game var is empty
            raise ValueError("Game not found")

        if len(game.players) >= 2:
            raise ValueError("Game already has 2 players")

        for player in game.players:
            if player["name"] == player_name:
                raise ValueError("Player already joined")

        game.players.append({
            "name": player_name,
            "score": 0,
            "submitted":False
        })

        return game
    
    def declare_winner(self, game):
        p1 = game.players[0]
        p2 = game.players[1]

        if p1["score"] > p2["score"]:
            game.winner = p1["name"]
        elif p2["score"] > p1["score"]:
            game.winner = p2["name"]
        else:
            game.winner = "DRAW"

        game.status = "ENDED"

