import sys

kb = {
    'predicates': [],
    'variables': [],
    'constants': [],
    'functions': [],
    'clauses': []
}

def main():

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()
        for line in lines:
            words = line.split()
            if words[0] == 'Predicates:':
                kb['predicates'] = words[1:]
            elif words[0] == 'Variables:':
                kb['variables'] = words[1:]
            elif words[0] == 'Constants:':
                kb['constants'] = words[1:]
            elif words[0] == 'Functions:':
                kb['functions'] = words[1:]
            elif words[0] != 'Clauses:':
                kb['clauses'].append(tuple(words))

    print(kb)

if __name__ == '__main__':
    main()