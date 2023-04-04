import sys

kb = {
    'predicates': [],
    'variables': [],
    'constants': [],
    'functions': [],
    'clauses': []
}

facts = []

class CompoundPredicate:
    def addToFacts(self):
        if self not in facts:
            facts.append(self)

    def evaluate(self):
        if isinstance(self.predicate1, CompoundPredicate):
            left = self.predicate1.evaluate()
        else:
            left = evaluate(self.predicate1)

        if isinstance(self.predicate2, CompoundPredicate):
            right = self.predicate2.evaluate()
        else:
            right = evaluate(self.predicate2)

        match self.joinOp:
            case "and":
                return left and right
            case "or":
                return left or right
            case _:
                raise ValueError("invalid join operator")

    def __init__(self, predicate1, joinOp, predicate2):
        self.predicate1 = predicate1
        self.predicate2 = predicate2
        self.joinOp = joinOp

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.predicate1 == other.predicate1
                and self.predicate2 == other.predicate2
                and self.joinOp == other.joinOp)

    def negate(self):
        self.predicate1 = self.predicate1.negate()
        self.predicate2 = self.predicate2.negate()

    def __repr__(self):
        if isinstance(self.predicate1, CompoundPredicate):
            left = f"({self.predicate1})"
        else:
            left = str(self.predicate1)

        if isinstance(self.predicate2, CompoundPredicate):
            right = f"({self.predicate2})"
        else:
            right = str(self.predicate2)

        return f"{left} {self.joinOp} {right}"


class Predicate:
    def negate(self):
        self.negated = not self.negated
        return self

    def addToFacts(self):
        if self not in facts:
            facts.append(self)

    def __init__(self, predicate, variables):
        self.predicate = predicate
        self.variables = variables
        self.negated = False

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.predicate == other.predicate
                and self.variables == other.variables
                and self.negated == other.negated)
    
    def __and__(self, other):
        return evaluate(self) and evaluate(other)
    
    def __or__(self, other):
        return evaluate(self) or evaluate(other)
    
    def __repr__(self):
        return '{}{}({})'.format('!' if self.negated else '', self.predicate, ', '.join(self.variables))

def evaluate(predicate):
        # Evaluate the truth value of the predicate in the given fact table
        return predicate in facts

def toPredicate(s):
    negated = False
    if s.startswith('!'):
        negated = True
        s = s[1:]

    i = s.find('(')
    predicate = s[:i]
    variables = []
    for v in s[i+1:-1].split(','): variables.append(v.strip())

    if negated: return Predicate(predicate, variables).negate()
    return Predicate(predicate, variables)

def toPredicates(clause):
    clause = clause.split(" ")
    temp = []

    for predicate in clause:
        temp.append(toPredicate(predicate))

    return temp

def clauseToCompound(clause, op):
    if isinstance(clause, Predicate):
        return clause
    while len(clause) > 1:
        pred1 = clause.pop(0)
        pred2 = clause.pop(0)
        compound = CompoundPredicate(pred1, op, pred2)
        clause.insert(0, compound)
    return clause[0]


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

    
    # convert all the predicates to Predicate objects
    clauses = [toPredicates(c) for c in kb['clauses']]
    kb['clauses'] = clauses

    # iterate over the clauses
    for clause in clauses[:]:
        # check if the clause has a single predicate
        if len(clause) == 1:
            predicate = clause[0]
            # check if the fact is already in the fact table
            if predicate not in facts:
                if (predicate.negated) in facts: # check if the new fact contradicts any existing facts
                    print("no")
                    return
                # if the fact is not in the fact table, add it
                predicate.addToFacts()
            # create a new list with the remaining clauses
            clauses.remove(clause)
    clauses = [clauseToCompound(c, 'and') for c in clauses]
    superPredicate = clauseToCompound(clauses, 'or')
    factPred = clauseToCompound(facts, 'and')
    finalCompound = CompoundPredicate(factPred, 'or', superPredicate)
    print(finalCompound)
    print("yes" if finalCompound.evaluate() else "no")


if __name__ == '__main__':
    main()