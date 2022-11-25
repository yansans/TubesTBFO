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
            '<<=', '>>=', '>>>=', '=>', '=', '?', ':']

unary_operator = ['+', '-', '++', '--', '!', '~']


start_state_op = 0
secondary_state_op = 1
final_state_op = 2

transition_operator = {}

# start state
transition_operator[start_state_op] = {}
for char in digits:
    transition_operator[start_state_op][char] = 2

# secondary state
transition_operator[final_state_op] = {}
for char in operator:
    transition_operator[final_state_op][char] = 1
for char in unary_operator:
    transition_operator[final_state_op][char] = 2

# final state
transition_operator[secondary_state_op] = {}
for char in digits:
    transition_operator[secondary_state_op][char] = 2

def is_legal_operation(operation):
    current_state = start_state_op
    for char in operation:
        if char == " ":
            continue
        if char in transition_operator[current_state]:
            current_state = transition_operator[current_state][char]
        else:
            return False
    if current_state == final_state_op:
        return True
    else:
        return False

if __name__ == '__main__':
    print(transition_variable)
    print(is_legal_variable('a'))
    print(is_legal_variable('var'))
    print(is_legal_operation('0 ++ '))