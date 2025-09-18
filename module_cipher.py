import requests
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import hashlib
from datetime import datetime, timedelta, timezone
from module_config import *

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
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted) + unpadder.finalize()
        return unpadded_data.decode('utf-8')

def generate_vh_value(post_data, dt_value, prefix="psynet0641"):
    # 비어 있지 않은 POST 데이터 항목의 값만 필터링하고 리스트로 변환
    filtered_values = [v for k, v in sorted(post_data.items()) if v]

    # 데이터 값들을 사전순으로 정렬된 상태로 연결
    sorted_data_string = "".join(filtered_values)

    # "psynet0641" 접두사와 dt 값 접미사 추가
    complete_string = f"{prefix}{sorted_data_string}{dt_value}"

    # SHA-512 해시 생성
    hash_object = hashlib.sha512(complete_string.encode())
    vh_value = hash_object.hexdigest()

    return vh_value

def generate_app_vfy(opcode, android_id, authcode):
    """app_vfy 해시 생성 함수."""
    # Kotlin 방식 문자열 조합
    target_str = f"{authcode}out:{APP_VER}anr:{android_id}Rhkd:{opcode}"

    # SHA-512 해시 입력 포맷: app_vfy:{문자열}:app_vfy
    full_str = f"app_vfy:{target_str}:app_vfy"

    # SHA-512 해시 후 base64 인코딩
    digest = hashlib.sha512(full_str.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("utf-8")



def calculate_md5_from_file(file_path):
    """
    파일의 MD5 해시를 로컬에서 계산합니다.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def generate_photo_key(file_path):
    """
    로컬에서 photo_key를 생성합니다.
    """
    if not os.path.exists(file_path):
        return None

    # MD5 해시 계산
    md5 = calculate_md5_from_file(file_path)

    # 파일 크기 (KB 단위)
    file_size = str(int(os.path.getsize(file_path) / 1024))

    # UTC 타임스탬프 (밀리초 단위)
    mod_time = str(int((datetime.now(timezone.utc)).timestamp() * 1000))

    # photo_key 생성
    photo_key = "_".join([md5, file_size, mod_time])

    return photo_key



def generate_goc(key: str = '@tlrksdjedjdhrl@') -> str:
    # 현재 시간 (KST 기준)
    now_kst = datetime.now(timezone(timedelta(hours=9)))

    # 기준 시간: 현재 UTC - 8시간
    logical_time_ts = int(now_kst.timestamp())

    # 로그 출력
    # print(f"[현재 UTC ] {now_utc.strftime('%Y-%m-%d %H:%M:%S')} (timestamp: {int(now_utc.timestamp())})")
    # print(f"[현재 KST ] {now_kst.strftime('%Y-%m-%d %H:%M:%S')}")
    # print(f"[logical_server_time UTC ] {logical_time_utc.strftime('%Y-%m-%d %H:%M:%S')} (timestamp: {logical_time_ts})")
    # print(f"[logical_server_time KST ] {logical_time_kst.strftime('%Y-%m-%d %H:%M:%S')}")

    seed = SEED128(key, key)
    return seed.encode(str(logical_time_ts))

