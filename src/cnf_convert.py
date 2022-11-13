# CFG to CNF Algorithm

import string

epsilon = "."

def parsingCFG(file):
    # read CFG from file
    grammar = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            left, right = line.split('->')
            left = left.strip()
            right = right.strip()
            for r in right.split('|'):
                r = r.strip()
                if left not in grammar:
                    grammar[left] = [r]
                else:
                    grammar[left].append(r)
    return grammar

def removeNull(grammar):
    # remove null productions in CFG
    for var in grammar:
        for prod in grammar[var]:
            if prod == epsilon:
                grammar[var].remove(prod)
                for var2 in grammar:
                    for prod2 in grammar[var2]:
                        if var in prod2:
                            grammar[var2].append(prod2.replace(var, epsilon))
    # grammar = replaceEpsilon(grammar)
    return grammar

def replaceEpsilon(grammar):
    for var in grammar:
        for prod in grammar[var]:
            np = prod.replace(epsilon, '')
            if np != prod:
                grammar[var].append(np)
                grammar[var].remove(prod)
    return grammar

def removeUnit(grammar):
    for var in grammar:
        for prod in grammar[var]:
            if len(prod) == 1 and prod.isupper():
                grammar[var].remove(prod)
                for prod2 in grammar[prod]:
                    grammar[var].append(prod2)
    return grammar

def replaceTerminal(grammar):
    # replace terminal with new variable
    newProd = {}
    usedVar = []
    for var in grammar.copy():
        usedVar.append(var)
    newVar = []
    for var in string.ascii_uppercase:
        if var not in usedVar:
            newVar.append(var)
    i = 0
    for var in grammar.copy():
        for prod in grammar[var].copy():
            if isTerminal(str(prod)):
                # print(var)
                newvar = newVar[i]
                newprod = replaceTerm(prod, newvar)
                # print(prod, "->" ,newprod)
                term = returnTerminal(prod)
                if len(term) > 3:
                    term = term[0:3]
                # print(newvar + " -> " + term)
                grammar[var].remove(prod)
                if term not in newProd:
                    newProd [term] = [newvar]
                    grammar[var].append(newprod)
                    grammar[newvar] = [term]
                    i += 1
                else:
                    newprod = replaceTerm(prod, str(newProd[term][0]))
                    # print(newProd[term][0], "->", newprod)
                    grammar[var].append(newprod)

    return grammar
                
def isTerminal(prod):
    # terminal is enclosed by ''
    np = ""
    if len(prod) > 3:
        for p in prod:
            if not(p.isupper()) and p != epsilon:
                np += p
        prod = np
    return prod[0] == "'" and prod[-1] == "'"

def replaceTerm(prod, newvar):
    # replace terminal with new variable
    np = ""
    for p in prod:
        if not(p.isupper()) and p != epsilon:
            np += p
    newprod = prod.replace(np, newvar)
    return newprod

def returnTerminal(prod):
    # return terminal in production
    np = ""
    n = 0
    for p in prod:
        if not(p.isupper()) and p != epsilon:
            np += p
            n += 1
    prod = np
    return prod

def removeInvalid(grammar):
    # remove invalid productions
    # one variable
    list_var = []
    for var in grammar.copy():
        list_var.append(var)

    for var in grammar.copy():
        for prod in grammar[var].copy():
            for i in list_var:
                strip_prod = prod.strip(".")
                if i == strip_prod:
                    grammar[var].remove(prod)
        
    # two terminal
    for var in grammar.copy():
        for prod in grammar[var].copy():
            if isTerminal(prod):
                if (len(returnTerminal(prod)) > 3):
                    grammar[var].remove(prod)
    return grammar

def makeTwoVar(grammar):
    # make two variable productions
    newProd = {}
    usedVar = []
    for var in grammar.copy():
        usedVar.append(var)
    newVar = []
    for var in string.ascii_uppercase:
        if var not in usedVar:
            newVar.append(var)
    i = 0
    for var in grammar.copy():
        for prod in grammar[var].copy():
            for j in prod:
                if j == epsilon:
                    prod = prod.replace(j, '')
            if len(prod) > 2 and prod[0] != "'" and prod[1] != "'":
                newvar = newVar[i]
                newprod = prod.replace(prod[0:2], newvar)
                print(prod, "->" ,newprod)
                grammar[var].remove(prod)
                if prod[0:2] not in newProd:
                    newProd [prod[0:2]] = [newvar]
                    grammar[var].append(newprod)
                    grammar[newvar] = [prod[0:2]]
                    i += 1
                else:
                    newprod = prod.replace(prod[0:2], str(newProd[prod[0:2]][0]))
                    print(newProd[prod[0:2]][0], "->", newprod)
                    grammar[var].append(newprod)
    return grammar
                

def printgrammar(grammar):
    for var in grammar:
        print(var, '->', ' | '.join(grammar[var]))
        

grammar = parsingCFG('test/cfgconv.txt')
print("Original Grammar:")
printgrammar(grammar)
nulls = removeNull(grammar)
print("Grammar after removing null productions:")
printgrammar(nulls)
unit = removeUnit(nulls)
print("Grammar after removing unit productions:")
printgrammar(unit)
replaceTerma = replaceTerminal(unit)
print("Grammar after replacing terminals:")
printgrammar(replaceTerma)
invalid = removeInvalid(replaceTerma)
print("Grammar after removing invalid productions:")
printgrammar(invalid)
twoVar = makeTwoVar(invalid)
print("Grammar after making two variable productions:")
printgrammar(twoVar)

#output
cnf = twoVar
filename = "test/cnf.txt"
with open(filename, 'w') as f:
    for var in cnf:
        f.write(var + ' -> ' + ' | '.join(cnf[var]))
        f.write('\n')
    f.write(f'epsilon = {epsilon}')
    f.close()

# test isTerminal
print(isTerminal("a"))
print(isTerminal("\'a\'.S"))


