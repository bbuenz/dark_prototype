import hashlib


def hash_all(*argv, bits=120):
    m = hashlib.sha256()
    for arg in argv:
        m.update(str(arg).encode('utf-8'))
    digest = m.digest()
    return int.from_bytes(digest, 'big', signed=False) % 2 ** bits
