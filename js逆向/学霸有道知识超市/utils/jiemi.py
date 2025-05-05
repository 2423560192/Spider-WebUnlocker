import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64


def decrypt(encrypted_text, key="zhl@k*^5f45H$r3*"):
    # Convert key to UTF-8 bytes
    key = key.encode('utf-8')

    # Assuming encrypted_text is base64 encoded (common for AES encrypted data)
    # If it's not base64 encoded in your use case, remove the decoding
    cipher_text = base64.b64decode(encrypted_text)

    # Create AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt and remove padding
    decrypted = cipher.decrypt(cipher_text)
    decrypted_text = unpad(decrypted, AES.block_size)

    return json.loads(decrypted_text.decode('utf-8'))
