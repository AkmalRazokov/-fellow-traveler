from passlib.hash import bcrypt
import os
os.environ["PASSLIB_BCRYPT_FORCE_BACKEND"] = "builtin"


def hash_password(password):
    return bcrypt.hash(password)

def verify_password(password, hashed_password):
    return bcrypt.verify(password, hashed_password)