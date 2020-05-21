import LALR as lr
from FA import FA
import FA as fam
from symbolpool import so
from collections import deque
from nltk.tree import Tree
from nltk.draw.tree import draw_trees


"""
NOTE:
only supports a subset of lex-regex grammer.
not support:
"<literals>"    so, use \+ instead of "+"

import regexparser as rx

rx.build()
rx.clear()
rx.pushseq(list('(a|bc)*'))
rx.pusheos()
rx.step()
...
rx.step()
rx.draw()

"""

_nfa_of_term={}
def add_nfa(name:str,nfa:FA):
    assert _nfa_of_term.get(name) is None, 'nfa of "%s" already exists'%name
    _nfa_of_term[name]=nfa


def get_nfa_of_term(name:str):
    return _nfa_of_term[name]
    
_registerd_actions={}
_prod_actions={}

def REGISTER_ACTION(i):
    def regi(x):
        _registerd_actions[i]=x
    return regi

def bind_action(production_id:int,action_id:int):
    _prod_actions[production_id]=_registerd_actions[action_id]

def get_action_of_prod(production_id):
    return _prod_actions[production_id]

def get_char_range(syba,sybb):
    """
    syba: Symbol
    sybb: Symbol
    returns: set<Symbol>, all Symbol in [a,b]
    """
    ans=[so.getSymbol(chr(k)) for k in range(ord(str(syba)),ord(str(sybb))+1)]
    return set(ans)

"""
_regex_metachar
_regex_specialchar
_regex_normalchar
should not overlap
"""
# operator, need escape
_regex_metachar='+*?'
# need escape
_regex_specialchar='.^$[]()\\|{}'
# not need escape
_regex_normalchar='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"\'- =<>%&/!;,:~#'

def dot_chars_but(sybset):
    """
    sybset: set<Symbol>
    returns: set<Symbol>
    """
    ans=set()
    for c in _regex_metachar+_regex_normalchar:
        syb=so.getSymbol(c)
        if syb not in sybset:
            ans.add(syb)
    return ans

def define_actions():
    
    @REGISTER_ACTION(1)
    def charclass__charrange_charclass(a,a_ch):
        a['chs']=a_ch[0]['chs'].union(a_ch[1]['chs'])

    @REGISTER_ACTION(2)
    def charrange__char(a,a_ch):
        a['chs']=set([a_ch[0]['ch']])

    @REGISTER_ACTION(3)
    def charrange__char_to_char(a,a_ch):
        a['chs']=get_char_range(a_ch[0]['ch'],a_ch[2]['ch'])
    
    @REGISTER_ACTION(4)
    def atom__1_charclass_1(a,a_ch):
        nfa=FA()
        nfa.addNode(0)
        nfa.addNode(1)
        for syb in a_ch[1]['chs']:
            nfa.addEdge(0,1,syb)
        nfa.special_node['start']=0
        nfa.special_node['to']=1
        a['nfa']=nfa
    
    @REGISTER_ACTION(5)
    def atom__1_not_charclass_1(a,a_ch):
        nfa=FA()
        nfa.addNode(0)
        nfa.addNode(1)
        for syb in dot_chars_but(a_ch[2]['chs']):
            nfa.addEdge(0,1,syb)
        nfa.special_node['start']=0
        nfa.special_node['to']=1
        a['nfa']=nfa

    @REGISTER_ACTION(6)
    def atom__c_regex_c(a,a_ch):
        a['nfa']=a_ch[1]['nfa']
    
    @REGISTER_ACTION(7)
    def atom__dot(a,a_ch):
        nfa=FA()
        nfa.addNode(0)
        nfa.addNode(1)
        for syb in dot_chars_but(set()):
            nfa.addEdge(0,1,syb)
        nfa.special_node['start']=0
        nfa.special_node['to']=1
        a['nfa']=nfa
    
    @REGISTER_ACTION(8)
    def atom__char(a,a_ch):
        nfa=FA()
        nfa.addNode(0)
        nfa.addNode(1)
        nfa.addEdge(0,1,a_ch[0]['ch'])
        nfa.special_node['start']=0
        nfa.special_node['to']=1
        a['nfa']=nfa

    @REGISTER_ACTION(9)
    def atom__3_ref(a,a_ch):
        a['nfa']=get_nfa_of_term(a_ch[1]['name'])
    
    @REGISTER_ACTION(10)
    def ref__char_ref(a,a_ch):
        a['name']=str(a_ch[0]['ch'])+a_ch[1]['name']
    
    @REGISTER_ACTION(11)
    def ref__3(a,a_ch):
        a['name']=''

    @REGISTER_ACTION(12)
    def factor__atom_metachar(a,a_ch):
        op=str(a_ch[1]['ch'])
        g=a_ch[0]['nfa']
        nfa=None
        if op=='*':
            nfa=fam.nfa_star(g)
        elif op=='+':
            nfa=fam.nfa_oneormore(g)
        elif op=='?':
            nfa=fam.nfa_oneornot(g)
        a['nfa']=nfa
    
    @REGISTER_ACTION(13)
    def factor__atom(a,a_ch):
        a['nfa']=a_ch[0]['nfa']

    @REGISTER_ACTION(14)
    def term__factor_term(a,a_ch):
        g=a_ch[0]['nfa']
        h=a_ch[1]['nfa']
        a['nfa']=fam.nfa_link(g,h)
    
    @REGISTER_ACTION(15)
    def term__factor(a,a_ch):
        a['nfa']=a_ch[0]['nfa']

    @REGISTER_ACTION(16)
    def regex__term_l_regex(a,a_ch):
        g=a_ch[0]['nfa']
        h=a_ch[2]['nfa']
        a['nfa']=fam.nfa_or(g,h)
    
    @REGISTER_ACTION(17)
    def regex__term(a,a_ch):
        a['nfa']=a_ch[0]['nfa']


    @REGISTER_ACTION(18)
    def charclass__charrange(a,a_ch):
        a['chs']=a_ch[0]['chs']
    
    @REGISTER_ACTION(19)
    def char__symbol(a,a_ch):
        a['ch']=a_ch[0]['syb']
    
    @REGISTER_ACTION(20)
    def start__regex(a,a_ch):
        a['nfa']=a_ch[0]['nfa']

    @REGISTER_ACTION(21)
    def char__slash_symbol(a,a_ch):
        a['ch']=a_ch[1]['syb']
        c=str(a_ch[1]['syb'])
        if c=='n':
            a['ch']=so.getSymbol('<newline>')
        elif c=='t':
            a['ch']=so.getSymbol('<tab>')
    
def build():

    global eps,eos
    eps = so.getSymbol('<eps>')
    eos = so.getSymbol('<eos>')

    lr.init()
    define_actions()
    bind_action(lr.adp('`<start>',      ['`regex']),                20)
    bind_action(lr.adp('`regex',        ['`term']),                 17)
    bind_action(lr.adp('`regex',        ['`term','|','`regex']),    16)
    bind_action(lr.adp('`term',         ['`factor']),               15)
    bind_action(lr.adp('`term',         ['`factor','`term']),       14)
    bind_action(lr.adp('`factor',       ['`atom']),                 13)
    bind_action(lr.adp('`factor',       ['`atom','`metachar']),     12)
    
    bind_action(lr.adp('`atom',         ['{','`ref']),              9)
    bind_action(lr.adp('`ref',          ['`char','`ref']),          10)
    bind_action(lr.adp('`ref',          ['}']),                     11)
    
    bind_action(lr.adp('`atom',         ['`char']),                 8)
    bind_action(lr.adp('`atom',         ['.']),                     7)
    bind_action(lr.adp('`atom',         ['(','`regex',')']),        6)
    bind_action(lr.adp('`atom',         ['[','`charclass',']']),    4)
    bind_action(lr.adp('`atom',         ['[','^','`charclass',']']),5)
    bind_action(lr.adp('`charclass',    ['`charrange']),            18)
    bind_action(lr.adp('`charclass',    ['`charrange','`charclass']),1)
    bind_action(lr.adp('`charrange',    ['`char']),                 2)
    bind_action(lr.adp('`charrange',    ['`metachar']),             2)
    bind_action(lr.adp('`charrange',    ['`char','-','`char']),     3)
    for c in _regex_normalchar:
        bind_action(lr.adp('`char',     [c]),                       19)
    for c in _regex_normalchar+_regex_metachar+_regex_specialchar:
        bind_action(lr.adp('`char',     ['\\',c]),                  21)
    for c in _regex_metachar: 
        bind_action(lr.adp('`metachar', [c]),                       19)

    lr.adp_done('`<start>')

    lr.build()

    """
    must be done in order:
    1. adp
    2. adp_done
    3. build
    """
    # print('all terminal symbols:')
    # for syb in lr.all_symbols:
    #     if syb.isTerminal():
    #         print(syb)


class Node:
    def __init__(self,syb):
        self.attr={'syb':syb}
    def __str__(self):
        return str(self.attr['syb'])


cur=None # current state id
symbol_stack=[]
t_symbol_stack=[] # stack of Tree
state_stack=[] # stack of state IDs
inq=deque()
t_inq=deque()

def is_a_terminal(s):
    return s in lr.all_symbols

def clear():
    global cur,state_stack
    cur=0
    symbol_stack.clear()
    t_symbol_stack.clear()
    state_stack=[cur]
    inq.clear()
    t_inq.clear()
    # print(lr.state_wrappers[cur])

def pushseq(seq):
    for s in seq:
        pushsyb(s)

def pushsyb(s,raw=True):
    if raw:s=so.getSymbol(s)
    if not is_a_terminal(s):
        print('%s is not a terminal')
        return
    inq.append(s)
    t_inq.append(Tree(Node(s),[s]))

def pusheos():
    pushsyb(eos,False)

def show_stacks(showstate=True):
    if showstate: 
        print(lr.state_wrappers[cur])
    print('[ ',end='')
    for syb in symbol_stack:
        print(syb,end=' ')
    print('][ ',end='')
    for syb in inq:
        print(syb,end=' ')
    print(']')
    print('[ ',end='')
    for i in state_stack:
        print(i,end=' ')
    print(']')

def draw(i=0):
    t=t_inq[i] if i>=0 else t_symbol_stack[i]
    draw_trees(t)

def parse():
    while step():
        pass
    draw(0)

def step():
    global cur
    if len(inq)==0:
        print('did nothing')
        return False
    
    syb=inq[0]

    sinfo=lr.getShiftInfo(cur,syb)
    rinfo=lr.getReduceInfo(cur,syb)
    if sinfo==None and rinfo==None:
        print('error(or parsing is done): cannot reduce nor shift') 
        return False
    if sinfo!=None and rinfo!=None:
        print('warning: a shift-reduce conflict happened')
        print('reduce: ',end='')
        print(lr.getProduction(rinfo['prod_id']))
        print('shift: %s'%str(syb))

    if sinfo!=None:
        symbol_stack.append(inq.popleft())
        t_symbol_stack.append(t_inq.popleft())
        state_stack.append(sinfo)
        cur=sinfo
    elif rinfo!=None:
        prod_id = rinfo['prod_id']
        reduce_len = rinfo['reduce_len']
        reduce_to = rinfo['reduce_to']

        t_pa=Tree(Node(reduce_to),[])
        
        for _ in range(reduce_len):
            symbol_stack.pop()
            t_pa.append(t_symbol_stack.pop())
            state_stack.pop()
        
        t_pa.reverse()

        attr=t_pa.label().attr
        attr_ch=[t.label().attr for t in t_pa]
        fn_reduce_action=get_action_of_prod(prod_id)
        fn_reduce_action(attr,attr_ch)

        # if attr.get('nfa') is not None:
        #     fam.draw(attr.get('nfa'),{'start':'orange','to':'lightgreen'})

        inq.appendleft(reduce_to)
        t_inq.appendleft(t_pa)
        cur=state_stack[-1]
    
    
    show_stacks(showstate=False)
    print('')
    return True
    
def get_final_nfa():
    """
    :rtype:FA
    """
    print('rx: get nfa of "%s"'%str(t_inq[0].label().attr['syb']))
    return t_inq[0].label().attr['nfa']