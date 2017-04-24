#-*- coding: utf-8 -*-

import sys
from ply import lex

reload(sys)
sys.setdefaultencoding('utf-8')

tokens = 'c v o u e i O U E k n r l K N R L lp rp st pl qst or'.split()

t_c = r'(ㄱ|ㄲ|ㄴ|ㄷ|ㄸ|ㄹ|ㅁ|ㅂ|ㅃ|ㅅ|ㅆ|ㅇ|ㅈ|ㅉ|ㅊ|ㅋ|ㅌ|ㅍ|ㅎ)'
t_v = r'(ㅏ|ㅐ|ㅑ|ㅒ|ㅓ|ㅔ|ㅕ|ㅖ|ㅗ|ㅛ|ㅜ|ㅠ|ㅡ|ㅣ)'

t_o = r'(ㅗ)'
t_u = r'(ㅜ)'
t_e = r'(ㅡ)'
t_i = r'(ㅏ|ㅐ|ㅑ|ㅒ|ㅓ|ㅔ|ㅕ|ㅖ|ㅛ|ㅠ|ㅣ)'

t_O = r'(ㅏ|ㅐ|ㅣ)'
t_U = r'(ㅓ|ㅔ|ㅣ)'
t_E = r'(ㅣ)'

t_k = r'(ㄱ|ㅂ)'
t_n = r'(ㄴ)'
t_r = r'(ㄹ)'
t_l = r'(ㄲ|ㄷ|ㄸ|ㅁ|ㅃ|ㅅ|ㅆ|ㅇ|ㅈ|ㅉ|ㅊ|ㅋ|ㅌ|ㅍ|ㅎ)'

t_K = r'(ㅅ)'
t_N = r'(ㅈ|ㅎ)'
t_R = r'(ㄱ|ㅁ|ㅂ|ㅅ|ㅌ|ㅍ|ㅎ)'
t_L = r'(ㄲ|ㄴ|ㄷ|ㄸ|ㄹ|ㅃ|ㅆ|ㅇ|ㅉ|ㅊ|ㅋ)'

t_lp = r'\('
t_rp = r'\)'
t_st = r'\*'
t_pl = r'\+'
t_qst = r'\?'
t_or = r'\|'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

hangeul = r'(%s(%s%s?|%s%s?|%s%s?|%s)(%s%s?|%s%s?|%s%s?|%s%s?)?)+' %(t_c, t_o, t_O, t_u, t_U, t_e, t_E, t_i, t_k, t_K, t_n, t_N, t_r, t_R, t_l, t_L)
#hangeul = r'(c(oO?|uU?|eE?|i)(kK?|nN?|rR?|lL?)?)+'

lexer = lex.lex()

#string = raw_input("한글을 입력해주세요\n")
string = 'ㄱㅏㅇㅅㅏㄴㅎㅗㅏㅈㅏㄱㅇㅛㅇ'

lexer.input(hangeul)
output = ''
while True:
    tok = lexer.token()
    if not tok: break
    output += tok.type
print lexer.lexmatch
print output

lexer.input(string)

output = ''
while True:
    tok = lexer.token()
    if not tok: break
    output += tok.type
print output
