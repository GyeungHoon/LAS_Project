import urllib
import uuid
import base64
from datetime import datetime, timezone, timedelta
import random
import os
import hashlib
from PIL import Image
import string

APP_VER = '49.2.0'

def generate_random_id():
    # UUID를 생성하고, '-'를 제거한 뒤 처음 16자리만 사용하여 길이를 제한합니다.
    random_id = str(uuid.uuid4()).replace('-', '')[:16]
    return random_id


# ro.hardware 값들의 리스트를 정의
ro_hardware_values = [
    "qcom", "mt6589", "exynos5",
    "msm7627a", "sdm845", "mt6735", "exynos9810", "kirin810",
    "helioX10", "apq8084", "mtk6797", "exynos8895",
    "snapdragon660", "helioP60", "exynos7885", "mt6765",
    "snapdragon765", "exynos9825", "mt6873",  "snapdragon888",
    "snapdragon730", "exynos9609", "mt6757",  "tegra4",
    "msm8937",  "mt6762", "exynos850", "kirin820", "apq8096", "mtk6885", "exynos980", "kirin985",
    "snapdragon865", "exynos990", "mt6875", "kirin1020", "snapdragon870",
    "exynos2100", "mt6893", "kirin9000", "snapdragon888Plus", "exynos1080"
]
# ro.hardware 값 중에서 랜덤하게 하나를 선택하여 반환하는 함수
def get_random_ro_hardware():
    return random.choice(ro_hardware_values)

phone_model_names = [
    "SM-N976N", "SM-G998B", "LM-V500N", "LM-G900N", "iPhone13,3",
    "Pixel 5", "M2007J3SG", "V2045", "LM-K500", "RMX2170",
    "SM-G975F", "M2102J20SG", "V2036", "21061111RG", "RMX2202",
    "SM-A505F", "CPH2025", "M1903F10G", "V2055A", "RMX3085",
    "SM-F916B", "CPH2005", "2107113SG", "M2012K11AG", "V2040",
    "iPhone12,1", "SM-G960F", "LM-X420", "RMX2001", "M1901F9E",
    "SM-A750GN", "V2031", "2106108C", "CPH1911", "M2101K9AG",
    "iPhone11,8", "SM-G981B", "LM-Q730", "RMX3031", "M1903C3GI",
    "SM-A515F", "V2046", "21081111RG", "CPH2127", "M2004J19C",
    "iPhone11,2", "SM-G986B", "LM-X320", "RMX2185", "M1901F7H"
]

# 핸드폰 단말명 중에서 랜덤하게 하나를 선택하여 반환하는 함수
def get_random_phone_model():
    import random
    return random.choice(phone_model_names)

def generate_device_id(seed, android_id):
    """안드로이드 디바이스 ID를 SEED 암호화합니다."""
    return seed.encode(android_id)

def generate_widevine_id(seed):
    """Widevine ID와 유사한 형태의 문자열을 생성하고 SEED 암호화합니다."""
    # 임의의 바이트 데이터를 Base64 인코딩
    random_bytes = generate_random_id().encode('utf-8')  # 이 예에서 generate_random_id()는 문자열을 반환합니다.
    base64_encoded = base64.b64encode(random_bytes).decode('utf-8')

    # Base64 인코딩된 문자열을 URL 인코딩
    url_encoded_widevine_id = urllib.parse.quote_plus(base64_encoded)

    # URL 인코딩된 값을 SEED 암호화
    encrypted_widevine_id = seed.encode(url_encoded_widevine_id)

    return url_encoded_widevine_id, encrypted_widevine_id


def generate_dt():
    # 현재 시간을 UTC 기준으로 가져온 후, KST로 변환 (+9시간)
    kst = timezone(timedelta(hours=9))
    current_time = datetime.now(kst)

    # 지정된 포맷으로 시간을 문자열로 변환
    dt_format = current_time.strftime('%Y%m%d%H%M%S%z')

    # '%z' 포맷은 '+0900' 형태로 변환되므로 공백 없이 직접 반환
    return dt_format

def create_thumbnail(file_path, thumbnail_size=(72, 72)):
    # 파일 이름에서 확장자를 제외하고 썸네일 파일명을 지정
    thumbnail_file_path = f"{os.path.splitext(file_path)[0]}_thumb.jpg"

    # 원본 이미지를 열어서 썸네일 생성
    with Image.open(file_path) as img:
        img.thumbnail(thumbnail_size)
        img.save(thumbnail_file_path, "JPEG")

    return thumbnail_file_path


def generate_boundary(length=30):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_multipart_body(fields, boundary):
    try:
        lines = []
        for name, value in fields.items():
            lines.append(f'--{boundary}')
            lines.append(f'Content-Disposition: form-data; name="{name}"')
            lines.append('Content-Type: text/plain; charset=UTF-8')
            lines.append('Content-Transfer-Encoding: 8bit')
            lines.append('')
            lines.append(value)
        lines.append(f'--{boundary}--')
        lines.append('')
        body = '\r\n'.join(lines)
        return body
    except Exception as e:
        print(f"create_multipart_body 예외 : {e}")

def create_multipart_body_cheer_with_photo(fields, files, boundary, data):
    """
    멀티파트 본문을 생성하는 함수. 필드와 파일 데이터를 포함합니다.
    :param fields: 폼 데이터 필드 (예: 텍스트 데이터)
    :param files: 파일 데이터 (예: {'field_name': (filename, file_data)})
    :param boundary: 멀티파트 바운더리
    :return: 멀티파트 본문 (텍스트 데이터와 바이너리 데이터 결합)
    """
    lines = []

    # 랜덤 숫자 생성 (12~14자리)
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(random.randint(12, 14))])

    # 필드 데이터 처리 (텍스트 데이터)

    for name, value in fields.items():
        print(f"필드 데이터 처리 (텍스트 데이터) 내부 : {name}")
        lines.append(f'--{boundary}')
        lines.append(f'Content-Disposition: form-data; name="{name}"')
        lines.append('Content-Type: text/plain; charset=UTF-8')
        lines.append('Content-Transfer-Encoding: 8bit')
        lines.append('')  # 빈 줄로 헤더와 데이터를 구분
        lines.append(value)  # 텍스트 데이터는 그대로 추가 (인코딩 X)

    # 파일 데이터 처리 (썸네일 및 원본 파일)
    if files is not None:
        for name, file in files.items():
            print(f"파일 데이터 처리  (썸네일 및 원본 파일) 내부 : {name}")
            # 파일명 변경 - _org, _thumb 구분
            if "org" in name:
                # new_filename = f"{data.get("photo_key")}_org{os.path.splitext(file.name)[1]}"  # 확장자 유지
                new_filename = f"photo1_org{os.path.splitext(file.name)[1]}"  # 확장자 유지
            elif "thum" in name:
                # new_filename = f"{data.get("photo_key")}_thumb{os.path.splitext(file.name)[1]}"  # 확장자 유지
                new_filename = f"photo1_thumb{os.path.splitext(file.name)[1]}"  # 확장자 유지
            else:
                new_filename = f"{random_number}{os.path.splitext(file.name)[1]}"  # 기본 파일명

            file_data = file.read()  # 파일 내용을 바이너리로 읽기
            lines.append(f'--{boundary}')
            lines.append(f'Content-Disposition: form-data; name="{name}"; filename="{new_filename}"')
            lines.append(f'Content-Type: application/octet-stream')
            lines.append('Content-Transfer-Encoding: binary')
            lines.append('')  # 빈 줄로 헤더와 파일 데이터를 구분
            lines.append(file_data)  # 파일 데이터는 그대로 추가 (바이너리로 처리)

    # 마지막 바운더리 추가
    lines.append(f'--{boundary}--')
    lines.append('')

    # 최종적으로 텍스트 데이터와 바이너리 데이터를 한 번에 처리
    body = b''
    for line in lines:
        if isinstance(line, str):
            body += line.encode('utf-8') + b'\r\n'  # 텍스트는 UTF-8로 인코딩
        elif isinstance(line, bytes):
            body += line + b'\r\n'  # 파일 데이터는 그대로 추가

    return body

def create_multipart_body_photo_upload(fields, files, boundary, profilephoto=False):
    """
    멀티파트 본문을 생성하는 함수. 필드와 파일 데이터를 포함합니다.
    :param fields: 폼 데이터 필드 (예: 텍스트 데이터)
    :param files: 파일 데이터 (예: {'field_name': (filename, file_data)})
    :param boundary: 멀티파트 바운더리
    :return: 멀티파트 본문 (텍스트 데이터와 바이너리 데이터 결합)
    """
    lines = []

    # 랜덤 숫자 생성 (12~14자리)
    if profilephoto:
        random_number = 'profilephoto'
    else:
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(random.randint(12, 14))])

    # 필드 데이터 처리 (텍스트 데이터)
    for name, value in fields.items():
        print(f"필드 데이터 처리 (텍스트 데이터) 내부 : {name}")
        lines.append(f'--{boundary}')
        lines.append(f'Content-Disposition: form-data; name="{name}"')
        lines.append('Content-Type: text/plain; charset=UTF-8')
        lines.append('Content-Transfer-Encoding: 8bit')
        lines.append('')  # 빈 줄로 헤더와 데이터를 구분
        lines.append(value)  # 텍스트 데이터는 그대로 추가 (인코딩 X)

    # 파일 데이터 처리 (썸네일 및 원본 파일)
    if files is not None:
        for name, file in files.items():
            print(f"파일 데이터 처리  (썸네일 및 원본 파일) 내부 : {name}")
            # 파일명 변경 - _org, _thumb 구분
            if "org" in name:
                new_filename = f"{random_number}_org{os.path.splitext(file.name)[1]}"  # 확장자 유지
            elif "thumb" in name:
                new_filename = f"{random_number}_thum{os.path.splitext(file.name)[1]}"  # 확장자 유지
            else:
                new_filename = f"{random_number}{os.path.splitext(file.name)[1]}"  # 기본 파일명

            file_data = file.read()  # 파일 내용을 바이너리로 읽기
            lines.append(f'--{boundary}')
            lines.append(f'Content-Disposition: form-data; name="{name}"; filename="{new_filename}"')
            lines.append(f'Content-Type: application/octet-stream')
            lines.append('Content-Transfer-Encoding: binary')
            lines.append('')  # 빈 줄로 헤더와 파일 데이터를 구분
            lines.append(file_data)  # 파일 데이터는 그대로 추가 (바이너리로 처리)

    # 마지막 바운더리 추가
    lines.append(f'--{boundary}--')
    lines.append('')

    # 최종적으로 텍스트 데이터와 바이너리 데이터를 한 번에 처리
    body = b''
    for line in lines:
        if isinstance(line, str):
            body += line.encode('utf-8') + b'\r\n'  # 텍스트는 UTF-8로 인코딩
        elif isinstance(line, bytes):
            body += line + b'\r\n'  # 파일 데이터는 그대로 추가

    return body

def create_multipart_body_photo_profile_set(fields, files, boundary, profilephoto=False):
    """
    멀티파트 본문을 생성하는 함수. 필드와 파일 데이터를 포함합니다.
    :param fields: 폼 데이터 필드 (예: 텍스트 데이터)
    :param files: 파일 데이터 (예: {'field_name': (filename, file_data)})
    :param boundary: 멀티파트 바운더리
    :return: 멀티파트 본문 (텍스트 데이터와 바이너리 데이터 결합)
    """
    lines = []

    # 랜덤 숫자 생성 (12~14자리)
    if profilephoto:
        random_number = 'profilephoto'
    else:
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(random.randint(12, 14))])

    # 필드 데이터 처리 (텍스트 데이터)
    for name, value in fields.items():
        print(f"필드 데이터 처리 (텍스트 데이터) 내부 : {name}")
        lines.append(f'--{boundary}')
        lines.append(f'Content-Disposition: form-data; name="{name}"')
        lines.append('Content-Type: text/plain; charset=UTF-8')
        lines.append('Content-Transfer-Encoding: 8bit')
        lines.append('')  # 빈 줄로 헤더와 데이터를 구분
        lines.append(value)  # 텍스트 데이터는 그대로 추가 (인코딩 X)

    # 파일 데이터 처리 (썸네일 및 원본 파일)
    if files is not None:
        for name, file in files.items():
            print(f"파일 데이터 처리  (썸네일 및 원본 파일) 내부 : {name}")
            # 파일명 변경 - _org, _thumb 구분
            if "org" in name:
                new_filename = f"{random_number}_org{os.path.splitext(file.name)[1]}"  # 확장자 유지
            elif "thum" in name:
                new_filename = f"{random_number}_thumb{os.path.splitext(file.name)[1]}"  # 확장자 유지
            else:
                new_filename = f"{random_number}{os.path.splitext(file.name)[1]}"  # 기본 파일명

            file_data = file.read()  # 파일 내용을 바이너리로 읽기
            lines.append(f'--{boundary}')
            lines.append(f'Content-Disposition: form-data; name="{name}"; filename="{new_filename}"')
            lines.append(f'Content-Type: application/octet-stream')
            lines.append('Content-Transfer-Encoding: binary')
            lines.append('')  # 빈 줄로 헤더와 파일 데이터를 구분
            lines.append(file_data)  # 파일 데이터는 그대로 추가 (바이너리로 처리)

    # 마지막 바운더리 추가
    lines.append(f'--{boundary}--')
    lines.append('')

    # 최종적으로 텍스트 데이터와 바이너리 데이터를 한 번에 처리
    body = b''
    for line in lines:
        if isinstance(line, str):
            body += line.encode('utf-8') + b'\r\n'  # 텍스트는 UTF-8로 인코딩
        elif isinstance(line, bytes):
            body += line + b'\r\n'  # 파일 데이터는 그대로 추가

    return body