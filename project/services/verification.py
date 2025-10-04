
# import secrets

# verification_codes = {}

# def generate_verification_code():
#     return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

# def assign_code(phone: str):
#     code = generate_verification_code()
#     verification_codes[phone] = code
#     return code

# def check_code(phone: str, code: str):
#     return verification_codes.get(phone) == code



from datetime import datetime, timedelta
import secrets

verification_codes = {}

def generate_verification_code():
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def assign_code(phone: str):
    code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=5)  # код действует 5 минут
    verification_codes[phone] = {"code": code, "expires_at": expires_at}
    return code
def check_code(phone: str, code: str):
    entry = verification_codes.get(phone)
    if not entry:
        return False
    if entry["expires_at"] < datetime.utcnow():
        verification_codes.pop(phone, None)  # удаляем устаревший код
        return False
    return entry["code"] == code

    