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
    def __init__(self,reader:YaccReader,writer:YaccWriter,generateTokenH:str='',nonTerminalStartID:int=0,enableDebugPrint:bool=False,drawTreeCode:str=''):
        self.writer=writer
        self.reader=reader
        self.generateTokenH=generateTokenH
        self.state=0
        self.tokens=set() # set<str>
        self.action_of_p={} # dict[Production]->str
        self.action_type_of_s = {} # dict[Symbol]->str
        self.start_syb=None # Symbol
        self._priority=0
        self._pri_of={}
        self._id_of_nonter={}
        self.enenableDebugPrint=enableDebugPrint
        self.drawTreeCode=drawTreeCode
        self.current_type='int'
        # non terminal symbol id start from base
        # so, all token id user defined should < base
        self._id_of_nonter_base=nonTerminalStartID 

    
    def addToken(self,word_list):
        self.tokens.update(word_list)
        for word in word_list:
            self.action_type_of_s[so.getSymbol(word,autocreate=True)]=self.current_type
        

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
        if self.enenableDebugPrint:
            w.writeToHeaders('\n#define _YACC_DBG_PRT\n')
        if len(self.drawTreeCode)>0:
            w.writeToHeaders('\n#define _YACC_DRAW_PY_CODE "%s"\n'%self.drawTreeCode)
        
        max_prod=0
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
                        res+='(*(%s*)(*(_ch_val[0])))'%self.action_type_of_s.get(p.lhs)
                    else:
                        assert x.isdigit()
                        type_str=self.action_type_of_s.get(p[int(x)-1])
                        if type_str is None:
                            type_str="int"
                        res+='(*(%s*)(*(_ch_val[%s])))'%(type_str,x)
                    flag=False
                elif x=='$':
                    flag=True
                else:
                    res+=x

            fn_name='_yacc_action_p%d'%id
            
            res='void %s(){\n(*(_ch_val[0]))=(int*)malloc(sizeof(%s));\n%s\n}\n'%(fn_name,self.action_type_of_s.get(p.lhs),res)
            w.writeToActions(res)
            w.writeToLALR('_action_of_p[%d]=%s;\n'%(id,fn_name))
            max_prod=max(max_prod,id)

        w.writeToHeaders('\n#define _LR_PROD_CNT %d\n'%(max_prod+1))
        count=0
        max_state=0
        for i,x,a,t in lr.actions():
            assert t in 'sr'
            max_state=max(max_state,i)
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
        w.writeToHeaders('\n#define _LR_STATE_CNT %d\n'%(max_state+1))
        w.writeToHeaders('#define _LR_SYMBOL_CNT %d\n'%(len(self._id_of_nonter)+self._id_of_nonter_base))
        
        

        name_of={}
        for syb in so:
            if syb.isTerminal():
                if str(syb)[0]!="'" and str(syb) not in self.tokens:
                    continue
            else:
                if self.getYaccId(syb)<0:
                    continue
            name_of[self.getYaccId(syb)]='"'+str(syb)+'"'
        name_str=''
        count=0
        max_len=0
        for i,(id,name) in enumerate(name_of.items()):
            if i>0:name_str+=',\n'
            name_str+=name
            max_len=max(max_len,len(name))
            w.writeToLALR('_name_of[%s]=%d;'%(id,i))
            count+=1
            if count%4==0:
                w.writeToLALR('\n')
        name_str=('int _name_of[%d];\nchar _name_str[%d][%d]={\n'%(count,count,max_len+1))+name_str+'\n};'
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
                assert len(words)==1,'Too many start'
                self.declStart(words[0])
            elif meta=='left':
                self.declAssociation(words,'left')
            elif meta=='right':
                self.declAssociation(words,'right')
            elif meta=='type':
                assert len(words)==1,'Too many type'
                self.current_type=words[0]
            else:
                assert False,'Unknown meta'
            return True
        elif self.state==3:
            r.skipBlankLines()

            if r.peek(2)=='%%':
                self.state=4
                r.readLine()
                return True

            if r.peek(1)=='%':
                meta=r.readString()
                meta=meta[1:]
                words=[]
                r.skipc(' \t')
                while r.peek()!='\n':
                    words.append(r.readString())
                    r.skipc(' \t')
                if meta=='type':
                    assert len(words)==1,'Too many type'
                    self.current_type=words[0]
                else:
                    assert False,'Unknown meta'


            lhs=r.readString()
            self.action_type_of_s[so.getSymbol(lhs,terminal=False,autocreate=True)]=self.current_type
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
            self.action_type_of_s[so.getSymbol('<start>')]=self.action_type_of_s[self.start_syb]

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
    drawTreeCode=''
    enableDebugPrint=False
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
                elif v=='-g' or v=='--generate-draw-tree-code':
                    drawTreeCode=sys.argv[i+1]
                    passCnt+=1
                elif v=='-d' or v=='--debug-print':
                    enableDebugPrint=True
                else:
                    assert False,'Unknown argument'
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
    yp=YaccProcessor(reader,writer,os.path.join(outdir,'y.tab.h') if generateTokenH else '',nonTerminalStartID,enableDebugPrint,drawTreeCode)
    while yp.step():
        pass
    