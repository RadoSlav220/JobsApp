import hashlib


def consistent_hash(input_string) -> str:
    input_bytes = input_string.encode('utf-8')
    hashed_bytes = hashlib.sha256(input_bytes).digest()
    hashed_hex = hashlib.sha256(input_bytes).hexdigest()
    return hashed_hex