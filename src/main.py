import sys
import CYK_Algorithm
import cnf_convert
import string
import time
import fa

kurung = ['(' , ')']

variable = ["let", "var", "const"]


if __name__ == "__main__":
    var_set = set()
    # cnf_convert.CFG_to_CNF_convert('grammar.txt', 'cnf.txt')
    parser = CYK_Algorithm.CYK()
    parser.insert_grammar('test/cnf.txt')
    string = ""
    with open(sys.argv[1], 'r') as source_code:
        for lines in source_code:
            string += lines.replace('\n', '  ')
    string = string.replace('\t', '   ')
    string = string.split(" ")
    # print(string)
    split = False
    search_var = False
    newstring = ""
    for i in string:
        if len(i) > 1:
            if i[0] == '"' and not split:
                for j in i:
                    newstring += j + "   "
                continue
            elif i == "//":
                split = True 
                newstring += i + "   "
                continue
            elif i in variable:
                newstring += i + "   "
                search_var = True
                continue
            
        if i != '':
            if split:
                for j in i:
                    newstring += j + "   "
            elif search_var:
                search_var = False
                var_set.add(i)
                newstring += i + "   "
            else:
                newstring += i + '   '
        elif i == '':
            newstring += ' '
            split = False
    
    newstring = newstring.replace(kurung[0],  " " + kurung[0] + '   ')
    newstring = newstring.replace(kurung[1], '   ' + kurung[1]  + " ")
    newstring = newstring.replace(';', '   ;  ')
    newstring = newstring.replace(':', '  :')
    newstring = newstring.replace('{', '  {  ')
    newstring = newstring.replace('}', '  }  ')
    newstring = newstring.replace('[', ' [')
    newstring = newstring.replace(']', '] ')
    # newstring = newstring.replace('"', '     "      ')
    newstring += "     "
    # newstring = newstring.replace('  ', ' ')
    # print(newstring)
    # print(var_set)
    print("Parsing...")
    start = time.time()
    status = parser.check_grammar(newstring)
    end = time.time()
    if status:
        print("Accepted")
    else:
        print("Syntax Error")
    print("Exec time :", round(end - start,2))

    print("Checking Variable...")
    start = time.time()
    status = True
    var = False
    if len(var_set) > 0:
        var = True
        for i in var_set:
            if not fa.is_legal_variable(i):
                status = False
                print("Variable Name Error :", i)
                break
    end = time.time()
    if status and var:
        print("Variable Name Accepted")
    else:
        print("No Variable Detected")
    print("Exec time :", round(end - start,2))
        

        
    