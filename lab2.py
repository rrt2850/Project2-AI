import sys
import re

kb = {
    'predicates': [],
    'variables': [],
    'constants': [],
    'functions': [],
    'clauses': []
}

        
class Predicate:
    def __init__(self, predicate, variables, negated=False):
        self.predicate = predicate
        self.variables = variables
        self.negated = negated

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.predicate == other.predicate
                and self.variables == other.variables
                and self.negated == other.negated)

    def __repr__(self):
        return '{}{}({})'.format('!' if self.negated else '', self.predicate, ', '.join(self.variables))

def parsePredicate(s):
    negated = False
    if s.startswith('!'):
        negated = True
        s = s[1:]

    i = s.find('(')
    predicate = s[:i]
    variables = []
    for v in s[i+1:-1].split(','):
        variables.append(v.strip())

    return Predicate(predicate, variables, negated)


def toPredicates(clause):
    clause = clause.split(" ")
    temp = []

    for predicate in clause:
        temp.append(parsePredicate(predicate))

    return temp


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
                kb['clauses'].append(line.strip())

    tempClauses = []

    for i in kb['clauses']:
        tempClauses.append(toPredicates(i))

    kb['clauses'] = tempClauses
    
    #print("yes" if runtimeLoop() else "no")

if __name__ == '__main__':
    main()