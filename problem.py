#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import os
import sys

PROBLEM_URL = 'https://www.acmicpc.net/problem/{{problem_id}}'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
    'Referer': 'https://www.acmicpc.net',
    'Origin': 'https://www.acmicpc.net'
}

def get_problem_url(problem_id):
    return PROBLEM_URL.replace('{{problem_id}}', str(problem_id))

def check_page_is_not_found(text):
    return text.find('<span class="error-v1-title">404</span>') != -1

def touch_directory(problem_id):
    path = str(problem_id)
    if not os.path.exists(path):
        os.makedirs(path)

def write_sampledata(text, problem_id):
    m = re.findall('(<pre.+?>([\s\S]*?)</pre>)', text)
    inputs = [x[1].strip() for x in m if x[0].find('sample-input') != -1]
    outputs = [x[1].strip() for x in m if x[0].find('sample-output') != -1]

    for index, content in enumerate(inputs):
        fd = os.open('%d/%d.in' % (problem_id, index), os.O_RDWR|os.O_CREAT)
        os.write(fd, content)
        os.close(fd)

    for index, content in enumerate(outputs):
        fd = os.open('%d/%d.out' % (problem_id, index), os.O_RDWR|os.O_CREAT)
        os.write(fd, content)
        os.close(fd)

def get_problem(problem_id):
    url = get_problem_url(problem_id)
    res = requests.get(url, headers=HEADERS)
    if check_page_is_not_found(res.text):
        print u'문제를 찾을 수 없습니다'
        return

    touch_directory(problem_id)
    write_sampledata(problem_id=problem_id, text=res.text)

def main():
    argv = sys.argv[1:]
    if len(argv) != 1:
        print 'Usage: python problem.py problem_id'
        return

    try:
        problem_id = int(argv[0])
    except:
        print '문제 번호는 숫자만 가능합니다'
        return

    get_problem(problem_id)

main()

