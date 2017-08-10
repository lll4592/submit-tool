#[Baekjoon Online Judge](http://www.acmicpc.net/) Submit Tool

##Tool 사용법

- python submit.py 파일이름 [버전]
- python submit.py 문제번호 파일이름 [버전]

###예제

python submit.py 1920.cpp
python submit.py 1920 1920.cpp

###주의 사항
- 확장자로 어떤 언어인지 판별합니다.
- 문제번호를 입력하지 않고 제출할 때는  문제번호.확장자 형식이어야 합니다. 예) 1920.cpp, 1000.py

##버전 설정
- python submit.py 1000.cc 14

  c++ 14로 제출합니다.
- python submit.py 1000.cc 11

  c++ 11로 제출합니다.
- python submit.py 1000.c clang

  c(clang)으로 제출합니다.
- python submit.py 1000.cc clang

  c++(clang)으로 제출합니다.
- python submit.py 1000.cc clang11

  c++(clang11)으로 제출합니다.
- python submit.py 1000.cc clang14

  c++(clang14)으로 제출합니다.
- python submit.py 1000.py 3

  python3 로 제출합니다.
- python submit.py 1000.py py3

  python3 로 제출합니다.
- python submit.py 1000.py pypy

  pypy로 제출합니다.
- python submit.py 1000.py pypy3

  pypy3로 제출합니다.

###python을 치기 귀찮다면…

아래와 같이 해도 제출은 됩니다.

./submit.py 1920 1920.cpp

그런데, .py도 치기 귀찮다면

mv submit.py submit
./submit 1920 1920.cpp

이렇게 하면 됩니다.

###problem.py

./problem.py 1000

1000/ 에 1000번 문제의 샘플데이터를 저장합니다

