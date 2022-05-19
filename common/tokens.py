from datetime import datetime, timedelta
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import jwt
from decouple import config
from django.contrib.auth.backends import BaseBackend
from user.models import User


class AuthBackend(BaseBackend):
    def authenticate(request, token):
        if AuthBackend.check_expiry(token):
            try:
                decoded_token = jwt.decode(
                    token, config("SECRET_KEY"), algorithms=["HS256"]
                )
                email = decoded_token["auth_user"]["email"]
                user = User.objects.get(email=email)
                return user
            except jwt.InvalidTokenError:
                print("i'm none")
                return None

    def get_user(self, user_id):
        print("user_id")
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def access_token(email):
        expires_in = datetime.now() + timedelta(
            seconds=int(config("ACCESS_EXPIRES_IN"))
        )
        expire_stamp = expires_in.timestamp()
        encoded_jwt = jwt.encode(
            {"auth_user": {"email": email, "expires_at": expire_stamp}},
            config("SECRET_KEY"),
            algorithm="HS256",
        )
        return encoded_jwt

    def refresh_token(email):
        expires_in = datetime.now() + timedelta(
            seconds=int(config("REFRESH_EXPIRES_IN"))
        )
        expire_stamp = expires_in.timestamp()
        encoded_jwt = jwt.encode(
            {"auth_user": {"email": email, "expires_at": expire_stamp}},
            config("SECRET_KEY"),
            algorithm="HS256",
        )
        return encoded_jwt

    def check_expiry(token):
        try:
            decoded_token = jwt.decode(
                token, config("SECRET_KEY"), algorithms=["HS256"]
            )
            expiry_date = datetime.fromtimestamp(
                decoded_token["auth_user"]["expires_at"]
            )

            if expiry_date > datetime.now():
                return True
            return False
        except jwt.ExpiredSignatureError:
            return False

    def generate_tokens(email):
        access = AuthBackend.access_token(email)
        refresh = AuthBackend.refresh_token(email)
        return {"access": access, "refresh": refresh}

    def generate_refresh_token(access_token):
        try:
            decoded_token = jwt.decode(
                access_token, config("SECRET_KEY"), algorithms=["HS256"]
            )
            if not AuthBackend.check_expiry(access_token):
                email = decoded_token["auth_user"]["email"]
                refresh = AuthBackend.refresh_token(email)
                return {"refresh": refresh}
            else:
                return {"data": "Token expired", "status": HTTP_400_BAD_REQUEST}
        except jwt.InvalidTokenError:
            return {"data": "Token is Invalid", "status": HTTP_400_BAD_REQUEST}
