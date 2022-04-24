import re

def verify_email(email:str) -> bool:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False

    return True

