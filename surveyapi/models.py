"""
models.py
- Data classes for the surveyapi application
"""
from sqlalchemy import MetaData , JSON
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    surveys = db.relationship('Survey', backref="creator", lazy=False)

    def __init__(self, email, password , name):
        self.email = str(email)
        self.name = str(name)
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        print('inside of authen')
        email = kwargs.get('email')
        password = kwargs.get('password')
        print(email,password)
        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if user:
            print("authen user",user)
            print(check_password_hash(user.password, password))
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    img=db.Column(db.Text)
    name = db.Column(db.Text)
    description=db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', backref="survey", lazy=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def to_dict(self):
        return dict(id=self.id,
                    img=self.img,
                    name=self.name,
                    description=self.description,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    questions=[question.to_dict() for question in self.questions])

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    choices = db.relationship('Choice', backref='question', lazy=False)
    ChoicePercent=db.Column(JSON, nullable=True)

    def to_dict(self):
        return dict(id=self.id,
                    text=self.text,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    survey_id=self.survey_id,
                    choices=[choice.to_dict() for choice in self.choices])

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    selected = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def to_dict(self):
        return dict(id=self.id,
                    text=self.text,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    question_id=self.question_id)

    # @classmethod
    # def SelectChoice(cls,**kwargs):
    #     print('inside of authen')
    #     UserId=kwargs.get('id')
    #     ChoiceId=kwargs.get('question_id')
    #     if not UserId or not ChoiceId:
    #         return None
    #     choice= cls.query.filter_by(id=ChoiceId).first()
    #     choice.selected=1
    #     db.session.add(choice)
    #     db.session.commit()
    #     return True