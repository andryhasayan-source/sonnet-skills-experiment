from aiogram import Router

router = Router()

QUESTIONS = [
    {"q": "Столица Франции?", "a": "париж"},
    {"q": "2+2?", "a": "4"},
    {"q": "Цвет неба?", "a": "голубой"},
]

class Quiz:
    def __init__(self, questions=QUESTIONS, time_limit=30.0):
        self.questions = questions
        self.time_limit = time_limit
        self._state = {}  # user -> {idx, score, asked_at}

    def start(self, user_id, now):
        self._state[user_id] = {"idx": 0, "score": 0, "asked_at": now}
        return self.questions[0]["q"]

    def score(self, user_id):
        st = self._state.get(user_id)
        return st["score"] if st else 0

    def answer(self, user_id, text, now):
        st = self._state.get(user_id)
        if st is None or st["idx"] >= len(self.questions):
            return {"correct": False, "timed_out": False, "finished": True,
                    "next_question": None, "score": self.score(user_id)}
        cur = self.questions[st["idx"]]
        timed_out = (now - st["asked_at"]) > self.time_limit
        correct = (not timed_out) and \
                  text.strip().lower() == cur["a"].strip().lower()
        if correct:
            st["score"] += 1
        st["idx"] += 1
        finished = st["idx"] >= len(self.questions)
        if finished:
            next_q = None
        else:
            next_q = self.questions[st["idx"]]["q"]
            st["asked_at"] = now
        return {"correct": correct, "timed_out": timed_out,
                "finished": finished, "next_question": next_q,
                "score": st["score"]}

if __name__ == "__main__":
    pass
