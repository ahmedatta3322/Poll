from user.models import User, Password
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate


class UserCreationServices:

    """ User creation errors """

    responses = {
        "password_creation_error": "Password creation error , the error is {e} ",
        "user_creation_error": "User creation error , the error is {e} ",
        "email_error": "Email sending error , the error is {e} ",
    }
    """ Email services errors """
    email = {
        "subject": "User registration",
        "message": "Your password is: {password}",
        "from_email": "ahmedatta3322@gmail.com",
    }

    """ Create new OTP """

    @staticmethod
    def create_password():
        password_token = Password.generate_password()
        password = Password.objects.create(
            password=make_password(password_token),
            expires_at=datetime.now() + timedelta(minutes=10),
        )
        return {"password": password, "password_token": password_token}

    """ Create new user """

    @staticmethod
    def user_register(name, email, password):
        user = User(name=name, email=email, password=password)
        user.save()
        return user

    """ User creation process
    1- Create new password
    2- Create new user
    3- Send email with password
    """

    @staticmethod
    def user_process(name, email):
        try:
            password_dict = UserCreationServices.create_password()
        except Exception:
            return {
                "data": UserCreationServices.responses[
                    "password_creation_error"
                ].format(e=e),
                "status": HTTP_400_BAD_REQUEST,
            }
        try:
            user = UserCreationServices.user_register(
                name, email, password_dict["password"]
            )
        except Exception as e:
            return {
                "data": UserCreationServices.responses["user_creation_error"].format(
                    e=e
                ),
                "status": HTTP_400_BAD_REQUEST,
            }
        try:
            User.email_user(
                self=user,
                subject=UserCreationServices.email["subject"],
                message=UserCreationServices.email["message"].format(
                    password=password_dict["password_token"]
                ),
                from_email=UserCreationServices.email["from_email"],
            )
        except Exception as e:
            return {
                "data": UserCreationServices.responses["email_error"].format(e=e),
                "status": HTTP_400_BAD_REQUEST,
            }
        return {"data": "User created successfully", "status": HTTP_200_OK}


""" User login process """


class UserAuthServices:

    """ User login errors"""

    @staticmethod
    def user_login(email, password):
        is_authenticated = authenticate(email=email, password=password)
        print(is_authenticated)
        return {"data": "User logged in successfully", "status": HTTP_200_OK}
