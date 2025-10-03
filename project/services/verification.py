
import secrets

verification_codes = {}

def generate_verification_code():
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def assign_code(phone: str):
    code = generate_verification_code()
    verification_codes[phone] = code
    return code

def check_code(phone: str, code: str):
    return verification_codes.get(phone) == code





# from datetime import datetime, timedelta

# # phone → {"code": str, "expires_at": datetime}
# verification_codes = {}

# # phone → datetime of last request
# verification_timestamps = {}

# CODE_LIFETIME = timedelta(minutes=5)
# REQUEST_INTERVAL = timedelta(minutes=1)
# # 