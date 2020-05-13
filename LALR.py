import copy

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
        for syb in rhs:
            assert syb!=eps,'error: production must not contain <eps>(epsilon)'
    
    def __getitem__(self,i):
        return self.rhs[i]

    def __len__(self):
        return len(self.rhs)

    def __hash__(self):
        return hash((self.lhs,tuple(self.rhs)))

    def __eq__(self,other):
        return self.lhs==other.lhs and self.rhs==other.rhs
    
    def __str__(self):
        ans=str(self.lhs)+' --> '
        for s in self.rhs:
            ans+=' '+str(s)
        return ans

class Item:
    def __init__(self,p,dot):
        self.p=p
        self.dot=dot
    
    def __getitem__(self,i):
        return self.p[i]
    
    def isEnd(self):
        return self.dot>=len(self.p)
    
    def __hash__(self):
        return hash((self.p,self.dot))
    
    def __eq__(self,other):
        return self.p==other.p and self.dot==other.dot
    
    def __str__(self):
        ans=str(self.p.lhs)+' -->'
        for syb in self.p[0:self.dot]:
            ans+=' '+str(syb)
        ans+=' `'
        for syb in self.p[self.dot:]:
            ans+=' '+str(syb)
        return ans

class Symbol:
    def __init__(self,uniqueID,terminal=True):
        """
        uniqueID: any type is ok but its value should be unique
        """
        self.uniqueID=uniqueID
        self.terminal=terminal
    
    def isTerminal(self):
        return self.terminal
    
    def __hash__(self):
        return hash((self.uniqueID,self.terminal))
    
    def __eq__(self,other):
        return self.uniqueID==other.uniqueID and self.terminal==other.terminal

    def __str__(self):
        return str(self.uniqueID)

class StateWrapper:
    def __init__(self,ID):
        self.ID=ID
        self.reduceinfo={}
        self.shiftinfo={}
        state=ID2state[ID]
        for i in state:
            item=getItemByID(i)
            for x in getLookAhead(i):
                if item.isEnd():
                    self.reduceinfo[x]={'prod_id':prod2ID[item.p],'reduce_len':len(item.p),'reduce_to':item.p.lhs}
        if trans.get(ID)!=None:
            self.shiftinfo=trans[ID]
    
    def getReduceInfo(self,x):
        """
        x: Symbol, lookahead
        returns: None or 
        {'prod_id':int,'reduce_len':int,'reduce_to':Symbol}
        """
        return self.reduceinfo.get(x)

    def getShiftInfo(self,x):
        """
        x: Symbol, lookahead
        returns: None or int, target state id
        """
        return self.shiftinfo.get(x)

    def __str__(self):
        ans='I%d:\n'%self.ID
        for i in ID2state[self.ID]:
            ans+='(%d) '%i
            ans+=str(getItemByID(i))

            # ans+='\n\t\t\tLA: '
            # for x in getLookAhead(i):
            #     ans+=str(x)
            ans+='\n'
        return ans

eps=Symbol('<eps>') # epsilon (null char)
eos=Symbol('<eos>') # end of stream (end of input)

def init():
    """
    initialize all global variables
    """
    global Sp,all_symbols,all_transymbols
    Sp=None # the start symbol (S'-->S)
    all_symbols=set([eps,eos]) # all symbols include <eps> <eos> S'
    all_transymbols=set() # all symbols that cause transitions (all symbols but <eps> <eos> and S')
    global prod2ID,ID2prod,productions_of,fi
    prod2ID={} # dict[Production]->int
    ID2prod={} # dict[int]->Production
    productions_of={} # dict[Symbol]->list[Productions]
    fi={} # dict[Symbol]->set<Symbol>
    global lookahead,item2ID,ID2item,prop,state2ID,ID2state,trans,state_wrappers
    lookahead={} # dict[int]->set<Symbol>
    item2ID={} # dict[item]->int
    ID2item={} # dict[int]->item
    prop={} # dict[int]->set(int) item id -> item ids, directed edges of LA propagation
    state2ID={} # dict[frozenset<int>]->int
    ID2state={} # dict[int]->frozenset<int>
    trans={} # dict[int]->(dict[Symbol]->int), transition from state to state
    state_wrappers={} # dict[int]->StateWrapper, all LALR states

def getProduction(i):
    """
    i: int, production id
    """
    return ID2prod[i]

def getReduceInfo(i,x):
    """
    i: int, state id
    x: Symbol, lookahead
    returns: None or {'prod_id':int,'reduce_len':int,'reduce_to':Symbol}
    """
    return state_wrappers[i].getReduceInfo(x)

def getShiftInfo(i,x):
    """
    i: int, state id
    x: Symbol, lookahead
    returns: None or int, target state id
    """
    return state_wrappers[i].getShiftInfo(x)

def getItemID(it):
    global item2ID,ID2item
    if item2ID.get(it)==None:
        x=item2ID[it]=len(item2ID)+1
        ID2item[x]=it
    return item2ID[it]

def getItemByID(id):
    return ID2item[id]

def addPropagation(id1,id2):
    global prop
    if prop.get(id1)==None:
        prop[id1]=set()
    prop[id1].add(id2)

def addLookAhead(id,symbolset):
    """
    id: int
    symbolset: set(Symbol) or list[Symbol]
    """
    global lookahead
    if lookahead.get(id)==None:
        lookahead[id]=set()
    sz=len(lookahead[id])
    lookahead[id].update(symbolset)
    return sz!=len(lookahead[id])

def getLookAhead(id):
    """
    id: int,item id
    returns: set<Symbol>
    """
    return lookahead[id]

def CLOSURE(I):
    """
    close I inplace
    I: set<int> set of item IDs
    """
    global eps
    mark=Symbol('<mark>') # mark must not be in the language
    while True:
        dI=[]
        for i in I:
            item=getItemByID(i)
            if item.isEnd():continue
            B=item[item.dot]
            if B.isTerminal():continue

            beta=item[item.dot+1:]
            fb=FIRST(beta+[mark])
            if eps in fb:fb.remove(eps)
            markin=False
            if mark in fb:
                markin=True
                fb.remove(mark)

            for p in productions_of[B]:
                x=getItemID(Item(p,0))
                dI.append(x)
                addLookAhead(x,fb)
                if markin:
                    addPropagation(i,x)

            # a=item.LA

            # for b in FIRST(beta+[a]):
            #    for p in productions_of[B]:
            #        dI.append(Item(p,0,b))
        sz=len(I)
        I.update(dI)
        if sz==len(I):break
        
    return I

def GOTO(I,X):
    """
    I: set<int> set of item IDs
    X: Symbol
    returns: set<int>
    """
    J=set()
    for i in I:
        item=getItemByID(i)
        if not item.isEnd() and item[item.dot]==X:
            xitem=copy.deepcopy(item)
            xitem.dot+=1
            addPropagation(getItemID(item),getItemID(xitem))
            J.add(getItemID(xitem))
    return CLOSURE(J)

def FIRST(L):
    """
    if result set is empty, eps will be added
    L: list<Symbol>
    returns: set<Symbol>
    """
    global fi,eps
    R=set()
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
        for p in ID2prod.values(): # all productions
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

def addProduction(lhs,rhs):
    """
    lhs: Symbol
    rhs: list<Symbol>
    """
    if rhs[0]==eps:
        rhs.pop(0)
    all_symbols.add(lhs)
    for s in rhs:
        all_symbols.add(s)
    p=Production(lhs,rhs)

    pid=len(ID2prod)
    ID2prod[pid]=p
    prod2ID[p]=pid

    if productions_of.get(lhs)==None:
        productions_of[lhs]=[]
    productions_of[lhs].append(p)

def adp(lhs,rhs):
    """
    adp('`X',['x',...]) is same as 
    addProduction(Symbol('X',terminal=False),[Symbol('x'),...])
    lhs:str
    rhs:list[str]
    """
    test=lambda s: s[0]=='`'
    lhs=Symbol(lhs[1:],False) if test(lhs) else Symbol(lhs)
    rhs=[Symbol(s[1:],False) if test(s) else Symbol(s) for s in rhs]
    addProduction(lhs,rhs)

def adp_done(start):
    global Sp,all_symbols,all_transymbols
    Sp=Symbol(start[1:],False)
    all_transymbols=copy.deepcopy(all_symbols)
    all_transymbols.remove(eps)
    all_transymbols.remove(Sp)
    all_transymbols.remove(eos)

def addTrans(u,x,v):
    """
    u: int, state id
    x: Symbol
    v: int, state id
    """
    if trans.get(u)==None:
        trans[u]={}
    trans[u][x]=v

def addState(I):
    """
    I: frozenset<int>
    """
    x=state2ID[I]=len(state2ID)
    ID2state[x]=I

def dfs(I):
    """
    I: frozenset(int) set of item IDs
    """
    for x in all_transymbols:
        J=frozenset(GOTO(I,x))
        if len(J)==0:continue
        flag = state2ID.get(J)==None
        if flag:
            addState(J)
        addTrans(state2ID[I],x,state2ID[J])
        if flag:
            dfs(J)

def setGrammer():
    adp('`Sp`',['`S`'])
    adp('`S`',['`C`','`C`'])
    adp('`C`',['c','`C`'])
    adp('`C`',['d'])
    adp_done('`Sp`')

def build():
    # setGrammer()
    FIRST_INIT()

    id0 = getItemID(Item(productions_of[Sp][0],0))
    addLookAhead(id0,[eos])
    I0=set([id0])
    I0=frozenset(CLOSURE(I0))
    addState(I0)

    dfs(I0)

    count=0
    while True:
        count+=1
        f=False
        for u,vs in prop.items():
            for v in vs:
                if addLookAhead(v,lookahead[u]):
                    f=True
        if not f:break
    print('LALR: propagate x%d '%count)

    for i in ID2state.keys():
        state_wrappers[i]=StateWrapper(i)
    print('LALR: %d states, %d items, %d productions'%(
        len(state_wrappers),len(ID2item),len(ID2prod)))
    
