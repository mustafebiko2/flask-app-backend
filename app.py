import os
from datetime import timedelta

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from models import db, User
from resources.student import StudentResource
from resources.course import CourseResource, CourseStudentsResource
from resources.user import SignupResource, LoginResource

app = Flask(__name__)
api = Api(app)
# configure db connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_ECHO'] = True
# JWT configs
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
# Access tokens should be short lived, this is for this phase only
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# setup cors
CORS(app)

# setup migration tool
migrate = Migrate(app, db, render_as_batch=True)

# link our app with the db
db.init_app(app)

# initialize bcrypt
bcrypt = Bcrypt(app)

# setup jwt
jwt = JWTManager(app)

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     user = User.query.filter_by(id=identity).one_or_none()

#     if user:
#         return user.to_dict()

#     return None

class HelloWorld(Resource):
    def get(self):
        return { "message": "Hello world" }

api.add_resource(HelloWorld, '/')
# PATCH -> /students/1
# DELETE -> /students/1
# GET one -> /student/1
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(StudentResource, '/students', '/students/<int:id>')
api.add_resource(CourseResource, '/courses', '/courses/<int:id>')
api.add_resource(CourseStudentsResource, '/courses/<int:course_id>/students')
