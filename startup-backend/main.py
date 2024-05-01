from turtle import title
from flask import Flask, jsonify, request, redirect, send_file, Blueprint
from flask_cors import CORS, cross_origin
from flask_restful import Resource,Api, marshal_with,reqparse,fields,marshal
import os, csv
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, current_user
from flask import jsonify
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.config.from_object(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy import extract
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity,JWTManager
import json
from flask import make_response
from functools import wraps
from flask import abort
import requests
import pymysql
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='bin@9'
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
from dateutil import parser as date_parser
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TSL"] = False
app.config["MAIL_USERNAME"] = 'rvshinde333@gmail.com'
app.config["MAIL_PASSWORD"] = 'bljsbckjdltxdhre'
mail = Mail(app)
from datetime import datetime
from celery import Celery
from celery.schedules import crontab, timedelta
port = 4000



def admin_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user or not current_user.is_authenticated or not current_user.is_admin:
            return jsonify(message="You don't have the necessary permissions to access this resource."), 403
        return func(*args, **kwargs)
    return decorated




CORS(app, supports_credentials=True, expose_headers='Authorization',origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login" # type: ignore


bcrypt = Bcrypt(app)



# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='users', lazy=True)
    policies_liked = db.relationship('Policy', backref='users', lazy=True)

    def __init__(self, name, password, email, phone, address, is_admin):
            self.name = name
            self.password = password
            self.email = email
            self.phone = phone
            self.address = address
            self.is_admin = is_admin

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='policy', lazy=True)
    users_liked = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)

class Poll(db.Model):
    __tablename__ = 'polls'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    questions = db.relationship('Question', back_populates='poll')

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))
    options = db.relationship('Option', back_populates='question')
    poll = db.relationship('Poll', back_populates='questions')

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    votes = db.Column(db.Integer, default=0)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship('Question', back_populates='options')

class QAPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('qa_posts', lazy=True))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    qa_post_id = db.Column(db.Integer, db.ForeignKey('qa_post.id'), nullable=False)
    qa_post = db.relationship('QAPost', backref=db.backref('answers', lazy=True))


    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/email', methods=['POST', 'OPTIONS'])
def send_email():
    if request.method == "OPTIONS":
        # Handle CORS preflight request
        response_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return "", 204, response_headers

    # Handle actual POST request to send email
    data = request.get_json()
    recipient = data.get("recipient")
    subject = data.get("subject")
    body = data.get("body")

    # Create a Flask-Mail message
    msg = Message(subject, recipients=[recipient], sender='no-reply@demo.com')
    msg.body = body

    # Send the message
    mail.send(msg)

    return jsonify({"message": "Email sent"}), 200




with app.app_context():
    # User resource
    
    user_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'password': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'address': fields.String,
        'is_admin': fields.Boolean
    }

    

    
    
    
# User resource
    
    class UserResource(Resource):
        
        @marshal_with(user_fields)
        
        def get(self,user_id):
            
            user = User.query.get(user_id)
            if user:
                return {
                    'id': user.id,
                    'password': user.password,
                    'name': user.name,
                    'email': user.email,
                    'phone': user.phone,
                    'address': user.address
                }
            else:
                return {'message': 'User not found'}, 404

        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('phone', type=str, required=True)
            parser.add_argument('address', type=str, required=True)
            parser.add_argument('is_admin', type=bool, required=True)
            parser.add_argument('key',type=str)
            args = parser.parse_args()
            hashing_pwd = bcrypt.generate_password_hash(args['password'])
            if args['is_admin'] == True:
                if args['key'] == '720305':
                    user = User(name=args['name'],password=hashing_pwd, email=args['email'], phone=args['phone'], address=args['address'], is_admin=args['is_admin'])
                    db.session.add(user)
                    db.session.commit()
                    return {'message': 'User created successfully'}, 201
                else:
                    return {'message': 'You do not have propery access Key'}
            else:
                user = User(name=args['name'],password=hashing_pwd, email=args['email'], phone=args['phone'], address=args['address'], is_admin=args['is_admin'])
                db.session.add(user)
                db.session.commit()
            return {'message': 'User created successfully'}, 201
        
        @jwt_required()
        def put(self, user_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next((user for user in users if user.name == current_user), None)
            # Access protected resource for the authenticated user
            if user :
                parser = reqparse.RequestParser()
                parser.add_argument('name', type=str)
                parser.add_argument('email', type=str)
                parser.add_argument('phone', type=str)
                parser.add_argument('address', type=str)
                parser.add_argument('is_admin', type=bool)
                args = parser.parse_args()

                user = User.query.get(user_id)
                if not user:
                    return {'message': 'User not found'}, 404

                if args['name']:
                    user.name = args['name']
                if args['email']:
                    user.email = args['email']
                if args['phone']:
                    user.phone = args['phone']
                if args['address']:
                    user.address = args['address']
                if args['is_admin']:
                    user.is_admin = args['is_admin']

                db.session.commit()

                return {'message': 'User updated successfully'}, 200
        @jwt_required()
        def delete(self):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next((user for user in users if user.name == current_user), None)
            
            if user:
                
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User deleted successfully'}, 200
            else:
                return {'message': 'User not found'}, 404

    # Login resource
    class LoginResource(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            args = parser.parse_args()

            username = args['name']
            password = args['password']
            
            # Retrieve the user from the database based on the provided username
            user = User.query.filter_by(name=username).first()

            if user and bcrypt.check_password_hash(user.password, password):
                user.last_login = datetime.now()
                db.session.commit()
                access_token = create_access_token(identity=user.name)
                return {'access_token': access_token, 'is_admin': user.is_admin}, 200
            else:
                return {'message': 'Invalid username or password'}, 401
            
    class ProtectedResource(Resource):
        @jwt_required()
        def get(self):
            # Retrieve the current user from the access token
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next((user for user in users if user.name == current_user), None)
            # Access protected resource for the authenticated user
            if user and user.is_admin == True:
                return jsonify({'message': 'Welcome, admin! You have access to protected resource','name':  current_user,'id': user.id})
            else:
                if user:
                    return jsonify({'message': 'Welcome, user! You have access to protected resource','name':  current_user,'id': user.id})
                else:
                    return jsonify({'message': 'User not found'})
            

    class CurrentUserCityResource(Resource):
        @jwt_required()
        def get(self):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            if user:
                return {'address': user.address, 'email': user.email}
            else:
                return {'message': 'User not found'}, 404

    class PolicyResource(Resource):
        @jwt_required()
        def get(self):
            policies = Policy.query.all()
            return [{'id': policy.id, 'title': policy.title, 'content': policy.content,
                    'likes': policy.likes, 'dislikes': policy.dislikes} for policy in policies]

        @jwt_required()
        def post(self):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            if user and user.is_admin == True: 
                data = request.get_json()
                new_policy = Policy(title=data['title'], content=data['content']) # type: ignore
                db.session.add(new_policy)
                db.session.commit()
                return {'message': 'Policy created successfully'}, 201
            else:
                return {'message': 'You do not have propery access Key'}

    class SinglePolicyResource(Resource):
        @jwt_required()
        def get(self, policy_id):
            policy = Policy.query.get_or_404(policy_id)
            return {'id': policy.id, 'title': policy.title, 'content': policy.content,
                    'likes': policy.likes, 'dislikes': policy.dislikes, 'comments': [{'id': comment.id, 'user': comment.users.name,'user_id': comment.users.id, 'comment_text': comment.comment_text} for comment in policy.comments]}
        
        @jwt_required()
        def delete(self, policy_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            if user and user.is_admin == True:
                policy = Policy.query.get_or_404(policy_id)
                db.session.delete(policy)
                db.session.commit()
                return {'message': 'Policy deleted successfully'}, 200
            else:
                return {'message': 'You do not have propery access Key'}
            
        @jwt_required()
        def put(self, policy_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            if user and user.is_admin == True:
                policy = Policy.query.get_or_404(policy_id)
                data = request.get_json()
                if data['title']:
                    policy.title = data['title']
                if data['content']:
                    policy.content = data['content']
                db.session.commit()
                return {'message': 'Policy updated successfully'}, 200
            else:
                return {'message': 'You do not have propery access Key'}
            
    class CommentResource(Resource):
        @jwt_required()
        def post(self, policy_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            if user and user.is_admin == False:
                data = request.get_json()
                policy = Policy.query.get_or_404(policy_id)
                new_comment = Comment(user_id=user.id, policy=policy, comment_text=data['text']) # type: ignore
                db.session.add(new_comment)
                db.session.commit()
                return {'message': 'Comment added successfully'}, 201
            else:
                return {'message': 'You do not have propery access Key'}, 405
            
    class SingleCommentResource(Resource):    
        @jwt_required()
        def delete(self, comment_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            comment = Comment.query.get_or_404(comment_id)

            if user and user.is_admin == False and user.id == comment.user_id:
                db.session.delete(comment)
                db.session.commit()
                return {'message': 'Comment deleted successfully'}, 200
            else:
                return {'message': 'You do not have proper access Key'}

    class PollResource(Resource):
        def get(self, poll_id):
            poll = Poll.query.get_or_404(poll_id)
            # You may want to customize the data returned based on your needs
            return {
                'id': poll.id,
                'title': poll.title,
                'questions': [
                    {
                        'id': question.id,
                        'text': question.text,
                        'options': [{'id': option.id, 'text': option.text, 'votes': option.votes} for option in question.options]
                    }
                    for question in poll.questions
                ]
            }

        def put(self, poll_id):
            data = request.get_json()
            poll = Poll.query.get_or_404(poll_id)
            poll.title = data['title']
            db.session.commit()
            return {'message': 'Poll updated successfully'}

        def delete(self, poll_id):
            poll = Poll.query.get_or_404(poll_id)
            db.session.delete(poll)
            db.session.commit()
            return {'message': 'Poll deleted successfully'}


    class QuestionResource(Resource):
        def get(self, question_id):
            question = Question.query.get_or_404(question_id)
            # Customize the data returned based on your needs
            return {
                'id': question.id,
                'text': question.text,
                'options': [{'id': option.id, 'text': option.text, 'votes': option.votes} for option in question.options]
            }

        def put(self, question_id):
            data = request.get_json()
            question = Question.query.get_or_404(question_id)
            question.text = data['text']
            db.session.commit()
            return {'message': 'Question updated successfully'}

        def delete(self, question_id):
            question = Question.query.get_or_404(question_id)
            db.session.delete(question)
            db.session.commit()
            return {'message': 'Question deleted successfully'}


    class OptionResource(Resource):
        def put(self, option_id):
            option = Option.query.get_or_404(option_id)
            option.votes += 1
            db.session.commit()
            return {'message': 'Vote recorded successfully'}

        @jwt_required()
        def delete(self, option_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            if user and user.is_admin == True:
                option = Option.query.get_or_404(option_id)
                db.session.delete(option)
                db.session.commit()
                return {'message': 'Option deleted successfully'}
            else:
                return {'message': 'You do not have proper access key'}

    class PollListResource(Resource):
        def get(self):
            polls = Poll.query.all()
            # Return a list of polls
            return jsonify([
                {
                    'id': poll.id,
                    'title': poll.title,
                    'description': poll.description,
                }
                for poll in polls
            ])
        

        def post(self):
            data = request.get_json()
            poll = Poll(title=data['title'], description=data['description']) #type:ignore 
            db.session.add(poll)
            db.session.commit()
            return {'message': 'Poll created successfully', 'poll_id': poll.id}


    class QuestionListResource(Resource):
        def post(self, poll_id):
            data = request.get_json()
            poll = Poll.query.get_or_404(poll_id)
            question = Question(text=data['text'], poll=poll) # type: ignore
            db.session.add(question)
            db.session.commit()
            return {'message': 'Question created successfully', 'question_id': question.id}


    class OptionListResource(Resource):
        def post(self, question_id):
            data = request.get_json()
            question = Question.query.get_or_404(question_id)
            option = Option(text=data['text'], question=question) # type: ignore
            db.session.add(option)
            db.session.commit()
            return {'message': 'Option created successfully', 'option_id': option.id}

    class PolicyLikeResource(Resource):
        @jwt_required()
        def put(self, policy_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            policy = Policy.query.get_or_404(policy_id)
            if user and policy in user.policies_liked:
            # User has already liked the policy, remove the like
                user.policies_liked.remove(policy)
                policy.likes -= 1
            else:
                # User is liking the policy
                if user:
                    user.policies_liked.append(policy)
                    policy.likes += 1

                
            db.session.commit()
            return {'message': 'Policy liked successfully'}
        
    class PolicyDislikeResource(Resource):
        @jwt_required()
        def put(self, policy_id):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            policy = Policy.query.get_or_404(policy_id)
            # If the user had liked the policy before, remove the like
            if user and policy in user.policies_liked:
                user.policies_liked.remove(policy)
                policy.likes -= 1
            db.session.commit()
            return {'message': 'Policy disliked successfully'}

    class QAPostResource(Resource):
        qa_post_fields = {
            'id': fields.Integer,
            'title': fields.String,
            'content': fields.String,
            'user_id': fields.Integer,
        }

        @marshal_with(qa_post_fields)
        def get(self, qa_post_id):
            qa_post = QAPost.query.get_or_404(qa_post_id)
            return qa_post

    class QAPostListResource(Resource):
        qa_post_fields = {
            'id': fields.Integer,
            'title': fields.String,
            'content': fields.String,
            'user_id': fields.Integer,
        }

        @marshal_with(qa_post_fields)
        def get(self):
            qa_posts = QAPost.query.all()
            return qa_posts

        @jwt_required()
        def post(self):
            current_user = get_jwt_identity()
            users = User.query.all()
            user = next(filter(lambda u: u.name == current_user, users), None)
            if user:
                data = request.get_json()
                print(data)
                new_qa_post = QAPost(title= data['title'], content = data['content'], user_id=user.id) # type: ignore
                db.session.add(new_qa_post)
                db.session.commit()
                return {'id':new_qa_post.id}, 201
            else:
                return {'message': 'You do not have proper access key'}

    class AnswerResource(Resource):
        answer_fields = {
            'id': fields.Integer,
            'text': fields.String,
            'user_id': fields.Integer,
            'qa_post_id': fields.Integer,
        }

        @marshal_with(answer_fields)
        def get(self, answer_id):
            answer = Answer.query.get_or_404(answer_id)
            return answer

    class AnswerListResource(Resource):
        answer_fields = {
            'id': fields.Integer,
            'text': fields.String,
            'user_id': fields.Integer,
            'qa_post_id': fields.Integer,
        }

        @marshal_with(answer_fields)
        def get(self):
            answers = Answer.query.all()
            return answers

        @marshal_with(answer_fields)
        def post(self):
            data = request.get_json()
            new_answer = Answer(**data)
            db.session.add(new_answer)
            db.session.commit()
            return new_answer, 201
        
    @app.route('/currentUserCity', methods=['OPTIONS'])
    def handle_options_2():
        response = jsonify({'message': 'Preflight request successful'})
        response.headers.add('Access-Control-Allow-Methods', 'PUT')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response
    
    @app.route('/search-policies', methods=['GET'])
    def search_policies():
        # Assuming the policy name is sent as a query parameter
        search_query = request.args.get('policy_name', '')
        results = Policy.query.filter(Policy.title.ilike(f'%{search_query}%')).all()

        # Convert the results to a list of dictionaries
        results_dict = [{"policy_name": policy.title, "content": policy.content} for policy in results]

        return jsonify(results_dict)
    
    
        
    # Define allowed HTTP methods for each resource
    api.add_resource(UserResource, '/users', '/users/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    api.add_resource(LoginResource, '/login',  methods=['POST'],endpoint='login')
    api.add_resource(ProtectedResource, '/protected',methods=['GET'])
    api.add_resource(PolicyResource, '/policies')
    api.add_resource(SinglePolicyResource, '/policies/<int:policy_id>')
    api.add_resource(CommentResource, '/policies/<int:policy_id>/comments')
    api.add_resource(SingleCommentResource, '/comments/<int:comment_id>')
    api.add_resource(PollListResource, '/polls')
    api.add_resource(PollResource, '/polls/<int:poll_id>')
    api.add_resource(QuestionListResource, '/polls/<int:poll_id>/questions')
    api.add_resource(QuestionResource, '/questions/<int:question_id>')
    api.add_resource(OptionListResource, '/questions/<int:question_id>/options')
    api.add_resource(OptionResource, '/options/<int:option_id>')
    api.add_resource(PolicyLikeResource, '/policies/<int:policy_id>/like')
    api.add_resource(PolicyDislikeResource, '/policies/<int:policy_id>/dislike')
    api.add_resource(QAPostResource, '/qa_posts')
    api.add_resource(QAPostListResource, '/qa_list', methods=['GET', 'POST'])
    api.add_resource(AnswerResource,'/answers/<int:answer_id>')
    api.add_resource(AnswerListResource,'/answers/<int:question_id>/list')




    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0',port=5000, debug=True)

