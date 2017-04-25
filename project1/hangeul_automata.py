#-*- coding: utf-8 -*-

import sys
import re
import numpy as np
from ply import lex

reload(sys)
sys.setdefaultencoding('utf-8')

# utf-8 url escape code로 받아들인 입력을 unicode로 바꿔주는 dictionary입니다.
# 종성 중성 초성의 순서로 deictionary를 업데이트합니다.
# 들어온 문자를 먼저 초성이라고 여기기 위해 종성 위에 덧씌웁니다.
utf_to_uni =       dict([(ele, unichr(0x11A8+i+1)) for i, ele in enumerate('ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄹ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅄ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ'.split())])
utf_to_uni.update( dict([(ele, unichr(0x1100+i)) for i, ele in enumerate('ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ'.split())]))
utf_to_uni.update( dict([(ele, unichr(0x1161+i)) for i, ele in enumerate('ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ'.split())]))

# 초성을 종성의 unicode 번호로 매칭시켜주는 dictionary입니다.
trans = {0:1,1:2,2:4,3:7,5:8,6:16,7:17,9:19,10:20,11:21,12:22,14:23,15:24,16:25,17:26,18:27}

# 중성과 종성은 두 개 이상의 unicode의 합으로 나타내어질 수도 있습니다.
# 이를 하나의 unicode로 매칭시켜주는 dictionary입니다.
mds = {'ㅗㅏ':'ㅘ','ㅗㅐ':'ㅙ','ㅗㅣ':'ㅚ','ㅜㅓ':'ㅝ','ㅜㅔ':'ㅞ','ㅜㅣ':'ㅟ','ㅡㅣ':'ㅢ'}
mds = dict((utf_to_uni[it[0][:3]] + utf_to_uni[it[0][3:]], utf_to_uni[it[1]]) for it in mds.items())
fcs = {'ㄱㅅ':'ㄳ','ㄴㅈ':'ㄵ','ㄴㅎ':'ㄶ','ㄹㄱ':'ㄺ','ㄹㅁ':'ㄻ','ㄹㅂ':'ㄼ','ㄹㅅ':'ㄽ','ㄹㅌ':'ㄾ','ㄹㅍ':'ㄿ','ㄹㅎ':'ㅀ','ㅂㅅ':'ㅄ'}
fcs = dict((utf_to_uni[it[0][:3]] + utf_to_uni[it[0][3:]], utf_to_uni[it[1]]) for it in fcs.items())

# 초성 중성 종성 unicode를 최종적으로 조합형으로 출력하기 위해 쓰이는 dictionary입니다.
ic = dict([(unichr(0x1100+i), i) for i in range(19)])
md = dict([(unichr(0x1161+i), i) for i in range(21)])
fc = dict([(unichr(0x11A8+i), i) for i in range(28)])
fc.update(dict([(unichr(0x1100+i), v) for i, v in trans.items()]))

# Lex에 이용할 token입니다.
# 한 번에 입력할 수 있는 31개의 한글 자모를 정확히 15개의 토큰으로 나눌 수 있습니다.
# 아래 토큰들은 조합형 한글 Regular Expression에서 같은 역할을 하는 것끼리 묶여있습니다.
tokens = 'o u e i O U E k n r K t m j h'.split()

t_o = r'(%s)' %(utf_to_uni['ㅗ'])
t_u = r'(%s)' %(utf_to_uni['ㅜ'])
t_e = r'(%s)' %(utf_to_uni['ㅡ'])
t_i = r'(%s|%s|%s|%s|%s|%s)' %(utf_to_uni['ㅑ'],utf_to_uni['ㅒ'],utf_to_uni['ㅕ'],utf_to_uni['ㅖ'],utf_to_uni['ㅛ'],utf_to_uni['ㅠ'])

t_O = r'(%s|%s)' %(utf_to_uni['ㅏ'],utf_to_uni['ㅐ'])
t_U = r'(%s|%s)' %(utf_to_uni['ㅓ'],utf_to_uni['ㅔ'])
t_E = r'(%s)' %(utf_to_uni['ㅣ'])

t_k = r'(%s|%s)' %(utf_to_uni['ㄱ'],utf_to_uni['ㅂ'])
t_n = r'(%s)' %(utf_to_uni['ㄴ'])
t_r = r'(%s)' %(utf_to_uni['ㄹ'])
t_m = r'(%s|%s|%s)' %(utf_to_uni['ㅁ'],utf_to_uni['ㅌ'],utf_to_uni['ㅍ'])

t_K = r'(%s)' %(utf_to_uni['ㅅ'])
t_j = r'(%s)' %(utf_to_uni['ㅈ'])
t_h = r'(%s)' %(utf_to_uni['ㅎ'])
t_t = r'(%s|%s|%s|%s|%s|%s|%s|%s|%s)' %(utf_to_uni['ㄲ'],utf_to_uni['ㄷ'],utf_to_uni['ㄸ'],utf_to_uni['ㅃ'],utf_to_uni['ㅆ'],utf_to_uni['ㅇ'],utf_to_uni['ㅉ'],utf_to_uni['ㅊ'],utf_to_uni['ㅋ'])

# 그대로 출력될 문자들입니다.
literals = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-= \n\b,./<>?;\':\"[]{}|~!@#$%^&*()_+'

def t_error(t):
    t.lexer.skip(1)

# 조합형 한글 Regular Expression입니다.
# 모든 한글 나열은 아래와 같은 조건을 만족할 때, 규칙에 맞게 조합되었다고 할 수 있습니다.
hangeul = r'((k|n|r|K|j|h|m|t)(o(O|E)?|u(U|E)?|eE?|(O|U|E|i))(kK?|n(j|h)?|r(k|m|h)?|(m|K|j|h|t|n|r)?))+'
prog = re.compile(hangeul)

lexer = lex.lex()
string = ''

print "자유롭게 한 글자씩 입력해주세요."

while True:
    toks = []
    possible_unions = []
    tokens_buffer = []
    complete_buffer = ''

    char = raw_input()
    if char == "\\b": string = string[:-1]
    elif utf_to_uni.has_key(char): string += utf_to_uni[char]
    else: string += char
    lexer.input(string)

    while True:
        tok = lexer.token()
        if not tok: break
        toks.append(tok)
        types = ''.join([o.type for o in toks])

        # 주어진 token을 최대한 많이 사용할 수 있는 형태를 찾기 위해 모든 곳에 기준 index를 두어 테스트해봅니다.
        total_re_len = [sum([len(e[0]) for e in ele]) for ele in [prog.findall(types, 0, i) + prog.findall(types, i, len(types)) for i in range(len(types))]]
        devide_index = np.argmax(total_re_len)

        # 그 중 가장 token을 많이 이용하도록 나누는 index를 기준으로 나눈 조합식 list를 정의합니다.
        possible_unions = [ele[0] for ele in prog.findall(types,0,devide_index)+prog.findall(types,devide_index,len(types))]

        # 가능한 한글 조합이 두개 이상 있다는 것은 하나는 이미 완성되었다는 의미입니다.
        if len(possible_unions) == 2:
            tokens_buffer.append([o.value for o in toks[:devide_index]])
            toks = toks[devide_index:]

        # 주어진 token의 갯수보다 조합에 사용 가능한 최대 token의 수가 적다는 것은 조합이 불가능한 문자열이 있다는 의미입니다.
        elif total_re_len[devide_index] < len(toks):
            tokens_buffer.append([o.value for o in toks[:-1]])
            toks = toks[-1:]

    # 입력이 끝난 후 남은 token은 그대로 빼내줍니다.
    tokens_buffer.append([o.value for o in toks])

    # 입력 후 토큰들이 Regular Expression에 맞게 나뉘어진 tokens_buffer에서 하나씩 조합형 한글을 꺼내옵니다.
    # 이 조합형 한글의 길이에 따라 해야 할 업무가 달라집니다.
    # 예를 들면, (ㄱ, ㅗ, ㅏ, ㄴ, ㅈ)와 같이 길이가 5인 조합형 한글은 (ㄱ, ㅘ, ㄵ)으로 바꾸어야 unicode로 표기하기 쉽습니다.
    # 맨 위에서 정의한 dictionary를 이용해서 unicode 형식에 맞게 바꿉니다.
    for toks in tokens_buffer:
        if not toks: continue

        # 첫 자부터 모음인 경우 조합형 한글이 아니므로 그대로 버퍼에 넣습니다.
        if md.has_key(toks[0]):
            complete_buffer += toks[0]
            continue

        # 길이가 1이면서 모음이 아닌 경우는 조합형 한글이 아닌 자음이므로 그대로 버퍼에 넣습니다.
        if len(toks) == 1:
            complete_buffer += toks[0]
            continue

        # 길이가 2이면 초성과 중성으로 이루어져 있으며 종성은 없습니다.
        elif len(toks) == 2:
            md_num = md[toks[1]]
            fc_num = 0
        
        # 길이가 3이면 초성 중성 중성 또는 초성 중성 종성 입니다.
        elif len(toks) == 3:
            if mds.has_key(''.join(toks[1:3])):
                md_num = md[mds[''.join(toks[1:3])]]
                fc_num = 0
            else:
                md_num = md[toks[1]]
                fc_num = fc[toks[2]]
        
        # 길이가 4이면 초성 중성 중성 종성 또는 초성 중성 종성 종성 입니다.
        elif len(toks) == 4:
            if mds.has_key(''.join(toks[1:3])):
                md_num = md[mds[''.join(toks[1:3])]]
                fc_num = fc[toks[3]]
            else:
                md_num = md[toks[1]]
                fc_num = fc[fcs[''.join(toks[2:])]]
        
        # 길이가 5이면 초성 중성 중성 종성 종성 입니다.
        elif len(toks) == 5:
            md_num = md[mds[''.join(toks[1:3])]]
            fc_num = fc[fcs[''.join(toks[3])]]

        # 위에 해당하지 않는 경우 Error 입니다.
        else: raise("Number of tokens")

        # 여기를 방문하면 항상 초성이 있는 경우이므로 초성 번호를 받아옵니다.
        ic_num = ic[toks[0]]

        # unicode character를 complete_buffer에 넣어줍니다.
        complete_buffer += unichr(0xAC00 + ic_num*21*28 + md_num*28 + fc_num)

    print '\033[F\033[K\033[F'
    print complete_buffer
