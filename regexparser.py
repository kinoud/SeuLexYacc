import LALR as lr
from symbolpool import so
from collections import deque
from nltk.tree import Tree
from nltk.draw.tree import draw_trees



"""
# using sample

import regexparser as rx

rx.build()
rx.clear()
rx.pushseq(list('(a|bc)*'))
rx.pusheos()
rx.step()
...
rx.step()
rx.draw(0)
"""

def build():
    """
    a few preprocess for the regex before we parse it:

    1. process "xxx"
        replaced "xxx" by xxx with escapes in it
        for example: "hello?" --> hello<slash>?
        therefore, " is not a metachar
    2. process <slash>x
        all escape be processed, that is, <slash>x is one token, not two

    """
    global eps,eos
    eps = so.getSymbol('<eps>')
    eos = so.getSymbol('<eos>')

    lr.init()
    lr.adp('`<start>',            ['`regex'])
    lr.adp('`regex',        ['`term'])
    lr.adp('`regex',        ['`term','|','`regex'])
    lr.adp('`term',         ['`factor'])
    lr.adp('`term',         ['`factor','`term'])
    lr.adp('`factor',       ['`atom'])
    lr.adp('`factor',       ['`atom','`metachar'])
    lr.adp('`atom',         ['`char'])
    lr.adp('`atom',         ['.'])
    lr.adp('`atom',         ['(','`regex',')'])
    lr.adp('`atom',         ['[','`charclass',']'])
    lr.adp('`atom',         ['[','^','`charclass',']'])
    lr.adp('`charclass',    ['`charrange'])
    lr.adp('`charclass',    ['`charrange','`charclass'])
    lr.adp('`charrange',    ['`char'])
    lr.adp('`charrange',    ['`char','-','`char'])
    for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
        lr.adp('`char',     [c])
    for c in '_"\'':
        lr.adp('`char',     [c])
    for c in '?*+^$': 
        lr.adp('`metachar', [c])

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

cur=None # current state id
symbol_stack=[]
t_symbol_stack=[]
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
    if raw:s=so.getSymbol(s,autocreate=True)
    if not is_a_terminal(s):
        print('%s is not a terminal')
        return
    inq.append(s)
    t_inq.append(s)

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

def draw(i):
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

    if rinfo!=None:
        prod_id = rinfo['prod_id']
        reduce_len = rinfo['reduce_len']
        reduce_to = rinfo['reduce_to']

        t_pa=Tree(reduce_to,[])
        
        for _ in range(reduce_len):
            symbol_stack.pop()
            t_pa.append(t_symbol_stack.pop())
            state_stack.pop()
        
        t_pa.reverse()

        inq.appendleft(reduce_to)
        t_inq.appendleft(t_pa)
        cur=state_stack[-1]
    elif sinfo!=None:
        symbol_stack.append(inq.popleft())
        t_symbol_stack.append(t_inq.popleft())
        state_stack.append(sinfo)
        cur=sinfo
    
    show_stacks(showstate=False)
    print('')
    return True
    