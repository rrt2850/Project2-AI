import sys
from typing import Dict

kb = {
    'predicates': [],
    'variables': [],
    'constants': [],
    'functions': [],
    'clauses': []
}


class Predicate:
    def negate(self):
        self.negated = not self.negated
        return self

    def __init__(self, predicate, variables):
        self.predicate = predicate
        self.variables = variables
        self.negated = False

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.predicate == other.predicate
                and self.variables == other.variables
                and self.negated == other.negated)

    def __repr__(self):
        return '{}{}({})'.format('!' if self.negated else '', self.predicate, ', '.join(self.variables))


def toPredicate(s):
    negated = False
    if s.startswith('!'):
        negated = True
        s = s[1:]

    i = s.find('(')
    predicate = s[:i]
    variables = [v.strip() for v in s[i + 1:-1].split(',')]

    if negated:
        return Predicate(predicate, variables).negate()
    return Predicate(predicate, variables)


def toPredicates(clause):
    clause = clause.split(" ")
    temp = []

    for predicate in clause:
        temp.append(toPredicate(predicate))

    return temp

def unify_terms(term1: str, term2: str, substitutions: Dict[str, str]) -> Dict[str, str]:
    if term1 == term2:
        return substitutions
    if term1 in kb['variables']:
        return unify_variable(term1, term2, substitutions)
    if term2 in kb['variables']:
        return unify_variable(term2, term1, substitutions)
    return None

def unify_variable(var: str, x: str, substitutions: Dict[str, str]) -> Dict[str, str]:
    if var in substitutions:
        return unify_terms(substitutions[var], x, substitutions)
    if x in substitutions:
        return unify_terms(var, substitutions[x], substitutions)
    substitutions[var] = x
    return substitutions

def unify(p1: Predicate, p2: Predicate) -> Dict[str, str]:
    if p1.predicate != p2.predicate or len(p1.variables) != len(p2.variables):
        return None

    substitutions = {}
    for term1, term2 in zip(p1.variables, p2.variables):
        substitutions = unify_terms(term1, term2, substitutions)
        if substitutions is None:
            return None

    return substitutions

def resolution(c1, c2):
    for literal1 in c1:
        neg_literal1 = literal1.negate()
        for literal2 in c2:
            substitutions = unify(neg_literal1, literal2)
            if substitutions is not None:
                new_clause = [l for l in c1 if l != literal1] + [l for l in c2 if l != literal2]
                new_clause = [Predicate(p.predicate, [substitutions.get(v, v) for v in p.variables]) for p in new_clause]
                return new_clause
    return None

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

    clauses = [toPredicates(c) for c in kb['clauses']]

    resolved = set()
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                if (i, j) not in resolved:
                    new_clause = resolution(clauses[i], clauses[j])
                    if new_clause is not None:
                        new_clauses.append(new_clause)
                        resolved.add((i, j))

        if not new_clauses:
            print("yes")  # The knowledge base is satisfiable
            break

        empty_clause_found = False
        for new_clause in new_clauses:
            # Check for contradictions (empty clauses)
            if not new_clause:
                print("no")  # The knowledge base is not satisfiable
                empty_clause_found = True
                break

            if new_clause not in clauses:
                clauses.append(new_clause)

        if empty_clause_found:
            break

if __name__ == '__main__':
    main()
