import sys
import CYK_Algorithm
import cnf_convert

if __name__ == "__main__":
    cnf_convert.CFG_to_CNF_convert('grammar.txt', 'cnf.txt')
    parser = CYK_Algorithm.CYK()
    parser.insert_grammar('cnf.txt')
    string = ""
    with open(sys.argv[1], 'r') as source_code:
        for lines in source_code:
            string += lines.replace('\n', ' ')
    string += '    '
    print(string)
    status = parser.check_grammar(string)
    if status:
        print("Accepted")
    else:
        print("Syntax Error")
        
    