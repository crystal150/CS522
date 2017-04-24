#-*- coding: utf-8 -*-

import sys
from reg import RE
from nfa import NFA
from dfa import DFA

reload(sys)
sys.setdefaultencoding('utf-8')

c = '(ㄱ|ㄲ|ㄴ|ㄷ|ㄸ|ㄹ|ㅁ|ㅂ|ㅃ|ㅅ|ㅆ|ㅇ|ㅈ|ㅉ|ㅊ|ㅋ|ㅌ|ㅍ|ㅎ)'
v = '(ㅏ|ㅐ|ㅑ|ㅒ|ㅓ|ㅔ|ㅕ|ㅖ|ㅗ|ㅛ|ㅜ|ㅠ|ㅡ|ㅣ)'

o = '(ㅗ)'
u = '(ㅜ)'
e = '(ㅡ)'
i = '(ㅏ|ㅐ|ㅑ|ㅒ|ㅓ|ㅔ|ㅕ|ㅖ|ㅛ|ㅠ|ㅣ)'

O = '(ㅏ|ㅐ|ㅣ)'
U = '(ㅓ|ㅔ|ㅣ)'
E = '(ㅣ)'

k = '(ㄱ|ㅂ)'
n = '(ㄴ)'
r = '(ㄹ)'
l = '(ㄲ|ㄷ|ㄸ|ㅁ|ㅃ|ㅅ|ㅆ|ㅇ|ㅈ|ㅉ|ㅊ|ㅋ|ㅌ|ㅍ|ㅎ)'

K = '(ㅅ)'
N = '(ㅈ|ㅎ)'
R = '(ㄱ|ㅁ|ㅂ|ㅅ|ㅌ|ㅍ|ㅎ)'
L = '(ㄲ|ㄴ|ㄷ|ㄸ|ㄹ|ㅃ|ㅆ|ㅇ|ㅉ|ㅊ|ㅋ)'

hangeul = '(%s(%s%s?|%s%s?|%s%s?|%s)(%s%s?|%s%s?|%s%s?|%s%s?)?)+' %(c, o, O, u, U, e, E, i, k, K, n, N, r, R, l, L)

print RE(hangeul).re_to_nfa()

string = raw_input("한글을 입력해주세요\n")

lexer.input(string)
tok = True
while tok:
    char = lexer.token().value
