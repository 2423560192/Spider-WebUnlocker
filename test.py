import hashlib


def hex_md5_utf16le(s: str) -> str:
    return hashlib.md5(s.encode('utf-16le')).hexdigest()


print(hex_md5_utf16le("123456"))
