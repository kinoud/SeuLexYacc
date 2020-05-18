
class Symbol:
    def __init__(self,id,terminal=True):
        """
        id: str, should be unique
        """
        self.id=id
        self.terminal=terminal
    
    def isTerminal(self):
        return self.terminal

    def __str__(self):
        return str(self.id)


class SymbolPool():

    def __init__(self):
        self._symbol_pool={} # dict[str]->Symbol
        # predefined symbols
        self.getSymbol('<eps>',autocreate=True) # epsilon (null char)
        self.getSymbol('<eos>',autocreate=True) # end of stream (end of input)
    
    def getSymbol(self,id:str,terminal=True,autocreate=False):
        if not autocreate:
            return self._symbol_pool[id]
        if self._symbol_pool.get(id) is None:
            self._symbol_pool[id]=Symbol(id,terminal)
            print('new symbol(%s): %s'%('ter'if terminal else'non',id))
        return self._symbol_pool[id]

so=SymbolPool() # singleton among all other modules