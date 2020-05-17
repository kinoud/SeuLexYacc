import FA as f

g=f.FA()

for i in [0,1,3,4,5,7]:
    g.addNode(i,{'accept':False})

for i in [2,6,8]:
    g.addNode(i,{'accept':True})

g.addEdge(0,1,f.eps)
g.addEdge(1,2,f.Symbol('a'))
g.addEdge(0,3,f.eps)
g.addEdge(3,4,f.Symbol('a'))
g.addEdge(4,5,f.Symbol('b'))
g.addEdge(5,6,f.Symbol('b'))
g.addEdge(0,7,f.eps)
g.addEdge(7,7,f.Symbol('a'))
g.addEdge(7,8,f.Symbol('b'))
g.addEdge(8,8,f.Symbol('b'))

g.info['start']=0

def fn_info(info_list):
    ans={}
    ans['accept']=False
    for info in info_list:
        if info['accept']==True:
            ans['accept']=True
            break
    return ans

dfa=f.get_dfa_from_nfa(g,fn_info)

print("accept state: ",end='')
for i in dfa:
    if dfa.getNodeInfo(i)['accept']==True:
        print(i,end=' ')
print('')

f.draw(dfa)

def fn_par(info):
    return 1 if info['accept']==True else 0

dfa=f.minimized_dfa(dfa,fn_par,fn_info)
f.draw(dfa)