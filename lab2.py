import sys

kb = {
    'predicates': [],
    'variables': [],
    'constants': [],
    'functions': [],
    'clauses': []
}

facts = {}
        
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

def evaluateClause(clause):
    for predicate in clause:
        negated = predicate.negated
        found = False
        for fact in kb['clauses']:
            if predicate == fact and not negated:
                found = True
                break
            elif predicate == fact and negated:
                return False
        if not found and negated:
            return True
    return True



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

    # convert all the predicates to Predicate objects
    clauses = [toPredicates(c) for c in kb['clauses']]
    kb['clauses'] = clauses

    for clause in clauses:
        if len(clause) == 1:
            predicate = clause[0]
            if predicate.negated:
                # if the fact is negated, we can just skip it
                continue
            factKey = predicate.predicate
            
            if factKey not in facts:
                facts[factKey] = []
            facts[factKey].extend(predicate.variables)
            clauses.remove(clause)

    print(facts)
        


    

if __name__ == '__main__':
    main()
