import FA as fam
import regexparser as rx
from symbolpool import so
import os
import sys

"""

NOTE:
at present only support a subset of lex grammer:
not support (including but not limited to):
[fixed] 1. "<literal>"      so, use \+ instead of "+"
2. /*...*/ in non-C-code part
3. A/B (match A with B behind it)

bugs:
[fixed] 1. '{' or '}' should not appear in lex action part, 
    why is that? you can check the code of LexReader.readBlock()

"""

def init():
    rx.build()

class Writer:
    def __init__(self,framefile,outputfile):
        self.frame_part=[]
        self.user_part=[]
        self.mark=[]
        assert os.path.isfile(framefile)
        self.outputfile=outputfile
        with open(framefile,'r',encoding='latin-1') as f:
            t=0
            while True:
                line=f.readline()
                if not line:
                    break
                if line[0:3]=='$$$':
                    self.user_part.append('')
                    self.mark.append(1)
                    t=1
                elif t==1 or t==0:
                    self.frame_part.append(line)
                    self.mark.append(0)
                    t=2
                else:
                    self.frame_part[-1]+=line

    def writeDown(self):
        with open(self.outputfile,'w',encoding='latin-1') as f:
            i,j=0,0
            for m in self.mark:
                if m==0:
                    f.write(self.frame_part[i])
                    i+=1
                else:
                    f.write(self.user_part[j])
                    j+=1
        print('writing %s done'%self.outputfile)

class LexWriter(Writer):
    
    def writeToHeaders(self,s:str):
        self.user_part[0]+=s
    
    def writeToFunctions(self,s:str):
        self.user_part[1]+=s

    def writeToActions(self,s:str):
        self.user_part[2]+=s
    
    def writeToDfa(self,s:str):
        self.user_part[3]+=s
    

class LexReader:

    def __init__(self,filename,verbo=False):
        assert os.path.isfile(filename)
        with open(filename,'r',encoding='latin-1') as f:
            self._buffer=f.read()
        self._p=0
        self.verbo=verbo
        pass
    
    def peek(self,k=1):
        """
        peek k chars
        """
        return self._buffer[self._p:self._p+k]

    def skipc(self,chs:str):
        p=self._p
        s=self._buffer
        while p+1<len(s) and s[p] in chs:
            p+=1
        self._p=p

    def skipBlankLines(self):
        p=self._p
        s=self._buffer
        while True:
            self._p=p
            while p+1<len(s) and s[p] in ' \t':
                p+=1
            if p==len(s)-1 or s[p]!='\n':
                break
            p+=1

    def readLine(self):
        """
        read a line (including <newline>)
        """
        p=self._p
        q=p
        while q+1<len(self._buffer) and self._buffer[q]!='\n':
            q+=1
        
        self._p=q+1
        ans=self._buffer[p:q+1]
        if self.verbo: print('read input: %s'%repr(ans))
        return ans
    
    def readString(self):
        """
        read until <blank><tab><newline> 
        """
        self.skipc(' \n\t')
        p=self._p
        s=self._buffer
        
        assert p<len(s),'no string found'

        q=p
        while q+1<len(s) and s[q] not in ' \n\t':
            q+=1
        
        self._p=q
        ans=self._buffer[p:q]
        if self.verbo: print('read input: %s'%repr(ans))
        return ans

    def readRegex(self) -> list:
        """
        difference to readString is:
        not always ends when meeting <blank>,
        e.g. [ abc]
        e.g. " "
        """
        self.skipc(' \n\t')
        p=self._p
        s=self._buffer
        assert p<len(s),'no regex found'
        hex_chars='0123456789abcdefABCDEF'
        oct_chars='01234567'

        q=p
        ans=[]
        lastTurn=''
        
        cur=0
        while True:
            x=s[q]
            if cur==0:
                if x=='\\':
                    cur=1
                    lastTurn='\\'
                    q+=1
                elif x=='[':
                    cur=2
                    ans.append(x)
                    q+=1
                elif x=='"':
                    cur=3
                    q+=1
                elif x in ' \n\t':
                    break
                else:
                    ans.append(x)
                    q+=1
            elif cur==1:
                cur=0
                lastTurn=''
                print((s[q]=='x' or s[q]=='X'),s[q+1] in hex_chars,s[q],s[q+1])
                if q+1<len(s) and (s[q]=='x' or s[q]=='X') and s[q+1] in hex_chars:
                    val=s[q+1]
                    q+=2
                    while q<len(s) and s[q] in hex_chars and len(val)<2:
                        val+=s[q]
                        q+=1
                    ans.append(['<raw>',chr(int(val,16))])
                elif s[q] in oct_chars:
                    val=s[q]
                    q+=1
                    while q<len(s) and s[q] in oct_chars and len(val)<3:
                        val+=s[q]
                        q+=1
                    ans.append(['<raw>',chr(int(val,8))])
                else:
                    ans.append('\\')
                    ans.append(x)
                    q+=1
            elif cur==2:
                if x==']':
                    cur=0
                    ans.append(x)
                    q+=1
                elif x=='\\':
                    lastTurn='\\'
                    cur=5
                    q+=1
                elif x=='\\':
                    lastTurn='\\'
                    cur=5
                    q+=1
                else:
                    ans.append(x)
                    q+=1
            elif cur==3:
                if x=='"':
                    cur=0
                    q+=1
                elif x=='\\':
                    cur=4
                    lastTurn='\\'
                    q+=1
                else:
                    if x in rx._regex_specialchar+rx._regex_metachar:
                        ans.append(['<raw>',x])
                    else:
                        ans.append(x)
                    q+=1
            elif cur==4:
                cur=3
                lastTurn=''
                if q+1<len(s) and (s[q]=='x' or s[q]=='X') and s[q+1] in hex_chars:
                    val=s[q+1]
                    q+=2
                    while q<len(s) and s[q] in hex_chars and len(val)<2:
                        val+=s[q]
                        q+=1
                    ans.append(['<raw>',chr(int(val,16))])
                elif s[q] in oct_chars:
                    val=s[q]
                    q+=1
                    while q<len(s) and s[q] in oct_chars and len(val)<3:
                        val+=s[q]
                        q+=1
                    ans.append(['<raw>',chr(int(val,8))])
                else:
                    ans.append('\\')
                    ans.append(x)
                    q+=1
            elif cur==5:
                cur=2
                lastTurn=''
                if q+1<len(s) and (s[q]=='x' or s[q]=='X') and s[q+1] in hex_chars:
                    val=s[q+1]
                    q+=2
                    while q<len(s) and s[q] in hex_chars and len(val)<2:
                        val+=s[q]
                        q+=1
                    ans.append(['<raw>',chr(int(val,16))])
                elif s[q] in oct_chars:
                    val=s[q]
                    q+=1
                    while q<len(s) and s[q] in oct_chars and len(val)<3:
                        val+=s[q]
                        q+=1
                    ans.append(['<raw>',chr(int(val,8))])
                else:
                    ans.append('\\')
                    ans.append(x)
                    q+=1
        
        if len(lastTurn)>0:
            ans.append(lastTurn)
        self._p=q
        if self.verbo: print('read input: %s'%repr(ans))
        return ans
    
    def readBlock(self):
        """
        read between first '{' and its matched '}'
        '{' and '}' not included 
        """
        self.skipc(' \n\t')
        p=self._p
        s=self._buffer
        
        assert s[p]=='{','no block found'

        q=p

        cur=0
        h=0
        while True:
            x=s[q]
            if cur==0:
                if x=='{':
                    q+=1
                    h+=1
                elif x=='}':
                    q+=1
                    h-=1
                    if h==0:break 
                elif x=='"':
                    cur=1
                    q+=1
                elif x=="'":
                    cur=3
                    q+=1
                else:
                    q+=1
            elif cur==1:
                if x=='\\':
                    cur=2
                    q+=1
                elif x=='"':
                    cur=0
                    q+=1
                else:
                    q+=1
            elif cur==2:
                cur=1
                q+=1
            elif cur==3:
                if x=='\\':
                    cur=4
                    q+=1
                elif x=="'":
                    cur=0
                    q+=1
                else:
                    q+=1
            elif cur==4:
                cur=3
                q+=1

        self._p=q
        ans=s[p+1:q-1]
        if self.verbo: print('read input: %s'%repr(ans))
        return ans

    def readable(self):
        return self._p<len(self._buffer)

class LexProcessor:

    def __init__(self,reader:LexReader,writer:LexWriter):
        self.state=0
        self.reader=reader
        self.writer=writer
        self.nfa_of_rule={} # dict[int]->FA
        self.final_dfa=None # FA
        self.ccode_of_rule={} # dict[int]->str
        self.user_ccode='' # str
        self.user_header='' # str
    
    def addDefinition(self,term:str,reg:list):
        print('new term :',term)
        print(reg)
        rx.clear()
        rx.pushtokenseq(reg)
        rx.pusheos()
        while(rx.step()):
            pass
        # rx.draw()
        nfa=rx.get_final_nfa()
        rx.add_nfa(term,nfa)
        # print(fam.draw_mermaid(nfa))
        # print()
        # fam.draw(nfa,{'start':'orange','to':'lightgreen'},verbo=True)
        

    def addRule(self,reg:list,c_code:str):
        rule_id=len(self.nfa_of_rule)
        self.ccode_of_rule[rule_id]=c_code
        print('new rule: %d'%rule_id)
        print(reg)
        rx.clear()
        rx.pushtokenseq(reg)
        rx.pusheos()
        while(rx.step()):
            pass
        # rx.draw()
        nfa=rx.get_final_nfa()
        nfa.setNodeInfo(nfa.special_node['to'],{'accept':True,'rule':rule_id})
        self.nfa_of_rule[rule_id]=nfa
        # print(fam.draw_mermaid(nfa))
        # print()
        

    def addUserCCode(self):
        """
        add user defined c code in 3rd part of lex file
        """
        r=self.reader
        while r.readable():
            self.user_ccode+=r.readLine()


    def buildFinalDFA(self):
        nfa_list=[self.nfa_of_rule[i] for i in range(len(self.nfa_of_rule))]
        start_node=[g.special_node['start'] for g in nfa_list]
        nfa,id_map=fam.merge(nfa_list)

        a=len(nfa)
        nfa.addNode(a)
        nfa.special_node['start']=a
        for i,u in enumerate(start_node):
            nfa.addEdge(a,id_map[i][u],so.getSymbol('<eps>'))
        # print(fam.draw_mermaid(nfa))
        # print()
        def fn_nodeinfo1(nodeinfo_list):
            min_rule=-1
            ans={}
            for info in nodeinfo_list:
                if info.get('accept')==True:
                    if min_rule==-1:
                        min_rule=info['rule']
                    else:
                        min_rule=min(min_rule,info['rule'])
                    ans['accept']=True
            if min_rule!=-1:
                ans['rule']=min_rule
            return ans
        
        dfa=fam.get_dfa_from_nfa(nfa,fn_nodeinfo1)
        # print(fam.draw_mermaid(dfa))
        # print()

        def fn_initial_partition(nodeinfo):
            if nodeinfo.get('accept')==True:
                return nodeinfo['rule']
            else:
                return -1
        
        def fn_nodeinfo2(nodeinfo_list):
            return nodeinfo_list[0].copy()

        dfa=fam.minimized_dfa(dfa,fn_initial_partition,fn_nodeinfo2)
        print(fam.draw_mermaid(dfa))
        print()
        self.final_dfa=dfa

    def step(self):
        r=self.reader
        if self.state==0:
            if r.peek(2)=='%{':
                r.readLine()
                self.state=1
                return True
            else:
                self.state=2
                return True
        elif self.state==1:
            if r.peek(2)=='%}':
                r.readLine()
                self.state=2
                return True
            else:
                self.user_header+=r.readLine()
                return True
        elif self.state==2:
            r.skipBlankLines()
            if r.peek(2)=='%%':
                r.readLine()
                self.state=3
                return True
            else:
                self.addDefinition(r.readString(),r.readRegex())
                return True
        elif self.state==3:
            r.skipBlankLines()
            if r.peek(2)=='%%':
                r.readLine()
                self.state=4
                return True
            else:
                self.addRule(r.readRegex(),r.readBlock())
                return True
        elif self.state==4:
            self.addUserCCode()
            self.buildFinalDFA()
            self.genLexyyc()
        
        return False
    
    def genLexyyc(self):
        assert self.final_dfa is not None
        w=self.writer
        w.writeToHeaders(self.user_header)
        w.writeToFunctions(self.user_ccode)
        dfa=self.final_dfa
        w.writeToDfa('_n=%d;_start_node=%d;\n'%(len(dfa),dfa.special_node['start']))
        count=0
        max_node_id=0
        for i,j,x in dfa.edges():
            w.writeToDfa('_dfa_set_edge(%d,%d,%d); '%(i,j,x.getLexyycId()))
            count+=1
            max_node_id=max(max_node_id,i)
            if count%3==0:w.writeToDfa('\n')
        
        for rule_id,ccode in self.ccode_of_rule.items():
            fn_name='_lex_action_%d'%rule_id
            w.writeToActions('int %s(){\n%s\n}\n'%(fn_name,ccode))

        count=0
        for u in dfa:
            if dfa.getNodeInfo(u).get('accept')==True:
                rule_id=dfa.getNodeInfo(u)['rule']
                fn_name='_lex_action_%d'%rule_id
                w.writeToDfa('_dfa_set_action(%d,%s); '%(u,fn_name))
                max_node_id=max(max_node_id,u)
                count+=1
                if count%3==0:w.writeToDfa('\n')
        w.writeToHeaders('\n#define _DFA_NODE_CNT %d\n'%(max_node_id+1))
        w.writeDown()

if __name__=='__main__':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='latin-1')
    if len(sys.argv)==1:
        print('please declare .l file')
        quit()
    outdir='.'
    lexfile=sys.argv[1]
    assert os.path.isfile(lexfile),'.l file not exists!'
    if len(sys.argv)>2:
        outdir=sys.argv[2]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    outfile=os.path.join(outdir,'lex.yy.c')

    samedir=os.path.dirname(__file__)

    with open(os.path.join(samedir,'lexyyframe.h'),'r',encoding='latin-1') as inf,open(os.path.join(outdir,'lex.yy.h'),'w',encoding='latin-1') as outf:
        outf.write(inf.read())

    framefile=os.path.join(samedir,'lexyyframe.c')

    init()
    reader=LexReader(lexfile)
    writer=LexWriter(framefile,outfile)
    lp=LexProcessor(reader,writer)
    while lp.step():
        pass
