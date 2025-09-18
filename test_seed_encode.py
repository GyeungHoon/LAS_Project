from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

class SEED128:
    def __init__(self, iv, key):
        self.iv = bytes(iv, encoding='utf-8')
        self.key = bytes(key, encoding='utf-8')
        self.cipher = Cipher(algorithms.SEED(self.key), modes.CBC(self.iv), backend=default_backend())

    def encode(self, text):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(bytes(text, 'utf-8')) + padder.finalize()
        encryptor = self.cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted).decode('utf-8')

    def decode(self, encrypted_data):
        decryptor = self.cipher.decryptor()
        decrypted = decryptor.update(base64.b64decode(encrypted_data)) + decryptor.finalize()
        # print(f"Decrypted (before unpadding): {decrypted}")
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted) + unpadder.finalize()
        return unpadded_data.decode('utf-8')

# SEED key
seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')
# seed = SEED128('psynet2020083101', 'psynet2020083101')


# Decoding the provided strings
Encoded_strings = [
    '0cd9cde0c82048e9',
]

for index, decoded in enumerate(Encoded_strings, start=1):
    try:
        encode = seed.encode(decoded)
        print(f"{index:02d}. Encoded strings : {encode}")
        # print(f"{index:02d}. encoded string: {decoded}")
    except Exception as e:
        print(f"{index:02d}. Failed to encode {decoded}: {e}")
