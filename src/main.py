import sys
import CYK_Algorithm
import cnf_convert
import string

abc = string.ascii_letters + string.digits + string.punctuation + ""

kurung = ['(' , ')']

if __name__ == "__main__":
    # cnf_convert.CFG_to_CNF_convert('grammar.txt', 'cnf.txt')
    parser = CYK_Algorithm.CYK()
    parser.insert_grammar('test/cnf.txt')
    string = ""
    with open(sys.argv[1], 'r') as source_code:
        for lines in source_code:
            string += lines.replace('\n', ' ')
    # string += '     '
    string = string.split(' ')
    print(string)
    newstring = ""
    for i in string:
        if len(i) > 0:
            if i[0] == '"':
                for j in i:
                    newstring += j + "   "
                continue
        if i != '':
            newstring += i + '     '
    
    newstring = newstring.replace(kurung[0], kurung[0] + '     ')
    newstring = newstring.replace(kurung[1], '     ' + kurung[1])
    newstring = newstring.replace(';', '     ;')
    # newstring = newstring.replace('"', '     "      ')
    newstring += "     "
    # newstring = newstring.replace('  ', ' ')
    print(newstring)
    status = parser.check_grammar(newstring)
    if status:
        print("Accepted")
    else:
        print("Syntax Error")
        
    