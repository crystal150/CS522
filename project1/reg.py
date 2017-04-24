#-*- coding: utf-8 -*-

import sys
from nfa import NFA
from dfa import DFA, State

reload(sys)
sys.setdefaultencoding('utf-8')

class RE(object):
    def __init__(self, re):
        self.re = re.strip()
        self.inv_re = self.re[::-1]
        self.grammar = '()|?*+'

    def find_sub_re(self, i):
        if self.inv_re[i] == ')':
            paren = 1; l = i+1
            while paren > 0:
                if self.inv_re[l] == ')': paren += 1
                if self.inv_re[l] == '(': paren -= 1
                l += 1
            return l
        
        l = i
        while l != len(self.re) and self.inv_re[l] in self.grammar: l += 1
        return l

    def re_to_nfa(self, n=0):
        s = n; f = n+1
        nfa = NFA({s, f}, {'e'}, {s:{'e':{s}}, f:{'e':{f}}}, s, {f})

        char = 'e'
        buff = ''
        for i, char in enumerate(self.inv_re):
            if char in self.grammar: break
            buff += char
        if char == 'e': buff = 'e'
        if char not in self.grammar:
            nfa.V.add(buff)
            nfa.T[s][buff] = {f}
            return nfa
        print "re: %s" %self.re
        buff = buff[::-1]

        if char == ')':
            l = self.find_sub_re(i)
            print '( )\nleft: %s\nsub: %s\nright: %s' %(self.inv_re[l:][::-1], self.inv_re[i+1:l-1][::-1], buff)
            left_nfa = RE(self.inv_re[l:][::-1]).re_to_nfa(n+len(nfa.Q))
            sub_nfa = RE(self.inv_re[i+1:l-1][::-1]).re_to_nfa(n+len(nfa.Q))
            right_nfa = RE(buff).re_to_nfa(n+len(nfa.Q))
            nfa.union(left_nfa)
            nfa.union(sub_nfa)
            nfa.union(right_nfa)

            nfa.T[s]['e'].add(left_nfa.S)
            for f in left_nfa.F:
                nfa.T[f]['e'].add(sub_nfa.S)
            for f in sub_nfa.F:
                nfa.T[f]['e'].add(right_nfa.S)
            for f in right_nfa.F:
                nfa.T[f]['e'].union(nfa.F)


        elif char == '|':
            l = self.find_sub_re(i+1)
            print l
            print len(self.re), len(self.inv_re[l:]), len(self.inv_re[i+1:l]), len(buff)
            print '|\nleft: %s\nsub: %s\nright: %s' %(self.inv_re[l:][::-1], self.inv_re[i+1:l][::-1], buff)
            left_nfa = RE(self.inv_re[l:][::-1]).re_to_nfa(n+len(nfa.Q))
            sub_nfa = RE(self.inv_re[i+1:l][::-1]).re_to_nfa(n+len(nfa.Q))
            right_nfa = RE(buff).re_to_nfa(n+len(nfa.Q))
            nfa.union(left_nfa)
            nfa.union(sub_nfa)
            nfa.union(right_nfa)

            nfa.T[s]['e'].add(left_nfa.S)
            nfa.T[s]['e'].add(sub_nfa.S)
            for f in left_nfa.F:
                nfa.T[f]['e'].add(right_nfa.S)
            for f in sub_nfa.F:
                nfa.T[f]['e'].add(right_nfa.S)
            for f in right_nfa.F:
                nfa.T[f]['e'].union(nfa.F)

        elif char == '?':
            l = self.find_sub_re(i+1)
            print '?\nleft: %s\nsub: %s\nright: %s' %(self.inv_re[l:][::-1], self.inv_re[i+1:l][::-1], buff)
            left_nfa = RE(self.inv_re[l:][::-1]).re_to_nfa(n+len(nfa.Q))
            sub_nfa = RE(self.inv_re[i+1:l][::-1]).re_to_nfa(n+len(nfa.Q))
            right_nfa = RE(buff).re_to_nfa(n+len(nfa.Q))
            nfa.union(left_nfa)
            nfa.union(sub_nfa)
            nfa.union(right_nfa)

            nfa.T[s]['e'].add(left_nfa.S)
            for f in left_nfa.F:
                nfa.T[f]['e'].add(sub_nfa.S)
            nfa.T[sub_nfa.S]['e'].add(right_nfa.S)
            for f in sub_nfa.F:
                nfa.T[f]['e'].add(right_nfa.S)
            for f in right_nfa.F:
                nfa.T[f]['e'].union(nfa.F)

        elif char == '+':
            l = self.find_sub_re(i+1)
            print '+\nleft: %s\nsub: %s\nright: %s' %(self.inv_re[l:][::-1], self.inv_re[i+1:l][::-1], buff)
            left_nfa = RE(self.inv_re[l:][::-1]).re_to_nfa(n+len(nfa.Q))
            sub_nfa = RE(self.inv_re[i+1:l][::-1]).re_to_nfa(n+len(nfa.Q))
            right_nfa = RE(buff).re_to_nfa(n+len(nfa.Q))
            nfa.union(left_nfa)
            nfa.union(sub_nfa)
            nfa.union(right_nfa)

            nfa.T[s]['e'].add(left_nfa.S)
            for f in left_nfa.F:
                nfa.T[f]['e'].add(sub_nfa.S)
            for f in sub_nfa.F:
                nfa.T[f]['e'].add(right_nfa.S)
            nfa.T[right_nfa.S]['e'].add(sub_nfa.S)
            for f in right_nfa.F:
                nfa.T[f]['e'].union(nfa.F)

        elif char == '*':
            l = self.find_sub_re(i+1)
            left_nfa = RE(self.re[:-l]).re_to_nfa(n+len(nfa.Q))
            sub_nfa = RE(self.re[-l+1:-i]).re_to_nfa(n+len(nfa.Q))
            right_nfa = RE(buff).re_to_nfa(n+len(nfa.Q))
            nfa.union(left_nfa)
            nfa.union(sub_nfa)
            nfa.union(right_nfa)
            print 'left: %s\nsub: %s\nright: %s' %(self.re[:-l], self.re[-l+1:-i], buff)

            nfa.T[s]['e'].add(left_nfa.S)
            for f in left_nfa.F:
                nfa.T[f]['e'].add(sub_nfa.S)
            nfa.T[sub_nfa.S]['e'].add(right_nfa.S)
            for f in sub_nfa.F:
                nfa.T[f]['e'].add(right_nfa.S)
            nfa.T[right_nfa.S]['e'].add(sub_nfa.S)
            for f in right_nfa.F:
                nfa.T[f]['e'].union(nfa.F)

        else:
            raise("Invalid Expression")

        return nfa
