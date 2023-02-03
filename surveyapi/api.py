"""
api.py
- provides the API endpoints for consuming and producing 
  REST requests and responses
"""

from functools import wraps
from datetime import datetime, timedelta
from flask_cors import cross_origin
from flask import Blueprint, jsonify, request, current_app

import jwt
import json

from .models import db, Survey, Question, Choice, User

api = Blueprint('api', __name__)







def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            print('f::::',f)
            data = jwt.decode(token, current_app.config['SECRET_KEY'],algorithms="HS256")
            # print(data)
            # data = jwt.decode(token, current_app.config['SECRET_KEY'],algorithm="HS256")
            # print(data)
            user = User.query.filter_by(email=data['sub']).first()
            print("usesr",user)
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify





  
@api.route('/login/', methods=('POST',))
@cross_origin(origin='http://127.0.0.1:5173/',headers=['Content- Type','Authorization'])
def login():
    print("login")
    data = request.get_json()
    user = User.authenticate(**data)
    print("login route user ",user)
    if not user:
        return jsonify({ 'notification': 'Login Failed: Invalid credentials', 'authenticated': False }), 201
    token = jwt.encode({
        'sub': user.email,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=10080),
        "admin":(user.email == "surajraika5sr@gmail.com")},
        current_app.config['SECRET_KEY'],algorithm="HS256")
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify({"token":token,"notification":'Login Succesfull',"authenticated":True}) 


@api.route('/register/', methods=('POST',))
def register():
    print("rejister:")
    data = request.get_json()
    print(data)
    # checkuser=
    UserExist=User.query.filter_by(email=data['email']).first()
    if UserExist == None :
        user = User(**data)
        print("register user ",user)
        db.session.add(user)
        db.session.commit()
    else:
        return jsonify({"notification":'Email is Already Taken',"authenticated":False})
    return jsonify({"user":user.to_dict(),"notification":'Account Created ',"authenticated":True}), 201







@api.route('/CreateSurvey/',methods=('POST',))
@token_required
def NewSurvey(current_user):
    data = request.get_json()
    # print(data)
    survey = Survey(name=data['name'])
    questions = []
    for q in data['questions']:
        question = Question(text=q['text'])
        question.choices = [Choice(text=c['text']) for c in q['choices']]
        questions.append(question)

    survey.questions = questions
    survey.img = data['thumnail']
    survey.description = data['description']
    survey.creator = current_user
    # print('questions',questions)
    # print(survey.questions)
    db.session.add(survey)
    db.session.commit()
    return jsonify(''), 201

@api.route('/Delete-Survey/<int:id>/',methods=('POST',))
@token_required
def DeleteSurvey(current_user,id):
    # data = request.get_json()
    # print(data)
    # print('<int:id>/ :',id)
    # print('current user :',current_user.id)
    # survey32=Survey.query.filter_by(id=id)
    # print(Survey.query.get(id).creator_id)
    if (Survey.query.get(id).creator_id == current_user.id or ( current_user.email == "surajraika5sr@gmail.com" )):
        Survey.query.filter_by(id=id).delete()
    
    # print(Survey.query)
    # print('questions',questions)
    # print(survey.questions)
    # db.session.add(survey)
    db.session.commit()
    return jsonify(''), 201


@api.route('/QuestionChoice/', methods=('POST',))
def QuestionChoice():
    print(request)
    data = request.get_json()
    print('data:',data)
    c_id=data['choice_id']
    q_id=data['question_id']
    
    # question=Question.get(id=q_id)
    question=Question.query.filter_by(id=q_id).first()
    if not question.ChoicePercent:
        Obj={}
        for choice in question.choices:
            id='Choice'+str(choice.id)
            Obj[id]=0
        question.ChoicePercent=json.dumps(Obj)


            
    ChoiceId='Choice'+str(c_id)

    ADict=json.loads(question.ChoicePercent)

    ADict[ChoiceId]+= 1
    print(question.ChoicePercent)
    question.ChoicePercent=json.dumps(ADict)

    db.session.commit()    
    
    return jsonify({"ChoicePersent":question.ChoicePercent}) 


@api.route('/surveys/', methods=('GET',))
def fetch_surveys():
    surveys = Survey.query.all()
    return jsonify([{"name":s.name,"img":s.img,"id":s.id} for s in surveys])



@api.route('/surveys/<int:id>/', methods=('GET', 'PUT'))
def survey(id):
    if request.method == 'GET':
        survey = Survey.query.get(id)
        Creator=User.query.get(survey.creator_id)
        print(Creator,Creator.name)
        survey_dic=survey.to_dict()
        survey_dic["creator_name"]=Creator.name
        survey_dic["creator_email"]=Creator.email

        return jsonify({ 'survey': survey_dic })
    elif request.method == 'PUT':
        data = request.get_json()
        for q in data['questions']:
            choice = Choice.query.get(q['choice'])
            choice.selected = choice.selected + 1
        db.session.commit()
        return jsonify(survey.to_dict()), 201