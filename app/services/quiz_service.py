
from sqlalchemy.orm import Session
from app.models.quiz import Quiz, Question, Option

class QuizService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, video_id: int, questions: list):
        quiz = Quiz(title=title, video_id=video_id)
        self.db.add(quiz)
        self.db.commit()
        self.db.refresh(quiz)
        for q in questions:
            question = Question(prompt=q['prompt'], quiz_id=quiz.id)
            self.db.add(question)
            self.db.commit()
            for opt in q.get('options', []):
                o = Option(text=opt.get('text'), is_correct=opt.get('is_correct', False), question_id=question.id)
                self.db.add(o)
            self.db.commit()
        self.db.refresh(quiz)
        return quiz

    def get_by_video(self, video_id: int):
        return self.db.query(Quiz).filter(Quiz.video_id == video_id).all()

    def get(self, quiz_id: int):
        return self.db.query(Quiz).filter(Quiz.id == quiz_id).first()

    def grade(self, quiz_id: int, selected_option_ids: list):
        quiz = self.get(quiz_id)
        if not quiz:
            raise ValueError('Quiz not found')
        all_options = [opt for q in quiz.questions for opt in q.options]
        correct_ids = {opt.id for opt in all_options if opt.is_correct}
        selected = set(selected_option_ids)
        correct = len(correct_ids & selected)
        total = len(quiz.questions)
        return total, correct
