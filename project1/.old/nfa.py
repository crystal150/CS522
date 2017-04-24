#-*- coding: utf-8 -*-

import sys
from dfa import DFA, State

reload(sys)
sys.setdefaultencoding('utf-8')

class NFA(object):
    def __init__(self, Q, V, T, S, F):
        self.Q = Q
        self.V = V
        self.T = T
        self.S = S
        self.F = F

    def __str__(self):
        res = ''
        res += "State: %s\n" %list(self.Q)
        res += "Char:  [%s]\n" %', '.join(self.V)
        res += "Begin: %s\n" %self.S
        res += "Final: %s\n" %list(self.F)
        res += "Trans:"
        for s_i in self.T:
            for v in self.T[s_i]:
                for s_j in self.T[s_i][v]:
                    res += "%s%s -> %s\n" %(s_i, v, s_j)
        return res

    def union(self, nfa):
        self.Q.union(nfa.Q)
        self.V.union(nfa.V)
        self.T.update(nfa.T)

