# Run with "python server.py"

from bottle import run, get, post, template, request, redirect, response, HTTPResponse
from models import initialize_db, db, User, Note
from schemas import *
import jwt
from datetime import datetime, timedelta

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 1800 



# Start your code here, good luck (: ...
initialize_db()

def validate_credentials(email, passw):
     db.connect()
     user = User.select().where(User.email == email, User.password == passw).first()
     db.close()
     return user


@post('/login')
def login():
    try:
        email =  request.forms.get('email')
        passw = request.forms.get('password')
        result = UserSchema().load({"email": email, "password": passw})
        user = validate_credentials(email, passw)
        if user:
            payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            response.set_cookie("jwtoken",jwt_token, secret=JWT_SECRET)
            redirect('/findAll')
        return HTTPResponse(status=400,
                            body=template('index.html',
                                        message='Wrong credentials'))
        
    except ValidationError as err:
        return HTTPResponse(status=400,
                                body=template('index.html',
                                            message=err.messages))
    

@post('/add_user')
def add_user():
    try:
        result = UserSchema().load({"email": request.forms.get('email'), "password": request.forms.get('password')})
        db.connect()
        print(result)
        User.create(email=result.data['email'], password=result.data['password'])
        db.close()
        redirect('/login')
        return HTTPResponse(status=200,
                            body=template('index.html',
                                           message='User have been created succefully'))
    except ValidationError as err:
        print(err.messages) 
        return HTTPResponse(status=400,
                            body=template('index.html',
                                           message=err.messages))


@get('/create')
def create_button():
    return template('create.html')
    
@post('/create')
def create_action():
    try:
        result = NoteSchema().load({"name": request.forms.get('name'), "description": request.forms.get('description')})
        jwt_token = request.get_cookie("jwtoken", secret=JWT_SECRET)
        payload = jwt.decode(jwt_token, JWT_SECRET, JWT_ALGORITHM)
        print(payload)
        db.connect()
        print(result)
        note = Note.create(name=result.data['name'], description=result.data['description'], user = payload['user_id'])
        db.close()
        return HTTPResponse(status=200,
                            body=template('create_response.html',
                                           message='Your note have been save succefully'))
    except ValidationError as err:
        print(err.messages) 
        return HTTPResponse(status=400,
                            body=template('create_response.html',
                                           message=err.messages))


@get('/findAll')
def findAll():
    jwt_token = request.get_cookie("jwtoken", secret=JWT_SECRET)
    payload = jwt.decode(jwt_token, JWT_SECRET, JWT_ALGORITHM)
    db.connect()
    result = [n for n in Note.select().where(Note.user == payload['user_id'])]
    db.close()
    return template('findAll.html', lista=result)


run(host='localhost', port=8000)