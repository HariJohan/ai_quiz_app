import uuid

class GameSession:
    def __init__(self, topic, questions):
        self.game_id = str(uuid.uuid4())[:8]
        self.topic = topic
        self.questions = questions

        self.players = []  # [{name, score}]
        self.status = "WAITING"

        self.current_question_index = 0

        # Track answers PER QUESTION
        self.answers = {}  # { player_name: answer }

        self.winner = None

       
