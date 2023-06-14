import os
from dotenv import load_dotenv
from myapp.authentications import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

load_dotenv()


def get_tokens_for_user(user):
    refresh_token = create_refresh_token(user.id)
    id = decode_refresh_token(refresh_token)
    refresh_access_token = create_access_token(id)

    return {
        "refresh": refresh_token,
        "access": refresh_access_token,
    }
