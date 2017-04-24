#-*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class DFA(object):
    def __init__(self, Q, V, T, S, F):
        self.Q = Q
        self.V = V
        self.T = T
        self.S = S
        self.F = F

    def union(self, dfa):
        self.Q.union(dfa.Q)
        self.V.union(dfa.V)
        self.T.update(dfa.T)

class State(object):
    pass

