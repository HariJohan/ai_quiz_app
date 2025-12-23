import os
import requests
import json
from models.question import Question

class AIService:

    def get_questions(self, topic):
        api_key = os.getenv("OPENROUTER_API_KEY")

        url = "https://openrouter.ai/api/v1/chat/completions"

        prompt = f"""
        Generate 3 multiple-choice quiz questions on {topic}.
        Return ONLY valid JSON in this format:

        {{
          "questions": [
            {{
              "question": "string",
              "options": ["A", "B", "C", "D"],
              "answer": "exact option text"
            }}
          ]
        }}
        """

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=body)

        ai_text = response.json()["choices"][0]["message"]["content"]

        data = json.loads(ai_text)

        questions = []
        for q in data["questions"]:
            questions.append(
                Question(
                    q["question"],
                    q["options"],
                    q["answer"]
                )
            )

        return questions
