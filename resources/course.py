from flask_restful import Resource
from models import Course

class CourseResource(Resource):
    def get(self, id = None):
        if id:
            course = Course.query.filter_by(id=id).first()

            if course:
                return course.to_dict()
            else:
                return { "message": "Course not found" }, 404

        else:
            courses = Course.query.all()

            results = []

            for course in courses:
                results.append(course.to_dict())

            return { "data": results, "items": len(results) }


class CourseStudentsResource(Resource):
    # get a list of students associated to a course
    def get(self, course_id):
        course = Course.query.filter_by(id = course_id).first()

        if course == None:
            return { "message": "Course not found" }, 404

        students = []

        for student in course.students:
            students.append(student.to_dict(rules=('-results',)))

        return students
