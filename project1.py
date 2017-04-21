#-*- coding: utf-8 -*-

import sys
import urllib
from ply import lex

reload(sys)
sys.setdefaultencoding('utf-8')


tokens = tuple(['CONSONANT'+str(i) for i in range(19)]+['VOWEL'+str(i) for i in range(21)])

t_CONSONANT0 = 'ㄱ'
t_CONSONANT1 = 'ㄲ'
t_CONSONANT2 = 'ㄴ'
t_CONSONANT3 = 'ㄷ'
t_CONSONANT4 = 'ㄸ'
t_CONSONANT5 = 'ㄹ'
t_CONSONANT6 = 'ㅁ'
t_CONSONANT7 = 'ㅂ'
t_CONSONANT8 = 'ㅃ'
t_CONSONANT9 = 'ㅅ'
t_CONSONANT10 = 'ㅆ'
t_CONSONANT11 = 'ㅇ'
t_CONSONANT12 = 'ㅈ'
t_CONSONANT13 = 'ㅉ'
t_CONSONANT14 = 'ㅊ'
t_CONSONANT15 = 'ㅋ'
t_CONSONANT16 = 'ㅌ'
t_CONSONANT17 = 'ㅍ'
t_CONSONANT18 = 'ㅎ'

t_VOWEL0 = 'ㅏ'
t_VOWEL1 = 'ㅐ'
t_VOWEL2 = 'ㅑ'
t_VOWEL3 = 'ㅒ'
t_VOWEL4 = 'ㅓ'
t_VOWEL5 = 'ㅔ'
t_VOWEL6 = 'ㅕ'
t_VOWEL7 = 'ㅖ'
t_VOWEL8 = 'ㅗ'
t_VOWEL9 = 'ㅘ'
t_VOWEL10 = 'ㅙ'
t_VOWEL11 = 'ㅚ'
t_VOWEL12 = 'ㅛ'
t_VOWEL13 = 'ㅜ'
t_VOWEL14 = 'ㅝ'
t_VOWEL15 = 'ㅞ'
t_VOWEL16 = 'ㅟ'
t_VOWEL17 = 'ㅠ'
t_VOWEL18 = 'ㅡ'
t_VOWEL19 = 'ㅢ'
t_VOWEL20 = 'ㅣ'



def t_error(t):
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

class NFA():
    def __init__(self, Q, V, S, T):
        self.Q = Q
        self.V = V
        self.S = S
        self.T = T
        self.s = S
    
    def next(self, char):
        for t in self.T:
            if self.get_state() == t.get_state() and char == t.get_char():
                self.set_state(t.get_final())
                return self.get_state()
        self.set_state(S)
        return self.get_state()

    def get_state(self):
        return self.s

    def set_state(self, s):
        self.s = s

    def to_DFA(self):
        pass

class transition():
    def __init__(self, s_i, c, s_f):
        self.s_i = s_i
        self.c = c
        self.s_f = s_f
    def get_initial(self):
        return self.s_i
    def get_char(self):
        return self.c
    def get_final(self):
        return self.s_f


states = 'S V O U A I K N R L'.split()
simga = 'ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅛ ㅜ ㅠ ㅡ ㅣ'.split()
transitions = []
transitions.extend([transition(s_i, c, 'V') for s_i in 'S L'.split() for c in 'ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅋ ㅌ ㅍ ㅎ'.split()])
transitions.extend([transition(s_i, 'ㅗ', 'O') for s_i in 'V K N R L'.split()])
transitions.extend([transition(s_i, 'ㅜ', 'U') for s_i in 'V K N R L'.split()])
transitions.extend([transition(s_i, 'ㅡ', 'A') for s_i in 'V K N R L'.split()])
transitions.extend([transition(s_i, c, 'I') for s_i in 'V K N R L'.split() for c in 'ㅏ ㅑ ㅓ ㅕ ㅛ ㅠ ㅣ ㅐ ㅒ ㅔ ㅖ'.split()])
transitions.extend([transition('O', c, 'I') for c in 'ㅏ ㅐ ㅣ'.split()])
transitions.extend([transition('U', c, 'I') for c in 'ㅓ ㅔ ㅣ'.split()])
transitions.extend([transition('A', 'ㅣ', 'I')])
transitions.extend([transition(s_i, c, 'K') for s_i in 'O U A I'.split() for c in 'ㄱ ㅂ'.split()])
transitions.extend([transition(s_i, 'ㄴ', 'N') for s_i in 'O U A I'.split()])
transitions.extend([transition(s_i, 'ㄹ', 'R') for s_i in 'O U A I'.split()])
transitions.extend([transition(s_i, c, 'L') for s_i in 'O U A I'.split() for c in 'ㄲ ㄷ ㅁ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ'.split()])
transitions.extend([transition(s_i, c, 'V') for s_i in 'O U A I'.split() for c in 'ㄸ ㅃ ㅉ'.split()])
transitions.extend([transition(s_i, c, 'O') for s_i in 'O U A I'.split() for c in 'ㄸ ㅃ ㅉ'.split()])
transitions.extend([transition('K', 'ㅅ', 'L')])
transitions.extend([transition('N', c, 'L') for c in 'ㅈ ㅎ'.split()])
transitions.extend([transition('R', c, 'L') for c in 'ㄱ ㅁ ㅂ ㅅ ㅌ ㅍ ㅎ'.split()])
transitions.extend([transition('K', c, 'V') for c in 'ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅆ ㅇ ㅈ ㅉ ㅋ ㅌ ㅍ ㅎ'.split()])
transitions.extend([transition('N', c, 'V') for c in 'ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅉ ㅋ ㅌ ㅍ'.split()])
transitions.extend([transition('R', c, 'V') for c in 'ㄲ ㄴ ㄷ ㄸ ㄹ ㅃ ㅆ ㅇ ㅈ ㅉ ㅋ'.split()])


nfa = NFA(states, sigma, , 'S', transitions)

string = raw_input("한글을 입력해주세요\n")

lexer.input(string)
tok = True

while tok:
    char = lexer.token().value
    NFA.next(char)
