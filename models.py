from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import check_password_hash

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# initialize metadata
metadata = MetaData(naming_convention = convention)

db = SQLAlchemy(metadata = metadata)

# define models
class Student(db.Model, SerializerMixin):
    # define table
    __tablename__ = "students"

    # define columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.Text, nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP)

    results = db.relationship('Result', back_populates="student")
    """
    When implementing a one to one rltship we need to add
    uselist=False option.
    """
    # result = db.relationship('Result', uselist=False)

    serialize_rules = ('-results.student',)

class Result(db.Model, SerializerMixin):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    student = db.relationship('Student', back_populates="results")
    course = db.relationship('Course', back_populates="results")

    # prevent student from loading results
    serialize_rules = ('-student.results','-course.results')
    # select specific fields
    serialize_only = ('id', 'marks', 'student', 'course')

class Course(db.Model, SerializerMixin):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date)

    results = db.relationship('Result', back_populates="course")
    students = association_proxy('results', 'student',
                                 creator=lambda student: Result(student = student))

    serialize_rules = ('-results.course',)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.Text)
    password = db.Column(db.String)

    serialize_rules = ('-password',)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)
