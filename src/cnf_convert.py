# CFG to CNF Algorithm

import string
from itertools import product

epsilon = "epsilon"
or_term = "'|'"

global terminal, variable
terminal = []
variable = []

def parsingCFG(file):
    # read CFG from file
    global terminal, variable
    grammar = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            left, right = line.split('->')
            left = left.strip()
            right = right.strip()
            if left not in terminal:
                variable.append(left)
            for r in right.split("|"):
                r = r.strip()
                if left not in grammar:
                    grammar[left] = [r]
                else:
                    grammar[left].append(r)

    for var in grammar.copy():
        for prod in grammar[var].copy():
            for p in prod.split():
                if isTerminal(p) and p not in terminal:
                    terminal.append(p)
                elif p not in variable and not(isTerminal(p)):
                    variable.append(p)

    grammar['OR'] = [or_term]
    variable.append('OR')
    terminal.append(or_term)
    terminal.append("' '")
    return grammar
    
def filler(word, from_char, to_char):
    options = [(c,) if c != from_char else (from_char, to_char) for c in word]
    return (''.join(o) for o in product(*options))

def removeNull(grammar):
    # remove null productions in CFG
    # removed = []
    # for var in grammar.copy():
    #     for prod in grammar[var].copy():
    #         if prod == epsilon:
    #             removed.append(var)
    #             for v in grammar.copy():
    #                 for p in grammar[v].copy():
    #                     if var in p:
    #                         newp = list(filler(p, var, epsilon))
    #                         for np in newp:
    #                             if np not in grammar[v]:
    #                                 grammar[v].append(np)

    copy_grammar = grammar.copy()

    set_epsilon = set()
    loop = True
    while(loop):
        loop = False
        for var in copy_grammar.copy():
            if not(var in set_epsilon):
                if epsilon in copy_grammar[var].copy():
                    set_epsilon.add(var)
                    loop = True

        for var in copy_grammar.copy():
                for prod in copy_grammar[var].copy():
                    for p in prod:
                        if p in set_epsilon:
                            copy_grammar[var].append(prod.replace(p, epsilon))
    # print(set_epsilon)

    for var_ep in set_epsilon:
        for var in grammar.copy():
            for prod in grammar[var].copy():
                if var_ep in prod:
                    newp = list(filler(prod, var_ep, epsilon))
                    for np in newp :
                        if np not in grammar[var]:
                            grammar[var].append(np)

    # printgrammar(grammar)
    replaceEpsilon(grammar)
    # printgrammar(grammar)
    removeBlankProd(grammar)
    # printgrammar(grammar)
    removeDuplicateProd(grammar)
    # printgrammar(grammar)
    return grammar

def removeNullDewa(CFG):
    # {'S': ['A A A', 'B', 'epsilon', 'epsilon', 'epsilon'], 
    # 'A': ["'a' A", 'B', 'epsilon', 'epsilon', 'epsilon'], 
    # 'B': ['epsilon'], 'OR': ["'|'"]}
    set_epsilon = set()
    loop = True
    grammar = CFG.copy()
    while(loop):
        loop = False
        for var in grammar:
            if not(var in set_epsilon) and epsilon in grammar[var]:
                set_epsilon.add(var)
                loop = True
                for newVar in grammar:
                    if not(newVar in set_epsilon) and not(epsilon in grammar[newVar]):
                        found = False
                        for resultGrammar in grammar[newVar]:
                            if (found == True):
                                break
                            varmid = " " + var + " "
                            varleft = var + " "
                            varright = " " + var
                            if (resultGrammar.startswith(varleft) or resultGrammar.endswith(varright) or resultGrammar.find(varmid)!=-1 or resultGrammar == var):
                                grammar[newVar].append(epsilon)
                                found = True
    
            
        
def removeDuplicateProd(grammar):
    for var in grammar.copy():
        grammar[var] = list(set(grammar[var]))
    return grammar

def removeNoProd(grammar):
    # remove no production variables
    for var in grammar.copy():
        if len(grammar[var]) == 0:
            del grammar[var]
    return grammar

def removeBlankProd(grammar):
    for var in grammar.copy():
        for prod in grammar[var].copy():
            if prod == "":
                grammar[var].remove(prod)
    return grammar


def replaceEpsilon(grammar):
    found = False
    for var in grammar.copy():
        for prod in grammar[var].copy():
            if epsilon in prod:
                if len(prod) == 7:
                    grammar[var].remove(prod)
                else:
                    np = prod.replace(epsilon, '')
                    np = np.strip()
                    # print(np)
                    grammar[var].append(np)
                    grammar[var].remove(prod)

    return grammar

def removeUnit(grammar):
    for var in grammar.copy():
        done = []
        for prod in grammar[var].copy():
            if " " not in prod:
                # print("p",p)
                if prod != var and prod not in done and not(isTerminal(prod)):
                    # print(prod)
                    grammar[var].remove(prod)
                    for p2 in grammar[prod].copy():
                        grammar[var].append(p2) 
                    done.append(prod)
    return grammar

def replaceTerminal(grammar):
    # replace terminal with variable
    replace = False
    newProd = {}
    Var = "V"
    global newvar
    i = 0
    for var in grammar.copy():
        for prod in grammar[var].copy():
            savedprod = prod
            for term in terminal:
                if term in savedprod and len(prod) > 3:
                    replace = True
                    if term in newProd:
                        newvar = newProd[term]
                    else:
                        newvar = Var + str(i)
                        i += 1
                        newProd[term] = newvar
                    newprod = savedprod.replace(term, newvar)
                    savedprod = newprod
            if replace:
                grammar[var].remove(prod)
                grammar[var].append(savedprod)
                replace = False  

    for term in newProd:
        grammar[newProd[term]] = [term]
        variable.append(newProd[term])

    return grammar

                
def isTerminal(prod):
    # terminal is enclosed by ''
    count = 0
    for p in prod:
        if p == "'":
            count += 1
    return count >= 2


def removeInvalid(grammar):
    # remove invalid productions
    # one variable productions
    invalid = False
    for var in grammar.copy():
        for prod in grammar[var].copy():
            for v in variable:
                if v == prod.strip():
                    invalid = True
                    print("Invalid Variable:", var, "->", prod)
                    grammar[var].remove(prod)
                    break
        # if invalid and len(grammar[var]) == 0:
        #     del grammar[var]

    # two or more terminal productions
    for var in grammar.copy():
        for prod in grammar[var].copy():
            count = 0
            for t in terminal:
                if t in prod:
                    count += 1
            if count > 1:
                invalid = True
                print("Invalid Terminal:", var, "->", prod)
                grammar[var].remove(prod)

    return grammar

def makeTwoVar(grammar):
    # make two variable productions
    i = 0
    for var in grammar.copy():
        for prod in grammar[var].copy():
            list_prod = []
            for p in prod.split():
                list_prod.append(p)
            if len(list_prod) > 2:
                newvar = "V" + str(i)
                while newvar in variable:
                    i += 1
                    newvar = "V" + str(i)
                i += 1
                newvar2 = "V" + str(i)
                n = len(list_prod)
                if n == 3:
                    grammar[var].remove(prod)
                    grammar[var].append(list_prod[0] + " " + newvar)
                    grammar[newvar] = [list_prod[1] + " " + list_prod[2]]
                    variable.append(newvar)
                else:
                    grammar[var].remove(prod)
                    grammar[var].append(list_prod[0] + " " + newvar)
                    grammar[newvar] = [list_prod[1] + " " + newvar2]
                    for j in range(2, n-2):
                        grammar[newvar2] = [list_prod[j] + " " + newvar2]
                    grammar[newvar2] = [list_prod[n-2] + " " + list_prod[n-1]]
                    variable.append(newvar)
                    variable.append(newvar2)

    grammar = removeDuplicateProd(grammar)
    grammar = removeNoProd(grammar)
    return grammar
                

def printgrammar(grammar):
    for var in grammar:
        print(var, '->', ' | '.join(grammar[var]))
        

if __name__ == '__main__':
    cfg = parsingCFG('test/cfgconv.txt')
    grammar = cfg.copy()
    print("Original Grammar:")
    printgrammar(grammar)


    # print(grammar)
    # print(variable)
    # print(terminal)
    # printgrammar(grammar)
    # removeNullDewa(grammar)
    nulls = removeNull(grammar)
    print("Grammar after removing null productions:")
    printgrammar(nulls)
    unit = removeUnit(nulls)
    print("Grammar after removing unit productions:")
    printgrammar(unit)
    replaceTerma = replaceTerminal(unit)
    print("Grammar after replacing terminals:")
    printgrammar(replaceTerma)
    print("Grammar after removing invalid productions:")
    invalid = removeInvalid(replaceTerma)
    printgrammar(invalid)
    print("Grammar after making two variable productions:")
    twoVar = makeTwoVar(invalid)
    printgrammar(twoVar)
    # # output
    cnf = twoVar
    filename = "test/cnf.txt"
    with open(filename, 'w') as f:
        for var in cnf:
            f.write(var + ' -> ' + ' | '.join(cnf[var]))
            f.write('\n')
        # f.write(f'epsilon = {epsilon}')
        f.close()

    # test isTerminal
    print(isTerminal("'+'"))
    print(isTerminal("'a'S"))


