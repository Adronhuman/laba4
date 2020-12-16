import os
from flask import Flask, render_template, flash, redirect, url_for, request, abort, jsonify
from flask import make_response
from database import *
import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt

app = Flask(__name__)

engine = create_engine('mssql+pyodbc://PC0007/lab-2?driver=SQL+Server+Native+Client+11.0')

bcrypt = Bcrypt(app)

DBSession = sessionmaker(bind=engine)
session = DBSession()
auth = HTTPBasicAuth(app)

@auth.verify_password
def verify_password(username, password):
    print("verify")
    user = session.query(User).filter_by(username = username).first()
    if user==None:
        return False
    return check_password_hash(user.password,password=password)

@app.route('/articles', methods=['POST'])
def addArticle():
    time = datetime.datetime.now()
    newArticle = Article(title=request.json['title'], text=request.json['text'],
                         create_date=str(time), author_id=request.json["author_id"], last_edit_date='0')
    session.add(newArticle)
    session.commit()
    return "success"

@app.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    temp = session.query(Article).order_by(Article.id.desc()).first()
    if temp is None:
        abort(404)
    number = session.query(Article).order_by(Article.id.desc()).first().id
    if article_id > number:
        abort(404)
    else:
        article = session.query(Article).filter_by(id=article_id).one()
        answer = {"id": article.id, "author_id": article.author_id, "text": article.text,
                  "create_date": article.create_date, "last_edit_date": article.last_edit_date}
        return jsonify({"article": answer})
    

@app.route('/articles/<int:article_id>', methods=['POST'])
@auth.login_required
def edit_article(article_id):
    print(article_id)
    time = datetime.datetime.now()
    article = session.query(Article).filter_by(id=article_id).one()
    user = session.query(User).filter_by(username=auth.current_user()).first()
    newRequest = Request(title=article.title, text=request.json['text'],
                         article_id=article_id, user_id=user.id,
                         DateTimeOfRequest=str(time), status="waiting",
                         )
    session.add(newRequest)
    session.commit()
    return "success"


@app.route('/user', methods=['POST'])
def create_user():
    newUser = User(username=request.json['username'],
                   password=generate_password_hash(request.json['password']),
                   email=request.json['email'],
                   phone=request.json['phone'],
                   role='moderator')
    session.add(newUser)
    session.commit()
    return "success"


@auth.login_required
@app.route('/user/<id>',methods=['GET'])
def get_user(id):
    print("yeah ")
    return "ewew",202
    number = session.query(User).order_by(User.id.desc()).first().id
    if id > number:
        abort(404)
    else:
        user = session.query(User).filter_by(id=id).one()
        answer = {"id": user.id, "email": user.email, "phone": user.phone,
                  "username": user.username, "role": user.role}
        return jsonify({"article": answer})


@app.route('/user/logout/', methods=['GET'])
@auth.login_required
def logout():
    logout_user()
    return "You have been logged out."


@auth.login_required
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    editedUser = session.query(User).filter_by(id=user_id).one()
    editedUser.username = request.json["username"]
    editedUser.password = generate_password_hash(request.json["password"])
    editedUser.email = request.json["email"]
    editedUser.phone = request.json["phone"]
    editedUser.role = request.json["role"]
    session.commit()
    return "success"


@auth.login_required
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_to_delete = session.query(User).filter_by(id=user_id).one()
    session.delete(user_to_delete)
    session.commit()
    return "success"


##@app.route('/user/login/', methods=['post', 'get'])
##def login():
##    form = LoginForm()
##    if form.validate_on_submit():
##        user = session.query(User).filter(User.username == form.username.data).first()
##        password = session.query(User).filter(
##            User.password == str(b.b64encode(form.password.data.encode("UTF-8")))).first()
##        if user and password:
##            login_user(user, remember=form.remember.data)
##            return "logged"
##
##        flash("Invalid username/password", 'error')
##        return redirect(url_for('login'))
##    return render_template('login.html', form=form)
##


@app.route('/requests/<int:request_id>/', methods=['GET'])
@auth.login_required
def get_request(request_id):
    user = session.query(User).filter_by(username=auth.current_user()).first()
    print(user.username)
    if user.role != "moderator":
        return make_response('Access denied', 403)
    else:
        request_ = session.query(Request).filter_by(id=request_id).one()
        answer = {"id": request_.id, "title": request_.title, "text": request_.text, "article_id": request_.article_id,
                  "user_id": request_.user_id, "DateTimeOfRequest": request_.DateTimeOfRequest,
                  "status": request_.status}
        return jsonify({"request": answer})


@app.route('/requests/<int:request_id>', methods=['POST'])
@auth.login_required
def set_status(request_id):
    user = session.query(User).filter_by(username=auth.current_user()).first()
    if user.role != "moderator":
        return make_response('Access denied', 403)
    else:
        editedRequest = session.query(Request).filter_by(id=request_id).one()
        print(request.json)
        editedRequest.status = request.json["status"]
        session.commit()
        if request.json["status"] == 'accepted':
            time = datetime.datetime.now()
            editedRequest = session.query(Request).filter_by(id=request_id).one()
            article_id = editedRequest.article_id
            editedArticle = session.query(Article).filter_by(id=article_id).one()
            editedArticle.text = editedRequest.text
            editedArticle.ready = 'true'
            editedArticle.last_edit_date = str(time)
            session.commit()
        return "success"


if __name__ == '__main__':
    app.run(debug=True)
