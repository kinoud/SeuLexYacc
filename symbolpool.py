
class Symbol:
    def __init__(self,id,terminal=True,lexyyc_id=None):
        """
        id: str, symbol's id in lex
        lexyyc_id: int, symbol's id in lex.yy.c
        """
        self.id=id
        self.terminal=terminal
        if terminal and lexyyc_id is None:
            lexyyc_id=ord(self.id)
        self.lexyyc_id=lexyyc_id
    
    def isTerminal(self):
        return self.terminal

    def getLexyycId(self):
        return self.lexyyc_id

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return 'syb:%s'%(repr(str(self)))


class SymbolPool():

    def __init__(self):
        self._symbol_pool={} # dict[str]->Symbol
        # predefined symbols
        self.getSymbol('<eps>',autocreate=True,lexyyc_id=-1) # epsilon (null char)
        self.getSymbol('<eos>',autocreate=True,lexyyc_id=-1) # end of stream (end of input)
        self.getSymbol('<newline>',autocreate=True,lexyyc_id=ord('\n'))
        self.getSymbol('<tab>',autocreate=True,lexyyc_id=ord('\t'))
    
    def getSymbol(self,id:str,terminal=True,autocreate=False,lexyyc_id=None):
        if not autocreate:
            return self._symbol_pool[id]
        if self._symbol_pool.get(id) is None:
            self._symbol_pool[id]=Symbol(id,terminal,lexyyc_id=lexyyc_id)
            print('new symbol(%s): %s'%('ter'if terminal else'non',id))
        return self._symbol_pool[id]

so=SymbolPool() # singleton among all other modules