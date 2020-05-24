import copy
from symbolpool import so
from symbolpool import Symbol


"""
import LALR as lr
lr.init()
lr.addProduction(...)
...
lr.addProductionDone(...)
lr.build()
# start state id is 0
"""

class Production:
    """
    productions don't include eps in it, 
    that is, eps won't appear anywhere in any productions
    """
    def __init__(self,lhs,rhs):
        """
        lhs:Symbol
        rhs:list[Symbol]
        """
        self.lhs=lhs
        self.rhs=rhs
        self.id=None
        for syb in rhs:
            assert syb!=eps,'error: production must not contain <eps>(epsilon)'
    
    def __getitem__(self,i):
        return self.rhs[i]

    def __len__(self):
        return len(self.rhs)
    
    def __str__(self):
        ans=str(self.lhs)+' --> '
        for s in self.rhs:
            ans+=' '+str(s)
        return ans
    
    def __repr__(self):
        return str(self)

class Item:
    def __init__(self,p,dot):
        self.p=p
        self.dot=dot
    
    def __getitem__(self,i):
        return self.p[i]
    
    def isEnd(self):
        return self.dot>=len(self.p)
    
    def __str__(self):
        ans=str(self.p.lhs)+' -->'
        for syb in self.p[0:self.dot]:
            ans+=' '+str(syb)
        ans+=' `'
        for syb in self.p[self.dot:]:
            ans+=' '+str(syb)
        return ans
    
    def __repr__(self):
        return str(self)

class ItemPool:
    def __init__(self):
        self._items={}
    def getItem(self,p:Production,dot:int,autocreate=True):
        """
        dot: dot position (numbered from 0)
        :rtype:Item
        """
        if self._items.get((p,dot)) is None:
            self._items[(p,dot)]=Item(p,dot)
        return self._items[(p,dot)]

ipool=ItemPool()

class ProductionPool:

    def __init__(self):
        self._prods_of={}
        self._productions=[]
        self._order_of={}
        self._priority_of={}

    def add(self,p:Production,priority=None):
        # TODO: check if p is unique
        self._productions.append(p)
        if self._prods_of.get(p.lhs) is None:
            self._prods_of[p.lhs]=[]
        self._prods_of[p.lhs].append(p)
        if priority is not None:
            self._priority_of[p]=priority
        self._order_of[p]=len(self._order_of)
        p.id=self._order_of[p]
    
    def getPriorityOf(self,p:Production):
        return self._priority_of.get(p)
    
    def getOrderOf(self,p:Production):
        return self._order_of.get(p)
    
    def getProdsOf(self,L:Symbol):
        assert not L.isTerminal(),'L must be non-terminal'
        return self._prods_of[L]

    def __iter__(self):
        return iter(self._productions)

    def __len__(self):
        return len(self._productions)

ppool=ProductionPool()

class State:
    def __init__(self):
        self._items=set()
        self._edges={}
        self.id=None
        self.reduceinfo={}

    def edges(self):
        for x,J in self._edges.items():
            yield (x,J)

    def clear(self):
        self._items.clear()
        self._edges.clear()
        self.reduceinfo.clear()

    def update(self,D):
        self._items.update(D)
    
    def add(self,item):
        self._items.add(item)

    def addEdge(self,x:Symbol,V):
        assert self._edges.get(x) is None
        self._edges[x]=V
    
    def getToBy(self,x:Symbol):
        """
        :rtype: State or None
        """
        return self._edges.get(x)

    def genReduceInfo(self):
        self.reduceinfo={}
        rdc=self.reduceinfo
        for item in self:
            for x in la.getLookaheads(self,item):
                if item.isEnd():
                    if rdc.get(x) is not None:
                        if ppool.getOrderOf(rdc[x]['p'])<ppool.getOrderOf(item.p):
                            continue
                    rdc[x]={'p':item.p,'reduce_len':len(item.p),'reduce_to':item.p.lhs}

    def getReduceInfo(self,x:Symbol):
        """
        :rtype: dict or None
        """
        return self.reduceinfo.get(x)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __str__(self):
        ans='I%d:\n'%self.id
        for item in self:
            ans+=str(item)

            ans+='\n\t\t\tLA: '
            for x in la.getLookaheads(self,item):
                ans+=str(x)
            ans+='\n'
        return ans

class LookaheadKeeper:

    def __init__(self):
        self.lookaheads={} # dict[State]->(dict[Item]->set<Symbol>)
        self._prop=set()

    def getLookaheads(self,I:State,item:Item):
        """
        :rtype: set
        """
        lk=self.lookaheads
        if lk.get(I) is None:
            lk[I]={}
        if lk[I].get(item) is None:
            lk[I][item]=set()
        return lk[I][item]

    def addLookaheads(self,I:State,item:Item,LAs):
        if LAs is None or len(LAs)==0:
            return False

        lk=self.lookaheads
        if lk.get(I) is None:
            lk[I]={}
        if lk[I].get(item) is None:
            lk[I][item]=set()

        sz=len(lk[I][item])
        lk[I][item].update(LAs)
        return sz != len(lk[I][item])

    def addPropagation(self,I:State,i:Item,J:State,j:Item):
        self._prop.add((I,i,J,j))

    def initLookaheads(self):
        mark=so.getSymbol('<mark>',autocreate=True)
        for I in ID2state.values():
            for it in I:
                if it != it0 and it.dot==0:continue
                T=State()
                T.add(it)
                h={it:[mark]}
                CLOSURE_LR1(T,h)
                for t in T:
                    if t.isEnd():continue
                    x=t[t.dot]
                    xI=I.getToBy(x)
                    xt=ipool.getItem(t.p,t.dot+1)
                    if mark in h[t]:
                        self.addPropagation(I,it,xI,xt)
                        h[t].remove(mark)
                    if len(h[t])>0:
                        self.addLookaheads(xI,xt,h[t])
        self.addLookaheads(I0,it0,[eos])


    def propagateLookaheads(self):
        count=0
        while True:
            count+=1
            f=False
            for I,i,J,j in self._prop:
                if self.addLookaheads(J,j,self.getLookaheads(I,i)):
                    f=True
            if not f:break

        lk=self.lookaheads
        for I in ID2state.values():
            if lk.get(I) is None:
                lk[I]={}
            CLOSURE_LR1(I,lk[I])
        return count

la=LookaheadKeeper()

eps = so.getSymbol('<eps>')
eos = so.getSymbol('<eos>')
Sp=None # the start symbol (S'-->S)
all_symbols=set([eps,eos]) # all symbols include <eps> <eos> S'
all_transymbols=set() # all symbols that cause transitions (all symbols but <eps> <eos> and S'(Sp))
fi={} # dict[Symbol]->set<Symbol>
ID2state={} # dict[int]->State
frozen2state={} # dict[frozenset<Item>]->State

priority_of_op={} # int[Symbol]->int
associ_of_op={} # int[Symbol]->int 0-left 1-right

def setTerminalAssoci(x:Symbol,associ:str):
    assert associ in ['left','right']
    associ_of_op[x] = 0 if associ=='left' else 1

def setTerminalPriori(s:Symbol,priority:int):
    priority_of_op[s] = priority

def init():
    pass

def getState(i:int):
    return ID2state[i]

def states():
    for s in ID2state.values():
        yield s

def getAction(i:int,x:Symbol):
    rinfo=getReduceInfo(i,x)
    sinfo=getShiftInfo(i,x)
    if rinfo is None:
        if sinfo is None:
            return None,''
        else:
            return sinfo,'s'
    else:
        if sinfo is None:
            return rinfo,'r'
        else:
            pp=ppool.getPriorityOf(rinfo['p'])
            po=priority_of_op.get(x)
            if pp is None or po is None:
                return sinfo,'s'
            if pp>po: return rinfo,'r'
            if pp<po: return sinfo,'s'
            if associ_of_op.get(x) == 1: # right associative
                return sinfo,'s'
            return rinfo,'r'

def getReduceInfo(i,x):
    """
    i: int, state id
    x: Symbol, lookahead
    returns: None or {'p':Production,'reduce_len':int,'reduce_to':Symbol}
    """
    U=ID2state.get(i)
    assert U is not None
    return U.getReduceInfo(x)

def getShiftInfo(i,x):
    """
    i: int, state id
    x: Symbol, lookahead
    returns: None or int, target state id
    """
    U=ID2state.get(i)
    assert U is not None
    V=U.getToBy(x)
    if V is None:
        return None
    return V.id

def actions():
    for i in ID2state.keys():
        for x in all_transymbols:
            a,t=getAction(i,x)
            if a is None:
                continue
            yield i,x,a,t
        a,t=getAction(i,eos)
        if a is None:continue 
        yield i,eos,a,t

def CLOSURE_LR1(I:State,h:dict):
    while True:
        change=False
        dI=[]
        for item in I:
            if item.isEnd():continue 
            B=item[item.dot]
            if B.isTerminal():continue 
            beta=item[item.dot+1:]
            if h.get(item) is None:
                h[item]=set()
            fb=FIRST(beta)
            if eps in fb:
                fb.remove(eps)
                fb.update(h[item])
            for p in ppool.getProdsOf(B):
                pitem=ipool.getItem(p,0)
                dI.append(pitem)
                if h.get(pitem) is None:
                    h[pitem]=set()
                sz=len(h[pitem])
                h[pitem].update(fb)
                if sz!=len(h[pitem]):change=True
        
        sz=len(I)
        I.update(dI)
        if sz!=len(I):change=True
        if not change:break
    
    return I,h

def CLOSURE_LR0(I:State):
    """
    I: State
    """
    while True:
        dI=[]
        for item in I:
            if item.isEnd():continue
            B=item[item.dot]
            if B.isTerminal():continue

            for p in ppool.getProdsOf(B):
                xitem=ipool.getItem(p,0)
                dI.append(xitem)
        
        sz=len(I)
        I.update(dI)
        if sz==len(I):break
    return I

def GOTO(I,X):
    """
    I: State
    X: Symbol
    returns: State
    """
    J=State()
    for item in I:
        if not item.isEnd() and item[item.dot]==X:
            xitem=ipool.getItem(item.p,item.dot+1)
            J.add(xitem)
    return CLOSURE_LR0(J)

def FIRST(L):
    """
    if result set is empty, eps will be added
    L: list<Symbol>
    returns: set<Symbol>
    """
    global fi,eps
    R=set()
    eps_appear=False
    for x in L:
        eps_appear=False
        if not x.isTerminal():
            for o in fi[x]:
                if o==eps:
                    eps_appear=True
                else:
                    R.add(o)
            if eps not in fi[x]:
                break
        elif x!=eps:
            R.add(x)
            break
        else: # x==eps
            eps_appear=True
    if eps_appear:
        R.add(eps)
    if len(R)==0:
        R.add(eps)
    return R

def FIRST_INIT():
    global fi,all_symbols,eps

    for x in all_symbols:
        fi[x]=set()
        if x.isTerminal():
            fi[x].add(x)

    while True:
        change=False
        for p in ppool: # all productions
            L=p.lhs # Symbol
            if len(p)==0 and eps not in fi[L]:
                fi[L].add(eps)
                change=True
            # note that no production contains <eps>
            for i,Y in enumerate(p):
                if Y.isTerminal():
                    sz=len(fi[L])
                    fi[L].add(Y)
                    change|=sz!=len(fi[L])
                
                sz=len(fi[L])

                had_eps=eps in fi[L]

                # print(Y)
                fi[L].update(fi[Y])
                if eps in fi[L] and not had_eps and i<len(p)-1:
                    fi[L].remove(eps)

                change|=sz!=len(fi[L])

                if eps not in fi[Y]:break
        if not change:break

def addProduction(lhs:Symbol,rhs:list,priority=None):
    """
    lhs: Symbol
    rhs: list<Symbol>
    priority: int
    :rtype: Production
    """

    if len(rhs)>0 and rhs[0]==eps:
        rhs.pop(0)
    all_symbols.add(lhs)
    for s in rhs:
        all_symbols.add(s)
    p=Production(lhs,rhs)

    ppool.add(p)

    print('LALR: add production:',str(p),'     [prio=',priority,']')
    return p

def addProductionDone(start:Symbol):
    global Sp,all_symbols
    Sp=so.getSymbol('<start>',terminal=False,autocreate=True)
    p=addProduction(Sp,[start])
    all_transymbols.clear()
    for syb in all_symbols:
        if syb not in [eps,Sp,eos]:
            all_transymbols.add(syb)
    return p

def adp(lhs,rhs):
    """
    adp('`X',['x',...]) is same as 
    addProduction(Symbol('X',terminal=False),[Symbol('x'),...])
    lhs:str
    rhs:list[str]
    """
    test=lambda s: s[0]=='`'
    assert test(lhs)==True,'error: lhs should be non-terminal'
    lhs=so.getSymbol(lhs[1:],terminal=False,autocreate=True)
    rhs=[so.getSymbol(s[1:],False,True) if test(s) else so.getSymbol(s,True,True) for s in rhs]
    return addProduction(lhs,rhs)

def adp_done(start):
    return addProductionDone(so.getSymbol(start[1:],False))

def dfs(I:State):
    frozen2state[frozenset(I)] = I
    id=len(ID2state)
    ID2state[id]=I
    I.id=id
    for x in all_transymbols:
        J=GOTO(I,x)
        if len(J)==0:continue
        frozenJ=frozenset(J)
        new_state=(frozen2state.get(frozenJ) is None)
        if new_state:
            I.addEdge(x,J)
            dfs(J)
        else:
            I.addEdge(x,frozen2state.get(frozenJ))
            
def build():
    print('LALR: cal FIRST...')
    FIRST_INIT()

    global it0,I0
    it0=ipool.getItem(ppool.getProdsOf(Sp)[0],0)
    I0=State()
    I0.add(it0)
    I0=CLOSURE_LR0(I0)

    print('LALR: generating LR0 states...')
    dfs(I0)

    print('LALR: generating LALR states...')
    
    la.initLookaheads()
    count=la.propagateLookaheads()

    print('LALR: lookahead propagate x%d '%count)

    all_items=0
    for I in ID2state.values():
        I.genReduceInfo()
        all_items+=len(I)

    print('LALR: %d states, %d items, %d productions'%(
        len(ID2state),all_items,len(ppool)))