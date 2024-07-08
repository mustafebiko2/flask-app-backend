from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token
from models import db, User


class SignupResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help="Name is required")
    parser.add_argument('email', required=True,
                        help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data = self.parser.parse_args()

        # User.query.delete()

        data['password'] = generate_password_hash(
            data['password']).decode('utf-8')

        data['role'] = 'member'

        email = User.query.filter_by(email=data['email']).first()

        if email:
            return {"message": "Email address already taken", "status": "fail"}, 422

        user = User(**data)

        db.session.add(user)

        db.session.commit()

        return {"message": "User registered successfully", "status": "success", "user": user.to_dict()}


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True,
                        help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data = self.parser.parse_args()

        # 1. Try to retrieve user with provided email
        user = User.query.filter_by(email=data['email']).first()

        # 2. check if user exists
        if user:
            # 3. password verification
            is_password_match = user.check_password(data['password'])

            if is_password_match:
                user_dict = user.to_dict()
                additional_claims = { "role": user_dict['role'] }
                access_token = create_access_token(identity=user_dict['id'],
                                                   additional_claims=additional_claims)

                return {"message": "Login successful",
                        "status": "success",
                        "user": user_dict,
                        "access_token": access_token}
            else:
                return {"message": "Invalid email/password", "status": "fail"}, 403
        else:
            return {"message": "Invalid email/password", "status": "fail"}, 403
