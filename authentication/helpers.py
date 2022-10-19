import hashlib
from handonvitals.settings import DEFAULT_CHARSET, HASH_SALT


def hash_code(code: str):
    salt = HASH_SALT
    default_encoding = DEFAULT_CHARSET
    code_hash = hashlib.sha256(salt.encode(default_encoding) + code.encode(default_encoding)).hexdigest()
    return code_hash
