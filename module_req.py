from module_utils import *
from module_cipher import *
import time
import socket
import requests
import http.client
import urllib.parse
import socket
import random
import gzip
from io import BytesIO
import xml.etree.ElementTree as ET



def check_keywords_all(running_flag, selected_game_id, single_run, proxy_host, proxy_port):
    print(f"check_keywords_all 실행 중1- running_flag 상태: {running_flag()}")
    while running_flag() or single_run:
        # print(f"check_keywords_all 실행 중2 - running_flag 상태: {running_flag()}")
        print(f"check_keywords_all 시작")

        rh = get_random_ro_hardware()
        dt = generate_dt()
        goc = generate_goc()

        aid = '78fe52ff45564923'
        app_auth_key = 'YJGnZl+jrSYMf3SGamwJ8GuT4tFCh/WgzlKmQIl6+M4DOaXaaYPqW9cqb1fGQqTr'

        # 쿼리 파라미터 변수
        os = 'android'
        rt = 'N'
        opcode = '00020016'

        app_vfy = generate_app_vfy(opcode, aid, app_auth_key)

        # 쿼리 파라미터 항목 나열
        query_params = {
            'rt': rt,
            'pk_sub': '2FVa240DLoB/EygcP6l1PTGM7bHS8WMbMfxWrVpmR84=',
            'os': os,
            'rh': rh,
            'opcode': opcode,
            'pk': 'MrExonqMtwmlLc7yeRn1BwHvS6sFeAOWts0NhFGypGY=',
        }

        # URL 구성
        base_url = 'psyappi.psynet.co.kr'
        path = '/LiveScoreController.jsp'
        full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

        # 헤더 변수
        # dt = '20240222164540+0900'
        content_type = 'application/x-www-form-urlencoded'
        host = 'psyappi.psynet.co.kr'
        psynet_port = '13003'
        connection = 'Keep-Alive'
        user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-N976N Build/PQ3B.190801.07281103)'
        accept_encoding = 'gzip'

        # 헤더 설정 (Date 헤더 사용)
        headers = {
            "dt": dt,
            "Content-Type": content_type,
            "Host": f"{host}:{psynet_port}",
            "Connection": connection,
            "User-Agent": user_agent,
            "Accept-Encoding": accept_encoding,
        }

        # POST 데이터 변수
        post_data = {
            'national_code': 'KR',
            'mo': 'SM-G950N',
            'os_ver': '28',
            'nt': 'KT',
            'search_country_code': '',
            'pageKey': '',
            'mac': '02:00:00:00:00:00',
            'app_auth_key': app_auth_key,
            'user_no': 'DO9Wtm+hCxY79KquKYMtSA==',
            'away_id': 'N000284',
            'language_code': 'KO',
            'h_gmt': '+0900',
            'compe': 'etc',
            'search_flag': '0',
            'app_ver': APP_VER,
            'ph': 'vAnvV3RiylPsd78unVhGzw==',
            'app_vfy': app_vfy,
            'goc': goc,
            'home_id': 'N000283',
            'aid': aid,
            'game_id': 'P20200205155738507'
        }

        # vh 값을 동적으로 계산
        vh = generate_vh_value(post_data, dt)

        # 데이터 인코딩 (vh 값을 post_data에 추가한 후 인코딩)
        post_data['vh'] = vh
        data = urllib.parse.urlencode(post_data).encode()

        # HTTPConnection 객체 생성 및 요청 보내기

        try:
            if proxy_host and proxy_port:
                conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
                conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
            else:
                conn = http.client.HTTPConnection(host, 13003, timeout=5)

            conn.request("POST", full_path, body=data, headers=headers)

            # 응답 받기
            response = conn.getresponse()

            # 응답 본문 처리
            response_content = response.read()
            if response.getheader('Content-Encoding') == 'gzip':
                buffer = BytesIO(response_content)
                with gzip.open(buffer, 'rb') as f:
                    response_text = f.read().decode('utf-8')
            else:
                response_text = response_content.decode('utf-8')

            print(f" response_text : {response_text}")

            # 응답 데이터에서 game_id에 맞는 <list> 항목들만 필터링
            root = ET.fromstring(response_text)
            filtered_items = []

            # 각 <list> 항목을 순회하며 <gameId>를 확인
            for item in root.findall('.//list'):
                game_id = item.find('gameId').text if item.find('gameId') is not None else None

                # game_id가 입력되지 않았거나, 특정 game_id와 일치하는 항목만 추가
                if selected_game_id is None or selected_game_id == game_id:
                    filtered_items.append(item)

            # 필터링된 <list> 항목들로 새 XML 데이터 생성
            if filtered_items:
                filtered_root = ET.Element('Response')  # 새 XML 루트 노드 생성
                header = root.find('.//Header')  # 원본 응답의 Header 복사
                if header is not None:
                    filtered_root.append(header)
                data_element = ET.SubElement(filtered_root, 'Data')  # Data 태그 생성
                for filtered_item in filtered_items:
                    data_element.append(filtered_item)

                # 필터링된 XML을 문자열로 변환 후 전달
                filtered_response = ET.tostring(filtered_root, encoding='utf-8', method='xml').decode('utf-8')
                keyword_manager.check_response(filtered_response)
                #fixme 프로젝트에 알맞게 수정 필요
                # 기존 코드의 경우 결과 값을 keyword_manager.check_response로 넘겨 가공이 이루어졌음(화면에 뿌려주는 등)



                # print(f"check_keywords_all 내부에서 selected_game_id: {selected_game_id}")
                # print(f"filtered_response: {filtered_response}")


        except Exception as e:
            print(f"check_keywords_all 오류: {e}")
        finally:
            conn.close()

        if single_run:
            break

        # 주기적으로 요청을 보내기 위해 대기
        time.sleep(check_interval)
        #fixme 프로젝트에 알맞게 수정 필요
        # check_keywords_all은 라스에 올라오는 응원글을 지속적으로 스캔해야함, check_interval = 스캔 인터벌

def check_keywords_analysis_game(running_flag, proxy_host, proxy_port):
    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # ph 값 설정
    phone_number = '010' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    ph = seed.encode(phone_number)

    pk = 'qZ1P8EsW2ROsZuH9ktG4Fw=='
    rh = get_random_ro_hardware()
    pk_sub = generate_widevine_id(seed)[1]
    dt = generate_dt()
    goc = generate_goc()

    # 쿼리 파라미터 변수
    os = 'android'
    rt = 'N'
    opcode = '00020000'

    # app_vfy = generate_app_vfy(opcode, '', '')

    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': os,
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': rh,
        'rt': rt,
        'opcode': opcode,
    }

    # URL 구성
    base_url = 'psyappi.psynet.co.kr'
    path = '/LiveScoreController.jsp'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

    # 헤더 변수
    # dt = '20240222164540+0900'
    content_type = 'application/x-www-form-urlencoded'
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-N976N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    # 헤더 설정 (Date 헤더 사용)
    headers = {
        "dt": dt,
        "Content-Type": content_type,
        "Host": f"{host}:{psynet_port}",
        "Connection": connection,
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
    }

    # POST 데이터 변수
    post_data = {
        'aid': '2x0eiam835ns8cb',
        'app_auth_key': '',
        'app_ver': APP_VER,
        'app_vfy': 'CSKudB0ImY9ehwOlPerZQt2Wr3KVAuE/43UoIqsM8pA18h/M8cly+T4S53auEKx7p4JDXlPeCEt97kcS0QecrA==',
        'away_id': 'N000502',
        'compe': 'etc',
        'game_id': 'P20200413230618730',
        'h_gmt': '+0900',
        'home_id': 'N000995',
        'language_code': 'KO',
        'mac': '02:00:00:00:00:00',
        'mo': 'SM-G781N',
        'national_code': 'KR',
        'nt': 'KT',
        'os_ver': '28',
        'pageKey': '',
        'ph': 'vAnvV3RiylPsd78unVhGzw==',
        'search_country_code': '',
        'search_flag': '0',
        'user_no': '0',
    }

    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가한 후 인코딩)
    post_data['vh'] = vh
    data = urllib.parse.urlencode(post_data).encode()

    # HTTPConnection 객체 생성 및 요청 보내기
    while running_flag():
        try:
            if proxy_host and proxy_port:
                conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
                conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
            else:
                conn = http.client.HTTPConnection(host, 13003, timeout=5)

            conn.request("POST", full_path, body=data, headers=headers)

            # 응답 받기
            response = conn.getresponse()

            # 응답 본문 처리
            response_content = response.read()
            if response.getheader('Content-Encoding') == 'gzip':
                buffer = BytesIO(response_content)
                with gzip.open(buffer, 'rb') as f:
                    response_text = f.read().decode('utf-8')
            else:
                response_text = response_content.decode('utf-8')

            # print(f" response_text : {response_text}")

            # XML 응답에서 처리
            root = ET.fromstring(response_text)
            keyword_manager.check_response(response_text)

        except Exception as e:
            print(f"check_keywords_analysis_game 오류: {e}")
        finally:
            conn.close()

        # 주기적으로 요청을 보내기 위해 대기
        time.sleep(check_interval)

# 닉네임 변경
def update_nickname(proxy_host, proxy_port, account_info):
    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # ph 값 설정
    phone_number = '010' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    ph = seed.encode(phone_number)
    pk = seed.encode(account_info.get('aid'))
    rh = get_random_ro_hardware()
    pk_sub = generate_widevine_id(seed)[1]
    dt = generate_dt()
    goc = generate_goc()


    # 쿼리 파라미터 변수
    os = 'android'
    rt = 'N'
    opcode = '00000003'

    app_vfy = generate_app_vfy(opcode, account_info.get('aid'), account_info.get('authcode'))

    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': os,
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': rh,
        'rt': rt,
        'opcode': opcode,
    }

    # URL 구성
    base_url = 'psyappi.psynet.co.kr'
    path = '/LiveScoreController.jsp'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

    # 헤더 변수
    # dt = '20240222164540+0900'
    content_type = 'application/x-www-form-urlencoded'
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-N976N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    # 헤더 설정 (Date 헤더 사용)
    headers = {
        "dt": dt,
        "Content-Type": content_type,
        "Host": f"{host}:{psynet_port}",
        "Connection": connection,
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
    }

    # POST 데이터 변수
    post_data = {
        'aid': account_info.get('aid'),
        'app_auth_key': account_info.get('authcode'),
        'app_ver': APP_VER,
        'app_vfy': app_vfy,
        'goc': goc,
        'h_gmt': '+0900',
        'language_code': 'KO',
        'mac': '02:00:00:00:00:00',
        'mo': account_info.get('mo'),
        'national_code': 'KR',
        'nt': account_info.get('nt', 'SKTelecom'),
        'os_ver': account_info.get('os_ver'),
        'ph': ph,
        'profile_country_code': '',
        'user_id': account_info.get('new_user_id'),
        'user_no': account_info.get('user_no'),
    }

    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가한 후 인코딩)
    post_data['vh'] = vh
    data = urllib.parse.urlencode(post_data).encode()


    # HTTPConnection 객체 생성 및 요청 보내기
    try:
        if proxy_host and proxy_port:
            conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
            conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
        else:
            conn = http.client.HTTPConnection(host, 13003, timeout=5)

        conn.request("POST", full_path, body=data, headers=headers)

        print(f"[디버깅_5] request data: {data}, headers: {headers}")

        # 응답 받기
        response = conn.getresponse()
        print(f"[디버깅_5] number_check Status: {response.status}, Reason: {response.reason}")

        # 응답 본문 처리
        response_content = response.read()
        if response.getheader('Content-Encoding') == 'gzip':
            buffer = BytesIO(response_content)
            with gzip.open(buffer, 'rb') as f:
                response_text = f.read().decode('utf-8')
        else:
            response_text = response_content.decode('utf-8')

        print(f"[디버깅_5] response_text: {response_text}")

        # XML 응답에서 idx 추출
        root = ET.fromstring(response_text)
        bbsNo_list = [elem.text for elem in root.findall(".//bbsNo")]
        # print(f"Extracted bbsNo: {bbsNo_list}")

        # XML 응답 파싱
        root = ET.fromstring(response_text)
        # msg 태그의 내용을 찾기
        msg_text = root.find(".//msg").text if root.find(".//msg") is not None else ""
        # print(f"[디버깅_5] number_check msg_text : {msg_text}")

    except socket.timeout:
        print(f"[디버깅_5] number_check The request timed out after 3 seconds.")
        return {"status": "timeout", "reason": "Request timed out", "response_text": ""}

    # 연결 닫기
    finally:
        conn.close()

        # 메시지 반환
        return {"status": response.status, "reason": response.reason, "response_text": response_text,
                "bbsNo_list": bbsNo_list}

# OPCODE:00000000
def user_login_request(account_info, proxy_host, proxy_port):
    print("[user_login_request] 함수 시작")

    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # ph 값 설정
    phone_number = '010' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    ph = seed.encode(phone_number)

    pk = seed.encode(account_info.get('aid'))
    rh = get_random_ro_hardware()
    pk_sub = generate_widevine_id(seed)[1];
    dt = generate_dt()
    goc = generate_goc()

    # 쿼리 파라미터 변수
    os = 'android'
    rt = 'N'
    opcode = '00000000'

    app_vfy = generate_app_vfy(opcode, account_info.get('aid'), account_info.get('authcode'))


    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': os,
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': rh,
        'rt': rt,
        'opcode': opcode,
    }

    # URL 구성
    base_url = 'psyappi.psynet.co.kr'
    path = '/LiveScoreController.jsp'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

    # 헤더 변수
    # dt = '20240222164540+0900'
    content_type = 'application/x-www-form-urlencoded'
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-N976N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    # 헤더 설정 (Date 헤더 사용)
    headers = {
        "dt": dt,
        "Content-Type": content_type,
        "Host": f"{host}:{psynet_port}",
        "Connection": connection,
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
    }

    # POST 데이터 변수
    post_data = {
        'aid': account_info.get('aid'),
        'aniinfo_version': '1.9',
        'app_auth_key': account_info.get('authcode'),
        'app_ver': APP_VER,
        'h_gmt': '+0900',
        'imgcacheinfo_version': '1.1',
        'language_code': 'KO',
        'mac': '02:00:00:00:00:00',
        'mo': account_info.get('mo'),
        'national_code': 'KR',
        'nt': account_info.get('nt', 'SKTelecom'),
        'os_ver': account_info.get('os_ver'),
        'ph': ph,
        'app_vfy': app_vfy,
        'goc': goc,
        'push_key': account_info.get('push_key'),
         'push_type': '4',
        'rank_version': '37.4',
        'user_no': account_info.get('user_no'),
    }

    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가한 후 인코딩)
    post_data['vh'] = vh
    data = urllib.parse.urlencode(post_data).encode()

    # HTTPConnection 객체 생성 및 요청 보내기
    try:
        if proxy_host and proxy_port:
            conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
            conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
        else:
            conn = http.client.HTTPConnection(host, 13003, timeout=5)

        conn.request("POST", full_path, body=data, headers=headers)

        # 응답 받기
        response = conn.getresponse()
        # print(f"[디버깅_5] user_login_request: {response.status}, Reason: {response.reason}")

        # 응답 본문 처리
        response_content = response.read()
        if response.getheader('Content-Encoding') == 'gzip':
            buffer = BytesIO(response_content)
            with gzip.open(buffer, 'rb') as f:
                response_text = f.read().decode('utf-8')
        else:
            response_text = response_content.decode('utf-8')

        # XML 응답 파싱
        root = ET.fromstring(response_text)
        # msg 태그의 내용을 찾기
        msg_text = root.find(".//msg").text if root.find(".//msg") is not None else ""
        # print(f"[디버깅_5] user_login_request response_text : {response_text}")
        # print(f"[디버깅_5] user_login_request msg_text : {msg_text}")

        # userId 태그의 내용을 찾기
        new_nickname = root.find(".//userId").text if root.find(".//userId") is not None else ""

    except socket.timeout:
        print(f"[디버깅_5] user_login_request The request timed out after 3 seconds.")
        return {"status": "timeout", "reason": "Request timed out", "response_text": ""}

    # 연결 닫기
    finally:
        conn.close()

    # 메시지 반환
    return {"status": response.status, "reason": response.reason, "response_text": response_text, "msg_text": msg_text, "new_nickname": new_nickname}

# 계정상태 확인
def check_account(account_info, proxy_host, proxy_port):
    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # ph 값 설정
    phone_number = '010' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    ph = seed.encode(phone_number)

    pk = seed.encode(account_info.get('aid'))
    rh = get_random_ro_hardware()
    pk_sub = generate_widevine_id(seed)[1]
    dt = generate_dt()
    goc = generate_goc()

    # 쿼리 파라미터 변수
    os = 'android'
    rt = 'N'
    opcode = '00000035'

    app_vfy = generate_app_vfy(opcode, account_info.get('aid'), account_info.get('authcode'))

    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': os,
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': rh,
        'rt': rt,
        'opcode': opcode,
    }

    # URL 구성
    base_url = 'psyappi.psynet.co.kr'
    path = '/LiveScoreController.jsp'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

    # 헤더 변수
    # dt = '20240222164540+0900'
    content_type = 'application/x-www-form-urlencoded'
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-N976N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    # 헤더 설정 (Date 헤더 사용)
    headers = {
        "dt": dt,
        "Content-Type": content_type,
        "Host": f"{host}:{psynet_port}",
        "Connection": connection,
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
    }

    # POST 데이터 변수
    post_data = {
        'aid': account_info.get('aid'),
        'app_auth_key': account_info.get('authcode'),
        'app_ver': APP_VER,
        'app_vfy': app_vfy,
        'goc': goc,
        'h_gmt': '+0900',
        'language_code': 'KO',
        'mac': '02:00:00:00:00:00',
        'mo': account_info.get('mo'),
        'national_code': 'KR',
        'nt': account_info.get('nt', 'SKTelecom'),
        'os_ver': account_info.get('os_ver'),
        'ph': ph,
        'user_no': account_info.get('user_no'),
    }

    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가한 후 인코딩)
    post_data['vh'] = vh
    data = urllib.parse.urlencode(post_data).encode()

    # HTTPConnection 객체 생성 및 요청 보내기
    try:
        if proxy_host and proxy_port:
            conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
            conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
        else:
            conn = http.client.HTTPConnection(host, 13003, timeout=5)

        conn.request("POST", full_path, body=data, headers=headers)

        # print(f"[디버깅] request data: {data}, headers: {headers}")

        # 응답 받기
        response = conn.getresponse()
        # print(f"[디버깅] number_check Status: {response.status}, Reason: {response.reason}")

        # 응답 본문 처리
        response_content = response.read()
        if response.getheader('Content-Encoding') == 'gzip':
            buffer = BytesIO(response_content)
            with gzip.open(buffer, 'rb') as f:
                response_text = f.read().decode('utf-8')
        else:
            response_text = response_content.decode('utf-8')

        print(f"[디버깅] check_account response_text: {response_text}")

        # XML 응답에서 user_id 추출
        root = ET.fromstring(response_text)
        user_id = root.find(".//user_id").text if root.find(".//user_id") is not None else None
        new_nickname = root.find(".//user_id").text if root.find(".//user_id") is not None else None

        # 계정 유효성 판단
        if new_nickname:
            return {"status": "valid", "user_id": user_id, "new_nickname": new_nickname, "response_text": response_text}
        else:
            return {"status": "invalid", "user_id": user_id, "new_nickname": new_nickname, "response_text": response_text}

    except socket.timeout:
        print(f"[디버깅] number_check The request timed out after 3 seconds.")
        return {"status": "timeout", "reason": "Request timed out"}

    # 연결 닫기
    finally:
        conn.close()

# 경기 일정 가져오기
def get_http_match_data(search_date, proxy_host, proxy_port):
    print("get_http_match_data 내부")

    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # 변수 값 설정
    # boundary = generate_boundary()

    aid = '78fe52ff45564923'
    app_ver = APP_VER
    betting_phrase_flag = 'Y'
    compe = ''
    country_code = 'KR'
    gmt_time = '+0900'
    h_gmt = '+0900'
    is_push_callback = 'N'
    kor_player_flag = ''
    language_code = 'KO'
    mac = '02:00:00:00:00:00'
    mo = 'SM-A710S'
    national_code = 'KR'
    nt = 'SKTelecom'
    os_ver = '28'
    ph = 'vAnvV3RiylPsd78unVhGzw=='
    search_date = search_date
    user_no = '0'

    pk = seed.encode(aid)
    pk_sub = generate_widevine_id(seed)[1]
    rh = 'apq8084'
    dt = generate_dt()
    goc = generate_goc()
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    opcode = '00080016'
    app_auth_key = 'YJGnZl+jrSYMf3SGamwJ8GuT4tFCh/WgzlKmQIl6+M4DOaXaaYPqW9cqb1fGQqTr'
    app_vfy = generate_app_vfy(opcode, aid, app_auth_key)

    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': 'android',
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': rh,
        'rt': 'N',
        'opcode': opcode,
    }

    # URL 구성
    path = '/LiveScoreController.jsp'
    # path = '/post'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

    post_data = {
        'national_code': national_code,
        'mo': mo,
        'os_ver': os_ver,
        'nt': nt,
        'kor_player_flag': kor_player_flag,
        'mac': mac,
        'app_auth_key': app_auth_key,
        'user_no': user_no,
        'language_code': language_code,
        'h_gmt': h_gmt,
        'compe': compe,
        'search_date': search_date,
        'country_code': country_code,
        'app_ver': app_ver,
        'ph': ph,
        'app_vfy': app_vfy,
        'goc': goc,
        'betting_phrase_flag': betting_phrase_flag,
        'is_push_callback': is_push_callback,
        'aid': aid,
        'gmt_time': gmt_time,
    }

    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가)
    post_data['vh'] = vh
    data = urllib.parse.urlencode(post_data).encode()

    # # 멀티파트 본문을 문자열로 생성 (기존 코드를 유지)
    # body = create_multipart_body(post_data, boundary)

    # 문자열을 UTF-8로 인코딩하여 바이트로 변환
    # encoded_body = body.encode('utf-8')

    # 요청 헤더 설정, 'Content-Length'에 인코딩된 본문의 길이를 사용
    headers = {
        "dt": dt,
        "Content-Type": f'application/x-www-form-urlencoded',
        "Host": f"{host}:{psynet_port}",
        "Connection": connection,
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
    }

    # HTTPConnection 객체 생성 및 요청 보내기
    try:
        if proxy_host and proxy_port:
            conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
            conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
        else:
            conn = http.client.HTTPConnection(host, 13003, timeout=5)

        conn.request("POST", full_path, body=data, headers=headers)
        # 초기화된 msg_text 변수
        msg_text = ""  # 이 줄을 추가

        # 인코딩된 바디와 헤더를 사용하여 POST 요청을 보냄
        # conn.request("POST", full_path, body=encoded_body, headers=headers)
        # conn.request("POST", full_path, body=data, headers=headers)

        # 응답 받기
        response = conn.getresponse()
        print(f"get_http_match_data Status: {response.status}, Reason: {response.reason}")

        # 응답 본문 처리
        response_content = response.read()

        # 응답 헤더에서 Content-Encoding 확인
        if response.getheader('Content-Encoding') == 'gzip':
            buffer = BytesIO(response_content)
            with gzip.open(buffer, 'rb') as f:
                response_text = f.read().decode('utf-8')
        else:
            response_text = response_content.decode('utf-8')

        conn.close()

        # print(f"get_http_match_data response_text: {response_text}")

        return response_text

        # XML 응답 파싱
        # root = ET.fromstring(response_text)
        # msg 태그의 내용을 찾기
        # result_code = root.find("./Header/ResultCode").text
        # ResultDes = root.find("./Header/ResultDes").text
        #
        # if result_code == "0000":
        #     conn.close()
        #     return {
        #         "status": "성공",
        #     }
        #
        # else:
        #     conn.close()
        #     return {
        #         "status": "에러, 알 수 없음",
        #     }




    except Exception as e:
        result = {"status": "예외발생"}
        print("예외 발생:", e)

        # 연결 닫기
        conn.close()

        return result

    # 응원글 작성

# 응원 답글 작성
def cheer_reply_request(data, proxy_host, proxy_port):
    print(f"[디버깅] cheer_reply_request 시작")


    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # 변수 값 설정
    boundary = generate_boundary()

    # ph 값 설정
    phone_number = '010' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    ph = seed.encode(phone_number)

    app_ver = APP_VER
    cheer_country_code = 'KR'
    diviedend_sc = 'S'
    font_color = data.get('font_color')
    gmt_time = '+0900'
    h_gmt = '+0900'
    language_code = 'KO'
    mac = '02:00:00:00:00:00'
    national_code = 'KR'
    predict_flag = 'L'
    # re_cheer_no = '0'
    search_country_code = 'KR'
    photo1 = 'photo1_org'
    photo1_key = data.get('photo_key')
    # to_user_no = '0'
    opcode = '00020001'

    pk = seed.encode(data.get('aid'))
    pk_sub = generate_widevine_id(seed)[1]
    dt = generate_dt()
    goc = generate_goc()
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': 'android',
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': data.get('rh'),
        'rt': 'N',
        'opcode': opcode,
    }

    app_vfy = generate_app_vfy(opcode, data.get('aid'), data.get('authcode'))

    # URL 구성
    path = '/LiveScoreController.jsp'
    # path = '/post'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

    # 멀티파트 요청 본문 구성을 위한 변수 및 값
    post_data = {
        'aid': data.get('aid'),
        'app_auth_key': data.get('authcode'),
        'app_ver': app_ver,
        'app_vfy': app_vfy,
        'goc': goc,
        'awayteam_id': data.get('away_team_id'),
        'cheer_country_code': cheer_country_code,
        'compe': data.get('compe'),
        'content': data.get('content'),
        'diviedend_sc': diviedend_sc,
        'font_color': font_color,
        'game_id': data.get('game_id'),
        'gmt_time': gmt_time,
        'h_gmt': h_gmt,
        'hometeam_id': data.get('home_team_id'),
        'language_code': language_code,
        'league_id': data.get('league_id'),
        'mac': mac,
        'match_date': data.get('match_date'),
        'match_time': data.get('match_time'),
        'mo': data.get('mo'),
        'national_code': national_code,
        'nt': data.get('nt'),
        'os_ver': data.get('os_ver'),
        'ph': ph,
    }


    # photo1과 photo1_key를 중간에 삽입하는 로직 (사진사용O, 사진검수O, 사진 선탱O 가 되어 있을 경우에만)
    if data.get("is_cheer_photo_used") and data.get("confirm_state") == "C" and data.get("photo_file_path") is not None:
        if photo1 is not None:
            post_data['photo1'] = photo1
        if photo1_key is not None:
            post_data['photo1_key'] = photo1_key

    # 나머지 데이터
    post_data.update({
        'predict_flag': predict_flag,
        're_cheer_no': data.get('cheer_no'), #답글에 사용하는것임으로 cheer_no그대로 사용
        'search_country_code': search_country_code,
        'team_id': data.get('team_id'),
        'to_user_no': data.get('to_user_no'),
        'to_user_id': data.get('to_user_id'),
        'user_no': data.get('user_no'),
    })



    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가)
    post_data['vh'] = vh

    print(f"체크포인트1 파일 부분 구성 직전 {post_data}")

    # 파일 부분 구성
    files = None
    if data.get("is_cheer_photo_used") and data.get("confirm_state") == "C" and data.get("photo_file_path") is not None:
        # 썸네일 파일과 원본 파일을 열어서 처리
        thumbnail_file_path = create_thumbnail(data.get("photo_file_path"))  # 썸네일 생성
        print(f"create_thumbnail 이후 photo_file_path: {data.get("photo_file_path")}")
        # 파일 객체를 열어서 전달
        with open(thumbnail_file_path, 'rb') as thumb_file, open(data.get("photo_file_path"), 'rb') as org_file:
            files = {
                'photo1_thum': thumb_file,  # 썸네일 파일 객체
                'photo1_org': org_file,  # 원본 파일 객체
            }

            print(f"체크포인트1 create_multipart_body_photo_upload 직전 {post_data}")

            print(f"체크포인트1 create_multipart_body_photo_upload 직전 files {files}")

            # post_data 값 출력
            print("post_data 리스트 값:")
            for key, value in post_data.items():
                print(f"{key}: {value}")

            # 멀티파트 본문을 문자열로 생성 (기존 코드를 유지)
            # body = HttpRequestManager.create_multipart_body(post_data, boundary)
            body = create_multipart_body_cheer_with_photo(post_data, files, boundary, data)
            print(f"체크포인트2 create_multipart_body_photo_upload 직후")

    else:
        # 멀티파트 본문을 문자열로 생성 (기존 코드를 유지)
        body = create_multipart_body(post_data, boundary)

        # 문자열을 UTF-8로 인코딩하여 바이트로 변환
        body = body.encode('utf-8')

    # 요청 헤더 설정, 'Content-Length'에 인코딩된 본문의 길이를 사용
    headers = {
        "dt": dt,
        # "Content-Length": str(len(encoded_body)),
        "Content-Length": str(len(body)),
        "Content-Type": f'multipart/form-data; boundary={boundary}',
        "Host": f"{host}:{psynet_port}",
        "Connection": connection,
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
    }

    # print(f"체크포인트3")

    try:
        if proxy_host and proxy_port:
            conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
            conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
        else:
            conn = http.client.HTTPConnection(host, 13003, timeout=5)

        # 인코딩된 바디와 헤더를 사용하여 POST 요청을 보냄
        # conn.request("POST", full_path, body=encoded_body, headers=headers)
        conn.request("POST", full_path, body=body, headers=headers)

        # 응답 받기
        response = conn.getresponse()
        print(f"Status: {response.status}, Reason: {response.reason}")

        # 응답 본문 처리
        response_content = response.read()

        # 응답 헤더에서 Content-Encoding 확인
        if response.getheader('Content-Encoding') == 'gzip':
            buffer = BytesIO(response_content)
            with gzip.open(buffer, 'rb') as f:
                response_text = f.read().decode('utf-8')
        else:
            response_text = response_content.decode('utf-8')

        # print(f"reply_auto_api_req response_text: {response_text}")

        print(f"\n"
                    f"[cheer_reply_request post_data]: {post_data}"
                    f"\n"
                    f"[cheer_reply_request response_text]: {response_text}")

        # XML 응답 파싱
        root = ET.fromstring(response_text)
        # msg 태그의 내용을 찾기
        msg_text = root.find(".//msg").text if root.find(".//msg") is not None else ""

        print(f"[cheer_reply_request response_text] msg_text : {msg_text}")
        print(f"----------------")

        # "성공여부 확인"
        if "성공" in msg_text:
            conn.close()
            return {
                "status": "성공",
            }

        elif "실패" in msg_text:
            conn.close()
            return {
                "status": "실패",
            }

        elif "200 OK" in response_text:
            conn.close()
            show_failure_popup(response_text)
            return {
                "status": "IP차단",
            }

        elif "차단" in msg_text:
            conn.close()
            show_failure_popup("금칙어(욕설, 음란, 광고 등) 포함]")
            return {
                "status": "금칙어",
            }

        elif "0002" in msg_text:
            conn.close()
            return {
                "status": "Restricted access service",
            }

        elif "중복" in msg_text:
            conn.close()
            # 실패 시 팝업으로 결과를 보여줌
            show_failure_popup("중복글")
            return {
                "status": "중복",
            }

        elif "차단" in response_text:
            conn.close()
            show_failure_popup("차단")
            return {
                "status": "차단",
            }

        else:
            conn.close()
            print(f"그외에러 response_text: {response_text}")
            # 실패 시 팝업으로 결과를 보여줌
            show_failure_popup(response_text)
            return {
                "status": "그외에러",
            }


    except Exception as e:
        result = {"status": "예외발생"}
        print("cheer_reply_request 예외 발생:", e)
        if 'response_text' in locals() and response_text is not None:
            show_failure_popup(response_text)

        if "timed out" in str(e).lower():
            print("⏳ 요청이 타임아웃되었습니다. 서버가 응답하지 않습니다.")
            show_failure_popup("time_out")



        # 연결 닫기
        conn.close()

        return result

# 응원글 작성
def writing_cheer_request(data, proxy_host, proxy_port):
    print("[writing_cheer_request] 함수 시작")

    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # 변수 값 설정
    boundary = generate_boundary()

    # ph 값 설정
    phone_number = '010' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    ph = seed.encode(phone_number)

    app_ver = APP_VER
    cheer_country_code = 'KR'
    diviedend_sc = 'S'
    font_color = data.get('font_color')
    gmt_time = '+0900'
    h_gmt = '+0900'
    language_code = 'KO'
    mac = '02:00:00:00:00:00'
    national_code = 'KR'
    predict_flag = 'L'
    re_cheer_no = '0'
    search_country_code = 'KR'
    to_user_no = '0'
    photo1 = 'photo1_org'
    photo1_key = data.get('photo_key')
    opcode = '00020001'

    pk = seed.encode(data.get('aid'))
    pk_sub = generate_widevine_id(seed)[1]
    dt = generate_dt()
    goc = generate_goc()
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': 'android',
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': data.get('rh'),
        'rt': 'N',
        'opcode': opcode,
    }

    app_vfy = generate_app_vfy(opcode, data.get('aid'), data.get('authcode'))

    # URL 구성
    path = '/LiveScoreController.jsp'
    # path = '/post'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"

    hometeam_id = selected_home_team_id
    awayteam_id = selected_away_team_id
    compe = selected_compe
    game_id = selected_game_id
    league_id = selected_league_id
    match_date = selected_match_date
    match_time = selected_match_time
    #fixme 위 변수들 기존에는 글로벌 변수 였으나, 함수를 가져오면서 연결된 참조값이 없음, 함수에 인자를 추가하거나 해야 될 듯 (한개씩 전부 추가하지말고 딕셔너리로 사용하세요)
    # 예를들면 "selected_game_info"  딕셔너리 같은걸로?
    # 사용 예제 hometeam_id = selected_game_info.get('selected_home_team_id')


    # 멀티파트 요청 본문 구성을 위한 변수 및 값
    post_data = {
        'aid': data.get('aid'),
        'app_auth_key': data.get('authcode'),
        'app_ver': app_ver,
        'app_vfy': app_vfy,
        'goc': goc,
        'awayteam_id': awayteam_id,
        'cheer_country_code': cheer_country_code,
        'compe': compe,
        'content': data.get('content'),
        'diviedend_sc': diviedend_sc,
        'font_color': font_color,
        'game_id': game_id,
        'gmt_time': gmt_time,
        'h_gmt': h_gmt,
        'hometeam_id': hometeam_id,
        'language_code': language_code,
        'league_id': league_id,
        'mac': mac,
        'match_date': match_date,
        'match_time': match_time,
        'mo': data.get('mo'),
        'national_code': national_code,
        'nt': data.get('nt'),
        'os_ver': data.get('os_ver'),
        'ph': ph,
    }



    # photo1과 photo1_key를 중간에 삽입하는 로직 (사진사용O, 사진검수O, 사진 선탱O 가 되어 있을 경우에만)
    if data.get("is_cheer_photo_used") and data.get("confirm_state") == "C" and data.get("photo_file_path") is not None:
        if photo1 is not None:
            post_data['photo1'] = photo1
        if photo1_key is not None:
            post_data['photo1_key'] = photo1_key

    # 나머지 데이터
    post_data.update({
        'predict_flag': predict_flag,
        're_cheer_no': re_cheer_no,
        'search_country_code': search_country_code,
        'team_id': data.get('team_id'),
        'to_user_no': to_user_no,
        'user_no': data.get('user_no'),
    })


    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가)
    post_data['vh'] = vh

    # 파일 부분 구성
    files = None
    if data.get("is_cheer_photo_used") and data.get("confirm_state") == "C" and data.get("photo_file_path") is not None:
        # 썸네일 파일과 원본 파일을 열어서 처리
        thumbnail_file_path = create_thumbnail(data.get("photo_file_path"))  # 썸네일 생성
        print(f"create_thumbnail 이후 photo_file_path: {data.get("photo_file_path")}")
        print(f"create_thumbnail 이후 thumbnail_file_path: {thumbnail_file_path}")
        # 파일 객체를 열어서 전달
        with open(thumbnail_file_path, 'rb') as thumb_file, open(data.get("photo_file_path"), 'rb') as org_file:
            files = {
                'photo1_thum': thumb_file,  # 썸네일 파일 객체
                'photo1_org': org_file,  # 원본 파일 객체
            }

            print(f"체크포인트1 create_multipart_body_photo_upload 직전 {post_data}")

            print(f"체크포인트1 create_multipart_body_photo_upload 직전 files {files}")

            # post_data 값 출력
            print("post_data 리스트 값:")
            for key, value in post_data.items():
                print(f"{key}: {value}")

            # 멀티파트 본문을 문자열로 생성 (기존 코드를 유지)
            # body = HttpRequestManager.create_multipart_body(post_data, boundary)
            body = create_multipart_body_cheer_with_photo(post_data, files, boundary, data)
            print(f"체크포인트2 create_multipart_body_photo_upload 직후")

    else:
        # 멀티파트 본문을 문자열로 생성 (기존 코드를 유지)
        body = create_multipart_body(post_data, boundary)

        # 문자열을 UTF-8로 인코딩하여 바이트로 변환
        body = body.encode('utf-8')

    # 요청 헤더 설정, 'Content-Length'에 인코딩된 본문의 길이를 사용
    headers = {
        "dt": dt,
        "Content-Length": str(len(body)),
        "Content-Type": f'multipart/form-data; boundary={boundary}',
        "Host": f"{host}:{psynet_port}",
        "Connection": connection,
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
    }

    try:

        if proxy_host and proxy_port:
            conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
            conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
        else:
            conn = http.client.HTTPConnection(host, 13003, timeout=5)

        # 인코딩된 바디와 헤더를 사용하여 POST 요청을 보냄
        conn.request("POST", full_path, body=body, headers=headers)

        # 응답 받기
        response = conn.getresponse()
        print(f"Status: {response.status}, Reason: {response.reason}")

        # 응답 본문 처리
        response_content = response.read()

        # 응답 헤더에서 Content-Encoding 확인
        if response.getheader('Content-Encoding') == 'gzip':
            buffer = BytesIO(response_content)
            with gzip.open(buffer, 'rb') as f:
                response_text = f.read().decode('utf-8')
        else:
            response_text = response_content.decode('utf-8')

        # print(f"reply_auto_api_req response_text: {response_text}")


        print(f"\n"
                    f"[writing_cheer_request post_data]: {post_data}"
                    f"\n"
                    f"[writing_cheer_request response_text]: {response_text}")

        # XML 응답 파싱
        root = ET.fromstring(response_text)
        # msg 태그의 내용을 찾기
        msg_text = root.find(".//msg").text if root.find(".//msg") is not None else ""



        # "성공여부 확인"
        if "성공" in msg_text:
            conn.close()
            return {
                "status": "성공",
            }


        elif "실패" in msg_text:
            conn.close()
            return {
                "status": "실패",
            }


        elif "200 OK" in response_text:
            conn.close()
            show_failure_popup(response_text)
            return {
                "status": "IP차단",
            }


        elif "0002" in msg_text:
            conn.close()
            return {
                "status": "Restricted access service",
            }

        elif "중복" in msg_text:
            conn.close()
            show_failure_popup("중복글")
            return {
                "status": "중복",
            }

        elif "금칙어" in msg_text:
            conn.close()
            show_failure_popup("금칙어(욕설, 음란, 광고 등) 포함]")
            return {
                "status": "금칙어",
            }

        elif "차단" in response_text:
            conn.close()
            show_failure_popup("차단")
            return {
                "status": "차단",
            }

        else:
            conn.close()
            print(f"그외에러 response_text: {response_text}")
            # 실패 시 팝업으로 결과를 보여줌
            show_failure_popup(response_text)
            return {
                "status": "그외에러",

            }


    except Exception as e:
        result = {"status": "예외발생"}
        print("writing_cheer_request 예외 발생:", e)
        if 'response_text' in locals() and response_text is not None:
            show_failure_popup(response_text)

        if "timed out" in str(e).lower():
            print("⏳ 요청이 타임아웃되었습니다. 서버가 응답하지 않습니다.")
            show_failure_popup("time_out")


        # 연결 닫기
        conn.close()

        return result

# 사진 업로드
def photo_upload_request(account_info, file_path, proxy_host, proxy_port):
    # 키값 선언
    seed = SEED128('cqwq2020asjdkq38', 'cqwq2020asjdkq38')

    # 썸네일 파일 생성
    thumbnail_file_path = create_thumbnail(file_path)



    # 변수 값 설정
    boundary = generate_boundary()

    # 값 설정
    phone_number = '010' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    ph = seed.encode(phone_number)
    rh = get_random_ro_hardware()
    photo_key = generate_photo_key(file_path)


    app_ver = APP_VER
    h_gmt = '+0900'
    language_code = 'KO'
    mac = '02:00:00:00:00:00'
    national_code = 'KR'
    opcode = '00000037'

    pk = seed.encode(account_info.get('aid'))
    pk_sub = generate_widevine_id(seed)[1]
    dt = generate_dt()
    goc = generate_goc()
    host = 'psyappi.psynet.co.kr'
    psynet_port = '13003'
    connection = 'Keep-Alive'
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N Build/PQ3B.190801.07281103)'
    accept_encoding = 'gzip'

    # 쿼리 파라미터 항목 나열
    query_params = {
        'os': 'android',
        'pk': pk,
        'pk_sub': pk_sub,
        'rh': rh,
        'rt': 'N',
        'opcode': opcode,
    }

    app_vfy = generate_app_vfy(opcode, account_info.get('aid'), account_info.get('authcode'))

    # URL 구성
    path = '/LiveScoreController.jsp'
    # path = '/post'
    full_path = f"{path}?{urllib.parse.urlencode(query_params)}"


    # 멀티파트 요청 본문 구성을 위한 변수 및 값
    post_data = {
        'aid': account_info.get('aid'),
        'app_auth_key': account_info.get('authcode'),
        'app_ver': app_ver,
        'app_vfy': app_vfy,
        'goc': goc,
        'h_gmt': h_gmt,
        'language_code': language_code,
        'mac': mac,
        'mo': account_info.get('mo'),
        'national_code': national_code,
        'nt': account_info.get('nt', 'SKTelecom'),
        'os_ver': account_info.get('os_ver'),
        'ph': ph,
        "photo_album": "photo1_org",
        "photo_key": photo_key,
        'user_no': account_info.get('user_no')


    }

    # vh 값을 동적으로 계산
    vh = generate_vh_value(post_data, dt)

    # 데이터 인코딩 (vh 값을 post_data에 추가)
    post_data['vh'] = vh

    # 파일 부분 구성
    with open(thumbnail_file_path, 'rb') as thumb_file, open(file_path, 'rb') as org_file:
        files = {
            'photo1_thumb': thumb_file,  # 썸네일 파일
            'photo1_org': org_file,  # 원본 파일
        }
        print(f"files 값: {files}")

        # 멀티파트 본문을 문자열로 생성 (기존 코드를 유지)
        body = create_multipart_body_photo_upload(post_data, files, boundary)

        # 문자열을 UTF-8로 인코딩하여 바이트로 변환
        # encoded_body = body.encode('utf-8')

        # 요청 헤더 설정, 'Content-Length'에 인코딩된 본문의 길이를 사용
        headers = {
            "dt": dt,
            # "Content-Length": str(len(encoded_body)),
            "Content-Length": str(len(body)),
            "Content-Type": f'multipart/form-data; boundary={boundary}',
            "Host": f"{host}:{psynet_port}",
            "Connection": connection,
            "User-Agent": user_agent,
            "Accept-Encoding": accept_encoding,
        }

        try:
            if proxy_host and proxy_port:
                conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=5)
                conn.set_tunnel(host, 13003)  # Use port 443 for HTTPS if needed
            else:
                conn = http.client.HTTPConnection(host, 13003, timeout=5)

            # 인코딩된 바디와 헤더를 사용하여 POST 요청을 보냄
            # conn.request("POST", full_path, body=encoded_body, headers=headers)
            conn.request("POST", full_path, body=body, headers=headers)

            # 응답 받기
            response = conn.getresponse()
            print(f"Status: {response.status}, Reason: {response.reason}")

            # 응답 본문 처리
            response_content = response.read()

            # 응답 헤더에서 Content-Encoding 확인
            if response.getheader('Content-Encoding') == 'gzip':
                buffer = BytesIO(response_content)
                with gzip.open(buffer, 'rb') as f:
                    response_text = f.read().decode('utf-8')
            else:
                response_text = response_content.decode('utf-8')

            print(f"photo_upload_request response_text: {response_text}")

            # XML 응답 파싱
            root = ET.fromstring(response_text)
            # msg 태그의 내용을 찾기
            msg_text = root.find(".//msg").text if root.find(".//msg") is not None else ""

            # "성공여부 확인"
            if "성공" in msg_text:
                conn.close()
                return {
                    "status": "성공",
                }

            elif "0002" in msg_text:
                conn.close()
                return {
                    "status": "Restricted access service",
                }

            elif "중복" in msg_text:
                conn.close()
                return {
                    "status": "중복",
                }

            else:
                conn.close()
                print(f"그외에러 response_text: {response_text}")
                return {
                    "status": "그외에러",

                }

        except Exception as e:
            result = {"status": "예외발생"}
            print("photo_upload_request 예외 발생:", e)

            # 연결 닫기
            conn.close()

            return result

# 글작성 실패시 팝업 함수
def show_failure_popup(result, proxy_host, proxy_port):
    if "차단" in result:
        app.popup_signal_warning.emit(
            "글 작성 실패",
            f"글 작성 실패! 에러 상세: \n해당 글이 광고, 음란, 욕설 등으로 의심되어 라스봇에 의해 차단되었습니다.\n\n"
            "라스봇에 의해 차단되었습니다.\n\n"
            "키워드를 변경하여 재 시도해주세요.\n\n"
            "*라스봇에 의해 BAN*"
        )

    if "금칙어" in result:
        app.popup_signal_warning.emit(
            "글 작성 실패",
            f"글 작성 실패! 에러 상세: \n{result}\n\n"
        )

    elif "200 OK" in result:
        app.popup_signal_warning.emit(
            "글 작성 실패",
            f"글 작성 실패! 에러 상세: \n{result}\n\n"
            "IP 또는 키워드가 라스에서 차단되었습니다.\n\n"
            "IP 또는 키워드를 변경하여 재 시도해주세요.\n\n"
            "*IP or 키워드 BAN*"
        )

    elif "417 Expectation Failed" in result:
        app.popup_signal_warning.emit(
            "글 작성 실패",
            "해당 에러는 VPN 서버와의 통신 문제 입니다.\n\n"
            "다른 VPN 사용을 추천 드립니다.\n\n"
            "노드 or 익스프레스 VPN 추천.\n\n"
            f"글 작성 실패! 에러 상세: \n{result[:300]}\n\n"
        )

    elif "CDATA[실패]" in result and not functions.macro_running:
        print(f"[디버깅] functions.is_new_account: {functions.is_new_account}")
        if not functions.is_new_account:
            app.popup_signal_warning.emit(
                "글 작성 실패",
                f"\n실패!\n해당 계정은 차단(BAN) 되었습니다.\n\n*계정 BAN*"
            )

    elif "time_out" in result:
        app.popup_signal_warning.emit(
            "글 작성 실패",
            f"서버 응답 없음, 인터넷 or VPN 상태를 확인해 주세요\n\n"
            f"글 작성 실패! 에러 상세: \n{result}\n\n"
        )

    elif not functions.macro_running:
        print(f"[디버깅] functions.is_new_account: {functions.is_new_account}")
        if not functions.is_new_account:
            app.popup_signal_warning.emit("글 작성 실패", f"글 작성 실패! 에러 상세: \n{result}")


    else:
        print(f"[디버깅] functions.is_new_account: {functions.is_new_account}")
        if not functions.is_new_account:
            app.popup_signal_warning.emit("글 작성 실패", f"글 작성 실패! 에러 상세: \n{result}")