from LALR import Symbol
from LALR import eps
from collections import deque
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt



class FA:

    def __init__(self):
        self.edge={} # dict[int]->(dict[Symbol]->set<int>)
        self._info_node={} # dict[int]->(dict[str]->any)
        self.info={} # dict[str]->any
        self.nodes=set() # set<int>
    
    def addNode(self,id,nodeinfo=None):
        """
        id: int
        nodeinfo: dict[str]->any
        returns: int, unique node id
        """
        assert id not in self.nodes,'error: node already exists'
        self.nodes.add(id)
        self.edge[id]={}
        self._info_node[id]=nodeinfo

    def getNodeInfo(self,id):
        """
        id: int, node id
        returns: dict[str]->any
        """
        return self._info_node.get(id)

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

def draw(fa:FA):
    G = nx.DiGraph(directed=True)

    for i in fa:
        G.add_node(i)

    edge_labels={}
    for i in fa:
        for syb,j_set in fa.getEdge(i).items():
            for j in j_set:
                print('add %d->%d'%(i,j))
                if i==j:
                    u='cc%d:%s'%(i,str(syb))
                    G.add_edge(i,u)
                    G.add_edge(u,i)
                    continue
                G.add_edge(i,j)
                edge_labels[(i,j)]=str(syb)
    pos = nx.spring_layout(G)

    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    nx.draw(G,pos,with_labels=True,font_size=20,node_color='lightblue',arrowsize=20, node_size=1500)
    plt.show()

def get_dfa_from_nfa(nfa:FA,fn_info_node=lambda x:None):
    """
    nfa: FA
    fn_...: lambda list<dict[str]->any>:(dict[str]->any)
    returns: FA
    """

    all_symbols=nfa.getAllSymbols()
    
    s0=nfa.info['start'] # int
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
        for syb,U in trans[T].items():
            dfa.addEdge(D_id[T],D_id[U],syb)
        if T is D0:
            dfa.info['start']=D_id[T]

    return dfa

def minimized_dfa(dfa:FA,fn_partition_id,fn_info_node):
    """
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
        
    s0=dfa.info['start']
    ans.info['start']=partition[s0]
    
    return ans