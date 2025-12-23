import uuid

class GameSession:
    def __init__(self, topic, questions):
        self.game_id = str(uuid.uuid4())[:8]
        self.topic = topic
        self.questions = questions
        self.score = 0
