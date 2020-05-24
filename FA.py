from symbolpool import so
from collections import deque

eps=so.getSymbol('<eps>')

class FA:

    def __init__(self):
        
        self.edge={} # dict[int]->(dict[Symbol]->set<int>)
        self._info_node={} # dict[int]->(dict[str]->str/int)
        self.special_node={} # dict[str]->int
        self.nodes=set() # set<int>
    
    def copy(self):
        """
        returns: FA
        """
        ans=FA()
        for i in self:
            ans.addNode(i,nodeinfo=self.getNodeInfo(i).copy())

        for i,j,x in self.edges():
            ans.addEdge(i,j,x)
        
        ans.special_node=self.special_node.copy()
        return ans

    def addNode(self,id,nodeinfo=None):
        """
        id: int
        nodeinfo: dict[str]->any
        returns: int, unique node id
        """
        assert id not in self.nodes,'error: node already exists'
        self.nodes.add(id)
        self.edge[id]={}
        if nodeinfo is None:
            self._info_node[id]={}
        else:
            self._info_node[id]=nodeinfo.copy()

    def getNodeInfo(self,id):
        """
        id: int, node id
        returns: dict[str]->any
        """
        return self._info_node.get(id)
    
    def setNodeInfo(self,id,params:dict):
        for k,v in params.items():
            self._info_node[id][k]=v


    def nodesBy(self,idu,syb):
        """
        idu: int, from idu
        syb: Symbol, by syb
        returns: set<Node>, to ans
        """
        return self.getEdge(idu).get(syb)
    
    def firstNodeBy(self,idu,syb):
        """
        idu: int, from idu
        syb: Symbol, by syb
        returns: int or None, to ans
        """
        ans=self.nodesBy(idu,syb)
        if ans==None or len(ans)==0:
            return None
        return next(iter(ans))

    def addEdge(self,u,v,syb):
        e=self.edge
        if e.get(u)==None:
            e[u]={}
        if e[u].get(syb)==None:
            e[u][syb]=set()
        e[u][syb].add(v)

    def getEdge(self,u):
        """
        u: int, node id
        returns: dict[Symbol]->set<int> (in DFA len(set<int>) = 1 or 0)
        """
        return self.edge.get(u)

    def edges(self):
        for i in self:
            for x,j_set in self.edge[i].items():
                for j in j_set:
                    yield (i,j,x)

    def getAllSymbols(self):
        """
        returns: set<Symbol>
        """
        all_symbols=set() # set<Symbol>
        for i in self:
            all_symbols.update(self.getEdge(i).keys())
        return all_symbols

    def move(self,T,a):
        """
        T: iter<int>
        a: Symbol
        returns frozenset<int>
        """
        ans=set()
        for u in T:
            neibor=self.nodesBy(u,a) # set<int>
            if neibor!=None:
                ans.update(neibor)
        return frozenset(ans)

    def closure(self,T):
        """
        T: iter<int>
        returns: frozenset<int>
        """
        vis={}
        ans=[]
        
        def dfs(u):
            """
            u: int
            """
            ans.append(u)
            neibor=self.nodesBy(u,eps) # set<int>
            if neibor==None:
                return
            
            for v in neibor: # v: node id
                if vis.get(v)==None:
                    vis[v]=1
                    
                    dfs(v)

        for i in T:
            dfs(i) 
        return frozenset(ans)    
        

    def __iter__(self):
        return iter(self.nodes)
    
    def __len__(self):
        return len(self.nodes)

def merge(nfa_list):
    """
    new special_node={}
    *nfa: FA(s)
    returns: FA,[id_map1,id_map2,...,id_mapx]
    """
    id_map=[]
    ans=FA()
    def addnodeedge(fa,id_map,base):
        for i in fa:
            ans.addNode(base,fa.getNodeInfo(i).copy())
            id_map[i]=base
            base+=1
        for i,j,x in fa.edges():
            ans.addEdge(id_map[i],id_map[j],x)
    base=0
    for i,g in enumerate(nfa_list):
        id_map.append({})
        addnodeedge(g,id_map[i],base)
        base+=len(g)

    return ans,id_map

def nfa_or(g:FA,h:FA):
    """
    ans = (g|h)
    g h special_node must have entry 'start' and 'to'
    returns: FA
    """
    ans,[idm,idm2]=merge([g,h])
    s1=idm[g.special_node['start']]
    t1=idm[g.special_node['to']]
    s2=idm2[h.special_node['start']]
    t2=idm2[h.special_node['to']]

    ans.addEdge(s1,s2,eps)
    ans.addEdge(t2,t1,eps)

    ans.special_node['start']=s1
    ans.special_node['to']=t1
    
    return ans

def nfa_link(g:FA,h:FA):
    """
    ans = gh
    g h special_node must have entry 'start' and 'to'
    returns: FA
    """
    ans,[idm,idm2]=merge([g,h])
    s1=idm[g.special_node['start']]
    t1=idm[g.special_node['to']]
    s2=idm2[h.special_node['start']]
    t2=idm2[h.special_node['to']]

    ans.addEdge(t1,s2,eps)

    ans.special_node['start']=s1
    ans.special_node['to']=t2
    
    return ans

def nfa_oneormore(g:FA):
    """
    ans = g+
    g special_node must have entry 'start' and 'to'
    returns: FA
    """
    ans=g.copy()
    eps=so.getSymbol('<eps>')
    s=ans.special_node['start']
    t=ans.special_node['to']
    ans.addEdge(t,s,eps)
    return ans

def nfa_oneornot(g:FA):
    """
    ans = g?
    g special_node must have entry 'start' and 'to'
    returns: FA
    """
    ans=g.copy()
    s=ans.special_node['start']
    t=ans.special_node['to']
    ans.addEdge(s,t,eps)
    return ans

def nfa_star(g:FA):
    """
    ans = g*
    g special_node must have entry 'start' and 'to'
    returns: FA
    """
    ans=g.copy()
    s=ans.special_node['start']
    t=ans.special_node['to']
    
    ans.addEdge(s,t,eps)
    ans.addEdge(t,s,eps)
    return ans

def draw_mermaid(g:FA):
    """
    returns: str, graph discription in mermaid format
    """
    print('graph TD\n')
    left= ['((','>','[']
    right=['))',']',']']
    for i in g:
        t=0
        if i==g.special_node.get('start'):
            t=1
        elif i==g.special_node.get('to'):
            t=2
        elif g.getNodeInfo(i).get('accept')==True:
            t=2
        note=''
        if g.getNodeInfo(i).get('rule') is not None:
            note='('+str(g.getNodeInfo(i).get('rule'))+')'
        print(str(i)+left[t]+'"'+str(i)+note+'"'+right[t])
    
    edge={}
    for i,j,x in g.edges():
        if edge.get((i,j)) is not None:
            edge[(i,j)]+='|'+str(x)
        else:
            edge[(i,j)]=str(x)
    for (i,j),s in edge.items():
        if s=='<eps>':
            s='eps'
        print(str(i)+'--"'+s+'"-->'+str(j))
        
    return '%d nodes %d edges'%(len(g),len(edge))

def get_dfa_from_nfa(nfa:FA,fn_info_node=lambda x:None):
    """
    nfa.special_node must have 'start' entry
    nfa: FA
    fn_...: lambda list<dict[str]->any>:(dict[str]->any)
    returns: FA
    """

    all_symbols=nfa.getAllSymbols()
    
    s0=nfa.special_node['start'] # int
    D0=nfa.closure([s0]) # frozenset<int>
    q=deque([D0])

    D_states=set() # set<frozenset<int>>
    D_states.add(D0)

    trans={} # dict[frozenset<int>]->(dict[Symbol]->frozenset<int>)

    def add_trans(U,x,V):
        """
        U: frozenset<int>
        x: Symbol
        V: frozenset<int>
        """
        if trans.get(U)==None:
            trans[U]={}
        trans[U][x]=V
    
    while len(q)>0:
        T=q.popleft()
        for a in all_symbols:
            if a==eps:
                continue
            U=nfa.closure(nfa.move(T,a))
            if len(U)!=0 and U not in D_states:
                D_states.add(U)
                q.append(U)
            if len(U)!=0:
                add_trans(T,a,U)

    dfa=FA()

    D_id={} # dict[int]->frozenset<int>

    for T in D_states:
        mem_info=[]
        # T: frozenset<int>
        for id in T:
            mem_info.append(nfa.getNodeInfo(id))
        u=len(dfa)
        D_id[T]=u
        dfa.addNode(u,fn_info_node(mem_info))
        
    for T in D_states:
        if trans.get(T) is not None:
            for syb,U in trans[T].items():
                dfa.addEdge(D_id[T],D_id[U],syb)
        if T is D0:
            dfa.special_node['start']=D_id[T]

    return dfa

def minimized_dfa(dfa:FA,fn_partition_id,fn_info_node):
    """
    dfa.info must have 'start' entry
    dfa: FA
    fn_...: lambda int:int, 
        initial partition function,
        fn(node_info) = partition_id (initial)
    returns: FA
    """
    partition={}
    for i in dfa:
        partition[i]=fn_partition_id(dfa.getNodeInfo(i))
    
    all_symbols=dfa.getAllSymbols()
    
    goes_to={}
    s={}
    while True:
        partition_happen=False
        for a in all_symbols: # Symbol
            for i in dfa:
                node_to=dfa.firstNodeBy(i,a)
                goes_to[i]=partition.get(node_to)
            s_len=len(s)
            s.clear()
            for i in dfa:
                x=(partition[i],goes_to[i])
                if s.get(x)==None:
                    s[x]=len(s)
                partition[i]=s[x]
            if len(s)!=s_len:
                partition_happen=True
        if not partition_happen:
            break
    
    trans={} # dict[int]->(dict[Symbol]->int), map partition_id to (...->partition_id)
    par_info={} # dict[partition_id]->list[node_info]

    for i in dfa:
        p=partition[i]
        if par_info.get(p)==None:
            par_info[p]=[]
        par_info[p].append(dfa.getNodeInfo(i))
        if trans.get(p)!=None:
            continue
        trans[p]={}
        for a in all_symbols:
            node_to=dfa.firstNodeBy(i,a)
            if node_to==None:
                continue
            trans[p][a]=partition[node_to]
    
    ans=FA()
    for p in trans.keys(): 
        ans.addNode(p,fn_info_node(par_info[p]))

    for i,edges in trans.items():
        for syb,j in edges.items():
            ans.addEdge(i,j,syb)
        
    s0=dfa.special_node['start']
    ans.special_node['start']=partition[s0]
    
    return ans