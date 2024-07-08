from datetime import datetime
from app import app
from models import db, Student, Result, Course

with app.app_context():
    print("Start seeding...")
    Result.query.delete()
    Course.query.delete()
    Student.query.delete()

    print("Seeding courses")

    course = Course(name="Phase 4 Flask", duration="3 weeks", category="Software Engineering", created_at=datetime.now())

    db.session.add(course)
    db.session.commit()
    print("Finished seeding courses")

    print("Seeding student")

    new_students = []

    joseph = Student(first_name="Joseph", last_name="Mburu", email="joseph@gmail.com",phone="0712345677", age=19)

    new_students.append(joseph)

    cindy = Student(first_name="Cindy", last_name="Mutisya", email="cindy@gmail.com", phone="0712345679", age=20)
    new_students.append(cindy)

    db.session.add_all(new_students)
    db.session.commit()
    print("Students seeded")

    print("Seeding results")
    new_results = []

    result = Result(marks=0,student=joseph, course= course)
    new_results.append(result)
    result2 = Result(marks=0, student = cindy, course = course)
    new_results.append(result2)

    db.session.add_all(new_results)
    db.session.commit()

    print("results seeded")

    print("Database seeded")
