import sys
import CYK_Algorithm
import cnf_convert
import string
import time
import fa

kurung = ['(' , ')']

if __name__ == "__main__":
    # cnf_convert.CFG_to_CNF_convert('grammar.txt', 'cnf.txt')
    parser = CYK_Algorithm.CYK()
    parser.insert_grammar('test/cnf.txt')
    string = ""
    with open(sys.argv[1], 'r') as source_code:
        for lines in source_code:
            string += lines.replace('\n', ' ')

    string = string.split(" ")
    print(string)
    split = False
    newstring = ""
    for i in string:
        if len(i) > 1:
            if i[0] == '"':
                for j in i:
                    newstring += j + "   "
                continue
            if i == "//":
                split = True 
                newstring += i + "   "
                continue
        if i != '':
            if split:
                for j in i:
                    newstring += j + "   "
            else:
                newstring += i + '   '
        elif i == '':
            newstring += ' '
            split = False
    
    newstring = newstring.replace(kurung[0],  " " + kurung[0] + '   ')
    newstring = newstring.replace(kurung[1], '   ' + kurung[1]  + " ")
    newstring = newstring.replace(';', '   ;')
    # newstring = newstring.replace('"', '     "      ')
    newstring += "      "
    # newstring = newstring.replace('  ', ' ')
    print(newstring)
    start = time.time()
    status = parser.check_grammar(newstring)
    end = time.time()
    if status:
        print("Accepted")
    else:
        print("Syntax Error")
    print("Exec time : ", round(end - start,2))
        
    