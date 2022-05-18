import jwt
from decouple import config


def access_token(email, password):
    expires_in = config("ACCESS_EXPIRES_IN")
    encoded_jwt = jwt.encode(
        {"auth_user": {"email": email, "password": password}},
        config("SECRET_KEY"),
        algorithm="HS256",
    )
    return {"access_token": encoded_jwt, "expiry": expires_in}
def refresh_token(email, password):
    expires_in = config("REFRESH_EXPIRES_IN")
    encoded_jwt = jwt.encode(
        {"auth_user": {"email": email, "password": password}},
        config("SECRET_KEY"),
        algorithm="HS256",
    )
    return {"refresh_token": encoded_jwt, "expiry": expires_in}