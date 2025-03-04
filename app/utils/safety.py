import bcrypt
import secrets


def generate_random_token() -> str:
    authenticator_token = secrets.token_hex(32)

    return authenticator_token


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    check_password = bcrypt.checkpw(password.encode(), hashed_password.encode())

    return check_password
