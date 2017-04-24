#-*- coding: utf-8 -*-

import sys
import re
import numpy as np
from ply import lex

reload(sys)
sys.setdefaultencoding('utf-8')

tokens = 'o u e i O U E k n r l K N R L t m j h'.split()

#t_c = r'(ㄱ|ㄲ|ㄴ|ㄷ|ㄸ|ㄹ|ㅁ|ㅂ|ㅃ|ㅅ|ㅆ|ㅇ|ㅈ|ㅉ|ㅊ|ㅋ|ㅌ|ㅍ|ㅎ)'
#t_v = r'(ㅏ|ㅐ|ㅑ|ㅒ|ㅓ|ㅔ|ㅕ|ㅖ|ㅗ|ㅛ|ㅜ|ㅠ|ㅡ|ㅣ)'
#t_v = t_o + t_u + t_e + t_i

t_o = r'(ㅗ)'
t_u = r'(ㅜ)'
t_e = r'(ㅡ)'
t_i = r'(ㅑ|ㅒ|ㅕ|ㅖ|ㅛ|ㅠ)'
#t_i = t_O + t_U + t_E + t_i
#t_i = r'(ㅏ|ㅐ|ㅑ|ㅒ|ㅓ|ㅔ|ㅕ|ㅖ|ㅛ|ㅠ|ㅣ)'

t_O = r'(ㅏ|ㅐ)'
t_U = r'(ㅓ|ㅔ)'
t_E = r'(ㅣ)'

t_k = r'(ㄱ|ㅂ)'
t_n = r'(ㄴ)'
t_r = r'(ㄹ)'
t_m = r'(ㅁ|ㅌ|ㅍ)'
#t_l = t_K + t_j + t_h + t_m + t_kk
#t_l = r'(ㄲ|ㄷ|ㄸ|ㅁ|ㅃ|ㅅ|ㅆ|ㅇ|ㅈ|ㅉ|ㅊ|ㅋ|ㅌ|ㅍ|ㅎ)'

t_K = r'(ㅅ)'
#t_N = r'(ㅈ|ㅎ)'
#t_N = t_j + t_h
t_j = r'(ㅈ)'
t_h = r'(ㅎ)'
#t_R = t_k + t_m + t_h
#t_R = r'(ㄱ|ㅁ|ㅂ|ㅅ|ㅌ|ㅍ|ㅎ)'
#t_L = t_t + t_n + t_r
#t_L = r'(ㄲ|ㄴ|ㄷ|ㄸ|ㄹ|ㅃ|ㅆ|ㅇ|ㅉ|ㅊ|ㅋ)'
t_t = r'(ㄲ|ㄷ|ㄸ|ㅃ|ㅆ|ㅇ|ㅉ|ㅊ|ㅋ)'
#t_c = t_k + t_n + t_r + t_K + t_j + t_h + t_m + t_t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

ic = dict('ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ'.split(), range(19))
md = dict('ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ'.split(), range(21))
fc = dict(['']+'ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄹ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅄ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ'.split(), range(28))
#hangeul = r'(%s(%s%s?|%s%s?|%s%s?|%s)(%s%s?|%s%s?|%s%s?|%s%s?)?)+' %(t_c, t_o, t_O, t_u, t_U, t_e, t_E, t_i, t_k, t_K, t_n, t_N, t_r, t_R, t_l, t_L)
hangeul = r'((k|n|r|K|j|h|m|t)(o(O|E)?|u(U|E)?|eE?|(O|U|E|i))(kK?|n(j|h)?|r(k|m|h)?|(t|n|r)?))+'
prog = re.compile(hangeul)

lexer = lex.lex()

#string = raw_input("한글을 입력해주세요\n")
string = 'ㄱㅏㅇㅅㅏㄴㅎㅗㅏㅈㅏㄱㅇㅛㅇㅇㄴㄴㅏㄴㅣㄴㅈㅏㅏㅏㄴㅇㄹㅏㄹㄱ'
lexer.input(string)

output = []
buff = []
final = []
while True:
    tok = lexer.token()
    if not tok: break
    output.append(tok)
    types = ''.join([o.type for o in output])
    print "%15s: %s" %("Type List", types)
    total_re_len = [sum([len(e[0]) for e in ele]) for ele in [prog.findall(types, 0, i) + prog.findall(types, i, len(types)) for i in range(len(types))]]
    print "%15s: %s" %("Max RE Length", np.max(total_re_len))
    i = np.argmax(total_re_len)
    buff = [ele[0] for ele in prog.findall(types,0,i)+prog.findall(types,i,len(types))]
    print "%15s: %s" %("Max Buffers", ' '.join(buff))

    if len(buff) == 2:
        print "Complete %s" %''.join([o.value for o in output[:i]
        final.append([o.value for o in output[:i]])
        output = output[i:]
    elif total_re_len[i] < len(output):
        final.append([o.value for o in output[:-1]])
        output = output[-1:]
final.append([o.value for o in output])
for f in final:
    iC = f[0:1]
    mD = f[1:2]
    fC = f[2:]
    
    print ''.join(f)
