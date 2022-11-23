
class CYK:
    # CYK Algorithm Class
    # How to use :
    # 1. Create CYK class variable
    # 2. do insert_grammar(filepath) with that variable
    # 3. run check_grammar(string) to start CYK parser and will decided if string accept with given grammar
    
    def __init__(self): # initialize variable
        # CFG in CNF, map<string, list[string]>, from grammar A -> a, stored into a : [A, B, C]
        # Seperate for speedup
        self.TerminalGrammar = {} # map<char, list[string]
        self.VariableGrammar = {} # map<pair<string, string>, list[string]>
    
    def insert_grammar(self, filepath):
        with open(filepath, 'r') as file:
            for line in file.readlines():
                cfg = line.split()
                leftVar = cfg[0]
                # arrow = cfg[1]

                i = 2
                while i < len(cfg):
                    if(cfg[i][0] == "\'" and i+1 < len(cfg) and cfg[i+1][0] == "\'"):
                        space = ' '
                        if space not in self.TerminalGrammar.keys():
                            self.TerminalGrammar[space] = []
                        self.TerminalGrammar[space].append(leftVar)
                        i+=3
                    elif(cfg[i][0] == "\'"): # terminal
                        terminal = cfg[i][1:len(cfg[i])-1]
                        if terminal not in self.TerminalGrammar.keys(): # create key if not exist
                            self.TerminalGrammar[terminal] = []
                        self.TerminalGrammar[terminal].append(leftVar)
                        i+=2
                    else:
                        variable1 = cfg[i]
                        variable2 = cfg[i+1]
                        variable = (variable1, variable2) # pair<variable, variable> in CNF
                        if variable not in self.VariableGrammar.keys(): # create key if not exist
                            self.VariableGrammar[variable] = []
                        self.VariableGrammar[variable].append(leftVar)
                        i+=3
        # print(self.TerminalGrammar)
        # print(self.VariableGrammar)

    def check_grammar(self, string):
        length = len(string) # target string length
        DPTable = [[set() for __ in range(length)] for _ in range(length)] # CYK Table, matrix of list[string]
        
        # fill the bottom row with terminal rule
        for j in range(length):
            if string[j] in self.TerminalGrammar.keys():
                DPTable[length-1][j] = self.TerminalGrammar[string[j]]
        
        # fill other row with cyk DP algorithm
        for i in range(length-2,-1,-1):
            for j in range(i+1):
                cartesian_product = set()
                for k in range(length-i):
                    for A in DPTable[length-k-1][j]:
                        for B in DPTable[i+k+1][j+k+1]:
                            cartesian_product.add((A,B))
                for AB in cartesian_product:
                    if AB in self.VariableGrammar.keys():
                        for variable in self.VariableGrammar[AB]:
                            DPTable[i][j].add(variable)

        possible = "S" in DPTable[0][0] # string can be reached if the top left CYK Table contain S
        return possible
    
if __name__ == "__main__":
    tmp = CYK() # init class variable

    # import os for navigating to another directory
    import os
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]
    grammarpath = parent_directory + "\\test" + "\\cnf2.txt"

    tmp.insert_grammar(grammarpath)
    print(tmp.check_grammar("vartemp "))