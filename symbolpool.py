def dbgPrintFormat(s:str)->str:
    ans=''
    for i in s:
        if ord(i) in range(32,127):
            ans+=i if i!='\\' else '\\\\'
        else:
            ans+='\\'+hex(ord(i))[1:]
    return ans

class Symbol:
    def __init__(self,id,terminal=True,terminal_id=None):
        """
        id: str, every symbol has a unique str id
        terminal_id: int, every terminal has int id, used in lexer
        """
        self.id=id
        self.terminal=terminal
        if terminal and terminal_id is None:
            if len(self.id)>1:
                terminal_id=-1
            else:
                terminal_id=ord(self.id)
        self.terminal_id=terminal_id
    
    def isTerminal(self):
        return self.terminal

    def getLexyycId(self):
        return self.terminal_id

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return 'syb:%s'%(repr(str(self)))


class SymbolPool():

    def __init__(self):
        self._symbol_pool={} # dict[str]->Symbol
        # predefined symbols
        self.getSymbol('<eps>',autocreate=True) # epsilon (null char)
        self.getSymbol('<eos>',autocreate=True) # end of stream (end of input)
        self.getSymbol('<raw>',autocreate=True) # raw char in regex tokens
    
    def getSymbol(self,id:str,terminal=True,autocreate=False,terminal_id=None):
        if not autocreate:
            return self._symbol_pool[id]
        if self._symbol_pool.get(id) is None:
            self._symbol_pool[id]=Symbol(id,terminal,terminal_id=terminal_id)
            
            print('new symbol(%s): %s'%('ter'if terminal else'non',dbgPrintFormat(id)))
        return self._symbol_pool[id]
    
    def __iter__(self):
        return iter(self._symbol_pool.values())
    
    def __len__(self):
        return len(self._symbol_pool)

so=SymbolPool() # singleton among all other modules