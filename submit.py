#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import re
import json
import time
import os
from getpass import getpass

#'language_id': ext array
LANGUAGES = {
    0: ['.c'],
    1: ['.cpp', '.cc', '.cxx'],
    2: ['.p','.pas'],
    3: ['.java'],
    4: ['.rb'],
    5: ['.sh'],
    6: ['.py'],
    7: ['.php'],
    8: ['.pl'],
    9: ['.cs'],
    10: ['.m'],
    12: ['.go'],
    13: ['.f95','.for'],
    14: ['.scm'],
    15: ['.scala'],
    16: ['.lua'],
    17: ['.js'],
    18: ['.coffee'],
    19: ['.ada'],
    20: ['.vb'],
    21: ['.awk'],
    22: ['.ml'],
    23: ['.bf'],
    24: ['.ws'],
    25: ['.groovy'],
    26: ['.tcl'],
    27: ['.asm'],
    29: ['.d'],
    33: ['.clj'],
    37: ['.fs'],
    39: ['.fal'],
    41: ['.pike'],
    43: ['.sed'],
    44: ['.rs'],
    46: ['.boo'],
    47: ['.i'],
    48: ['.bc'],
    53: ['.n'],
    54: ['.cobra'],
    55: ['.nim'],
    58: ['.txt'],
    61: ['.io']
};

LOGIN_URL = 'https://www.acmicpc.net/signin'
SUBMIT_URL = 'https://www.acmicpc.net/submit/{{problem_id}}'
STATUS_URL = 'https://www.acmicpc.net/status/ajax';
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
    'Referer': 'https://www.acmicpc.net',
    'Origin': 'https://www.acmicpc.net'
}

s = requests.session()
read = lambda: sys.stdin.readline()
write = lambda x: sys.stdout.write(x)


def get_language(filename):
    dummy, extension = os.path.splitext(filename)

    for key, value in LANGUAGES.items():
        if extension in value:
            return int(key)
    return -1

def get_source(filename):
    if not os.path.exists(filename):
        return (False, '')
    fp = open(filename, 'r')
    source = fp.read()
    fp.close()
    return (True, source)

def wait_solution(solution_id):
    data = {
        'solution_id': solution_id
    }

    while (True):
        solution_headers = {
            'X-Requested-With': 'XMLHttpRequest'
        }
        solution_headers.update(HEADERS)
        res = s.post(STATUS_URL, headers=solution_headers, data=data)
        result = json.loads(res.text)
        print result['result_name'];
        if int(result['result']) > 3:
            break
        time.sleep(1)

def get_submit_url(problem_id):
    return SUBMIT_URL.replace('{{problem_id}}', str(problem_id))

def submit(problem_id, source, language):
    data = {
        'problem_id': problem_id,
        'source': source,
        'language': language,
        'csrf_key': get_csrf_token(problem_id)
    }
    url = get_submit_url(problem_id)
    res = s.post(url, headers=HEADERS, data=data)
    # get solution_id
    m = re.search('watch_solution\([0-9]+\)', res.text)
    m2 = re.search('[0-9]+', m.group(0))
    
    solution_id = int(m2.group(0))
    return solution_id

def get_csrf_token(problem_id):
    url = get_submit_url(problem_id)
    res = s.get(url, headers=HEADERS)
    pos = res.text.find('name="csrf_key"')
    csrf_token = res.text[pos+23:pos+23+32]
    return csrf_token

def login(username, password):
    data = {
        'login_user_id': username,
        'login_password': password
    }
    res = s.post(LOGIN_URL, headers=HEADERS, data=data)
    if u'<title>로그인</title>' not in res.text:
        return True
    else:
        return False

def validation_check(username, password):
    if len(username) == 0:
        print u'아이디를 입력해 주세요'
        return False
    if len(password) == 0:
        print u'비밀번호를 입력해 주세요'
        return False

    return True

def get_problem_id_from_filename(filename):
    problem_id, extension = os.path.splitext(filename)
    if problem_id.isdigit():
        return int(problem_id)
    else:
        return -1

def close_session():
    s.close()

def main():

    # parse arguments vector
    argv = sys.argv[1:]
    if len(argv) < 1 or len(argv) > 2:
        print u'Usage: python submit.py filename'
        print u'Usage: python submit.py problem_id filename'
        return close_session()

    # get filename, problem_id from arguments
    if len(argv) == 1:
        filename = argv[0]
        problem_id = get_problem_id_from_filename(filename)
        if problem_id == -1:
                print u'파일 이름은 문제번호.확장자 형식이 되어야 합니다'
                return close_session()
    else:
        problem_id = int(argv[0])
        filename = argv[1]

    # get source from filename
    success, source = get_source(filename)
    if not success:
        print u'%s는 없는 파일입니다' % filename
        return close_session()

    # get language_id
    language = get_language(filename)
    if language == -1:
        print u'무슨 언어인지 모르겠어요. 확장자를 확인해 주세요'
        return close_session()

    # get username, password
    write(u'아이디: ')
    username = read().strip()
    write(u'비밀번호: ')
    password = getpass('')

    # validation check
    if not validation_check(username, password):
        return close_session()

    # login
    if not login(username, password):
        print u'아이디 또는 비밀번호가 일치하지 않습니다'
        return close_session()

    # submit source code
    solution_id = submit(problem_id, source, language)
    # wait result
    wait_solution(solution_id)

    return close_session()

# start
main()
