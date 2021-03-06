import LALR as lr
from FA import FA
import FA as fam
from symbolpool import so
from collections import deque


"""
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

class TreeNode(list):
    def __init__(self, label, children: list):
        assert children is not None, 'children of TreeNode is None'
        list.__init__(self, children)
        self._label = label
    
    def label(self):
        return self._label

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

def bind_action(p,action_id:int):
    _prod_actions[p]=_registerd_actions[action_id]

def get_action_of_prod(p):
    return _prod_actions[p]

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
_regex_specialchar='.^-[]()\\|{}'
# not need escape
_regex_normalchar='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"\'$ =<>%&/!;,:~#@'

def dot_chars_but(sybset):
    """
    sybset: set<Symbol>
    returns: set<Symbol>
    """
    ans=set()
    for i in range(256):
        c=chr(i)
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
        for syb in dot_chars_but(set([so.getSymbol('\n')])):
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
    def char__slash_raw_symbol(a,a_ch):
        c=a_ch[1]['raw']
        if c=='n':
            a['ch']=so.getSymbol('\n',autocreate=True)
        elif c=='r':
            a['ch']=so.getSymbol('\r',autocreate=True)
        elif c=='t':
            a['ch']=so.getSymbol('\t',autocreate=True)
        elif c=='v':
            a['ch']=so.getSymbol('\v',autocreate=True)
        elif c=='f':
            a['ch']=so.getSymbol('\f',autocreate=True)
        else:
            a['ch']=so.getSymbol(c,autocreate=True)

    @REGISTER_ACTION(22)
    def char__raw_symbol(a,a_ch):
        a['ch']=so.getSymbol(a_ch[0]['raw'],autocreate=True)

    @REGISTER_ACTION(23)
    def char__slash_symbol(a,a_ch):
        a['ch']=a_ch[1]['syb']
    
def build():

    global eps,eos
    eps = so.getSymbol('<eps>')
    eos = so.getSymbol('<eos>')

    for i in range(256):
        so.getSymbol(chr(i),True,True)

    lr.init()
    define_actions()

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
    bind_action(lr.adp('`char',         ['<raw>']),                 22)
    bind_action(lr.adp('`char',         ['-']),                     19)
    bind_action(lr.adp('`char',         ['^']),                     19)
    bind_action(lr.adp('`char',         ['\\','<raw>']),            21)
    for c in _regex_metachar+_regex_specialchar:
        bind_action(lr.adp('`char',     ['\\',c]),                  23)
    for c in _regex_metachar: 
        bind_action(lr.adp('`metachar', [c]),                       19)

    bind_action(lr.adp_done('`regex'),                              20)

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
t_symbol_stack=[] # stack of TreeNode
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

def pushtokenseq(seq):
    for s in seq:
        pushtoken(s)

def pushtoken(t):
    if isinstance(t,str) and len(t)==1 and t not in (_regex_metachar+_regex_specialchar):
        t=['<raw>',t]
    if isinstance(t,list):
        s=t[0]
        info=t[1]
    else:
        s=t
        info=None
    s=so.getSymbol(s)
    assert is_a_terminal(s),'token is not a terminal'
    inq.append(s)
    n=Node(s)
    if info is not None:
        n.attr['raw']=info
    
    #print('push token: %s|%s'%(str(n.attr['syb']),repr(n.attr['raw']) if info is not None else 'none'))
    t_inq.append(TreeNode(n,[s]))

def pushsyb(s,raw=True):
    if raw:s=so.getSymbol(s)
    if not is_a_terminal(s):
        print('s is not a terminal')
        return
    inq.append(s)
    t_inq.append(TreeNode(Node(s),[s]))

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
    from nltk.tree import Tree
    from nltk.draw.tree import draw_trees
    def dfsGenTree(node):
        if not isinstance(node,TreeNode):
            return node
        l=[]
        for i in node:
            l.append(dfsGenTree(i))
        return Tree(node.label(),l)
    
    draw_trees(dfsGenTree(t))

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
        print('regex parsing done, please check the results:')
        print('stacks:')
        show_stacks(showstate=False)
        if inq[0] != so.getSymbol('<start>') or state_stack[0]!=0:
            print('(if you see this line, parsing may be wrong)')
            assert 1==2
        return False
    if sinfo!=None and rinfo!=None:
        print('warning: a shift-reduce conflict happened')
        print('reduce: ',end='')
        print(rinfo['p'])
        print('shift: %s'%str(syb))

    if sinfo!=None:
        symbol_stack.append(inq.popleft())
        t_symbol_stack.append(t_inq.popleft())
        state_stack.append(sinfo)
        cur=sinfo
    elif rinfo!=None:
        p = rinfo['p']
        reduce_len = rinfo['reduce_len']
        reduce_to = rinfo['reduce_to']

        t_pa=TreeNode(Node(reduce_to),[])
        
        for _ in range(reduce_len):
            symbol_stack.pop()
            t_pa.append(t_symbol_stack.pop())
            state_stack.pop()
        
        t_pa.reverse()

        attr=t_pa.label().attr
        attr_ch=[t.label().attr for t in t_pa]
        fn_reduce_action=get_action_of_prod(p)
        fn_reduce_action(attr,attr_ch)

        # if attr.get('nfa') is not None:
        #     fam.draw(attr.get('nfa'),{'start':'orange','to':'lightgreen'})

        inq.appendleft(reduce_to)
        t_inq.appendleft(t_pa)
        cur=state_stack[-1]
    
    
    # show_stacks(showstate=False)
    # print('')
    return True
    
def get_final_nfa():
    """
    :rtype:FA
    """
    # print('rx: get nfa of "%s"'%str(t_inq[0].label().attr['syb']))
    return t_inq[0].label().attr['nfa']