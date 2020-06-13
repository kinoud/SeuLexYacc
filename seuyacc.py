from seulex import LexReader,Writer
from symbolpool import so,Symbol
import LALR as lr
import os
import sys


"""
from seuyacc import *
reader=YaccReader('test.y')
writer=YaccWriter('ytabframe.c','y.tab.c')
yp=YaccProcessor(reader,writer)
while yp.step():
    pass

d=so.getSymbol('NUMBER')
ln=so.getSymbol('lines')
print(lr.getState(0))
print(lr.getAction(0,d))


NOTE:
bugs:
1. do not use ' ' as blank, it is recognized as ["'","'"] rather than [" "]
2. user defined token id must < YaccProcessor._id_of_nonter_base
"""

class YaccReader(LexReader):
    pass

class YaccWriter(Writer):
    def writeToHeaders(self,s:str):
        self.user_part[0]+=s
    
    def writeToFunctions(self,s:str):
        self.user_part[1]+=s

    def writeToActions(self,s:str):
        self.user_part[2]+=s
    
    def writeToLALR(self,s:str):
        self.user_part[3]+=s

class YaccProcessor:
    def __init__(self,reader:YaccReader,writer:YaccWriter,generateTokenH:str='',nonTerminalStartID:int=0):
        self.writer=writer
        self.reader=reader
        self.generateTokenH=generateTokenH
        self.state=0
        self.tokens=set() # set<str>
        self.action_of_p={} # dict[Production]->str
        self.start_syb=None # Symbol
        self._priority=0
        self._pri_of={}
        self._id_of_nonter={}
        # non terminal symbol id start from base
        # so, all token id user defined should < base
        self._id_of_nonter_base=nonTerminalStartID 

    
    def addToken(self,word_list):
        self.tokens.update(word_list)
        

    def declAssociation(self,word_list,associ:str):
        for word in word_list:
            syb=so.getSymbol(word,autocreate=True)
            lr.setTerminalAssoci(syb,associ)
            lr.setTerminalPriori(syb,self._priority)
            self._pri_of[syb]=self._priority
        self._priority+=1

    def declStart(self,word):
        self.start_syb=so.getSymbol(word,terminal=False,autocreate=True)

    def assignYaccId(self,syb:Symbol):
        """
        define non-terminal id used in y.tab.c
        terminal id is defined by user 
        """
        if syb.isTerminal():return
        t=self._id_of_nonter
        if t.get(syb) is not None:return
        t[syb]=len(t)+self._id_of_nonter_base

    def getYaccId(self,syb:Symbol):
        if syb==so.getSymbol('<eos>'):
            return 0
        if syb==so.getSymbol('<start>'):
            return -2
        if syb.isTerminal():return syb.id # eq str(syb)
        return self._id_of_nonter[syb]


    def addProduction(self,lhs:str,rhs:list,action:str,pri:int):
        assert lhs not in self.tokens
        L=so.getSymbol(lhs,terminal=False,autocreate=True)
        self.assignYaccId(L)
        R=[]
        for r in rhs:
            terminal=(r in self.tokens)
            if r[0]=="'": terminal=True
            syb=so.getSymbol(r,terminal=terminal,autocreate=True)
            self.assignYaccId(syb)
            R.append(syb)
        
        if pri is None:
            rightmost_ter=None
            for r in R:
                if r.isTerminal():
                    rightmost_ter=r
            pri=self._pri_of.get(rightmost_ter)

        p=lr.addProduction(L,R,pri)
        if action is not None:
            self.action_of_p[p]=action
    
    def genYtabc(self):
        w=self.writer
        for p in lr.ppool:
            id=p.id
            act=self.action_of_p.get(p)
            if act is None and len(p)>0:
                act='$$=$1;'
            if act is None:
                act=''
            # $$ -> (*_ch_val[0])
            # $1 -> (*_ch_val[1])
            # $2 -> (*_ch_val[2])
            # ...
            res=''
            flag=False
            for x in act:
                if flag:
                    if x=='$':
                        res+='(*_ch_val[0])'
                    else:
                        assert x.isdigit()
                        res+='(*_ch_val[%s])'%x
                    flag=False
                elif x=='$':
                    flag=True
                else:
                    res+=x

            fn_name='_yacc_action_p%d'%id
            
            res='void %s(){\n%s\n}\n'%(fn_name,res)
            w.writeToActions(res)
            w.writeToLALR('_action_of_p[%d]=%s;\n'%(id,fn_name))

        count=0
        for i,x,a,t in lr.actions():
            assert t in 'sr'
            x=str(self.getYaccId(x))
            if t=='s':
                j=a
                w.writeToLALR('_add_shift(%d,%d,%s); '%(i,j,x))
            else:
                p=a['p'].id
                rlen=a['reduce_len']
                rto=str(self.getYaccId(a['reduce_to']))
                w.writeToLALR('_add_reduce(%d,%s,%d,%d,%s); '%(i,x,p,rlen,rto))
            count+=1
            if count%3==0:
                w.writeToLALR('\n')
        w.writeToLALR('\n')
        

        name_of={}
        for syb in so:
            if syb.isTerminal():
                if str(syb)[0]!="'" and str(syb) not in self.tokens:
                    continue
            else:
                if self.getYaccId(syb)<0:
                    continue
            name_of[self.getYaccId(syb)]='"'+str(syb)+'"'
        name_str='int _name_of[1000];\nchar _name_str[1000][50]={\n'
        count=0
        for i,(id,name) in enumerate(name_of.items()):
            if i>0:name_str+=',\n'
            name_str+=name
            w.writeToLALR('_name_of[%s]=%d;'%(id,i))
            count+=1
            if count%4==0:
                w.writeToLALR('\n')
        name_str+='\n};'
        # print(name_str)
        w.writeToHeaders(name_str)

        w.writeDown()
    
    def genYtabh(self):
        with open(self.generateTokenH,'w') as f:
            id=256
            for token in self.tokens:
                f.write('#define '+token+' '+str(id)+'\n')
                id+=1


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
            
            self.writer.writeToHeaders(r.readLine())
            return True
        elif self.state==2:
            r.skipBlankLines()
            if r.peek(2)=='%%':
                r.readLine()
                if self._id_of_nonter_base==0:
                    self._id_of_nonter_base=256+len(self.tokens)
                print("Non-terminal start id: "+str(self._id_of_nonter_base))
                self.state=3
                return True

            meta=r.readString()
            assert meta[0]=='%'
            meta=meta[1:]
            words=[]
            r.skipc(' \t')
            while r.peek()!='\n':
                words.append(r.readString())
                r.skipc(' \t')
            if meta=='token':
                self.addToken(words)
            elif meta=='start':
                self.declStart(words[0])
            elif meta=='left':
                self.declAssociation(words,'left')
            elif meta=='right':
                self.declAssociation(words,'right')
            return True
        elif self.state==3:
            r.skipBlankLines()

            if r.peek(2)=='%%':
                self.state=4
                r.readLine()
                return True

            lhs=r.readString()
            rhs=None
            while True:
                r.skipc(' \t\n')
                rhs=[]
                if r.peek()==';':
                    r.readLine()
                    break
                assert r.peek() in '|:'
                r.readString()
                r.skipc(' \t')

                while r.peek() not in '{\n%':
                    rhs.append(r.readString())
                    r.skipc(' \t')
                
                pri=None
                action=None
                if r.peek()=='%':
                    assert r.peek(5)=='%prec'
                    r.readString()
                    syb=so.getSymbol(r.readString())
                    pri=self._pri_of[syb]
                    r.skipc(' \t')
                
                if r.peek()=='{':
                    action=r.readBlock()
                
                self.addProduction(lhs,rhs,action,pri)
            return True
        elif self.state==4:
            while r.readable():
                self.writer.writeToFunctions(r.readLine())

            lr.addProductionDone(self.start_syb)
            lr.build()

            if len(self.generateTokenH)>0:
                self.genYtabh()

            self.genYtabc()
        
        return False


if __name__=='__main__':
    outdir='.'
    argvState=0
    yaccfile=''
    generateTokenH=False
    passCnt=0
    nonTerminalStartID=0
    for i in range(len(sys.argv)):
        if passCnt>0:
            passCnt-=1
            continue
        v=sys.argv[i]
        if argvState==0:
            argvState=1
        else:
            if v[0]=='-':
                if v=='-h' or v=='--auto-gen-h':
                    generateTokenH=True
                elif v=='-s' or v=='--nonterminal-start-id':
                    nonTerminalStartID=int(sys.argv[i+1])
                    passCnt+=1
            elif argvState==1:
                argvState=2
                yaccfile=v
            elif argvState==2:
                argvState=3
                outdir=v
            elif argvState==3:
                print('Too many arguments!')
                quit()
    if argvState<2:
        print('please provide .y file')
        quit()
    print("Parameters:")
    print("Input from "+yaccfile)
    print("Output to "+outdir)
    print("generate h file: "+str(generateTokenH))
    print("Non-terminal start ID: "+(str(nonTerminalStartID) if nonTerminalStartID!=0 else 'auto'))
    assert os.path.isfile(yaccfile),'.y file not exists!'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    outfile=os.path.join(outdir,'y.tab.c')
    samedir=os.path.dirname(__file__)
    framefile=os.path.join(samedir,'ytabframe.c')
    reader=YaccReader(yaccfile)
    writer=YaccWriter(framefile,outfile)
    yp=YaccProcessor(reader,writer,os.path.join(outdir,'y.tab.h') if generateTokenH else '',nonTerminalStartID)
    while yp.step():
        pass
    