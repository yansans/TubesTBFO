import string

# FA check variabel name
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
all_letter = lowercase + uppercase
digits = string.digits

other_char = ['_', '$']

first_char = list(all_letter) + other_char
second_char = first_char + list(digits)


reserved_name = ['break', 'default', 'for', 'return' , 'var' , 'const' , 'delete',
                'function', 'switch', 'while', 'case', 'else', 'if', 'throw', 'catch',
                'false', 'let', 'try', 'continue' , 'finally' , 'null', 'true']

start_state_var = 0
final_state_var = 1

transition_variable = {}

# start state
transition_variable[start_state_var] = {}
for char in first_char:
    transition_variable[start_state_var][char] = 1

# final state
transition_variable[final_state_var] = {}
for char in second_char:
    transition_variable[final_state_var][char] = 1

# reserved name
def is_reserved_name(variable):
    return variable in reserved_name


def is_legal_variable(variable):
    current_state = start_state_var
    for char in variable:
        if char in transition_variable[current_state]:
            current_state = transition_variable[current_state][char]
        else:
            return False
    if current_state == final_state_var:
        return not is_reserved_name(variable)
    else:
        return False


# FA for operator

operator = ['+', '-', '*', '/', '%', '+=', 
            '-=', '*=', '/=', '%=', '==', '!=', '===', 
            '!==', '>', '<', '>=', '<=', '&&', '||', 
             '&', '|', '^', '<<', '>>', '>>>', 
            '<<=', '>>=', '>>>=', '=>', '=']

unary_operator = ['+', '-', '++', '--', '!', '~']

ternary_op = ['?', ':']

negative = ['-']
negative_digits = []
for i in digits:
    negative_digits.append('-' + i)

start_state_op = 0
final_state_op = 1
secondary_state_op = 2
ternary_state1_op = 3

transition_operator = {}

# start state
transition_operator[start_state_op] = {}
for char in second_char:
    transition_operator[start_state_op][char] = 1

# final state
transition_operator[final_state_op] = {}
for char in operator: 
    transition_operator[final_state_op][char] = 2
for char in unary_operator:
    transition_operator[final_state_op][char] = 1
for char in second_char + negative_digits:
    transition_operator[final_state_op][char] = 1
transition_operator[final_state_op][ternary_op[0]] = 3

# secondary state
transition_operator[secondary_state_op] = {}
for char in second_char + negative_digits:
    transition_operator[secondary_state_op][char] = 1

# ternary state1
transition_operator[ternary_state1_op] = {}
for char in second_char + negative_digits:
    transition_operator[ternary_state1_op][char] = 3
transition_operator[ternary_state1_op][ternary_op[1]] = 2


def is_legal_operation(operation):
    current_state = start_state_op
    operation = split_operation(operation)
    # print(operation)
    for op in operation:
        if op in transition_operator[current_state]:
            current_state = transition_operator[current_state][op]
        else:
            return False
    if current_state == final_state_op:
        return True
    else:
        return False

def split_operation(operation):
    result = []
    var = ""
    op = ""
    for char in operation:
        if char == " ":
            continue
        if char in second_char:
            if op != "":
                result.append(op)
                op = ""
            if var != "":
                char = var + char
                var = ""
            result.append(char)
        elif char in negative:
            var += char
        elif char in operator + unary_operator + ternary_op:
            op += char
    if op != "":
        result.append(op)
    return result

if __name__ == '__main__':
    print(is_legal_variable('a'))
    print(is_legal_variable('var'))
    print(is_legal_operation('1 * -1 / 2'))
