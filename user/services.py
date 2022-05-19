from user.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from common.tokens import AuthBackend


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
        password_token = User.generate_password()
        password = make_password(password_token)
        return {"password": password, "password_token": password_token}

    """ Create new user """

    @staticmethod
    def user_register(name, email, password, expires_at):
        user = User(name=name, email=email, password=password, expires_at=expires_at)
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
                name,
                email,
                password_dict["password"],
                expires_at=datetime.now() + timedelta(minutes=10),
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
        expired_check = UserAuthServices.user_is_expired(email)
        if expired_check == True:
            User.objects.get(email=email).delete()
            return {
                "data": "User is expired please re register",
                "status": HTTP_400_BAD_REQUEST,
            }
        is_authenticated = authenticate(username=email, password=password)
        if is_authenticated:
            tokens = AuthBackend.generate_tokens(email=email)
            return tokens
        else:
            return False

    @staticmethod
    def refresh_token(access_token):
        return AuthBackend.generate_refresh_token(access_token=access_token)

    @staticmethod
    def user_is_expired(email):
        user = User.objects.get(email=email)
        return user.is_expired()
