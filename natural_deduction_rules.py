#!/usr/bin/env python


from parser import *
from term_parser import *

subgoals = []


class Theorem(object):

    def __init__(self, assumptions, conclusion):

        super(Theorem, self).__init__()
        self.assumptions = assumptions
        self.conclusion = conclusion

    def __str__(self):

        str_rep = ''

        for i in range(len(self.assumptions)):
            str_rep = str_rep + str(i + 1) + '. ' + str(self.assumptions[i]) + '\n'

        str_rep = str_rep + '\n\n ===> ' + str(self.conclusion)

        return str_rep



def conjunction_introduction(theorem):

    if not isinstance(theorem.conclusion, Conjunction):
        return False

    subgoals.remove(theorem)

    new_subgoal_1 = Theorem(theorem.assumptions, 
                            theorem.conclusion.fst_operand)

    new_subgoal_2 = Theorem(theorem.assumptions, 
                            theorem.conclusion.snd_operand)
    
    subgoals.append(new_subgoal_1)
    subgoals.append(new_subgoal_2)

    return True



def conjunction_elimination_left(theorem, assumption):

    if not isinstance(assumption, Conjunction):
        return False

    theorem.assumptions.append(assumption.fst_operand)

    return True


def conjunction_elimination_right(theorem, assumption):

    if not isinstance(assumption, Conjunction):
        return False

    theorem.assumptions.append(assumption.snd_operand)

    return True

    

def disjunction_introduction_left(theorem):

    if not isinstance(theorem.conclusion, Disjunction):
        return False

    subgoals.remove(theorem)

    new_subgoal = Theorem(theorem.assumptions, theorem.conclusion.fst_operand)
    subgoals.append(new_subgoal)

    return True


    
def disjunction_introduction_right(theorem):

    if not isinstance(theorem.conclusion, Disjunction):
        return False

    subgoals.remove(theorem)

    new_subgoal = Theorem(theorem.assumptions, theorem.conclusion.snd_operand)
    subgoals.append(new_subgoal)

    return True



def disjunction_elimination(theorem, assumption):

    if not isinstance(assumption, Disjunction):
        return False

    subgoals.remove(theorem)

    new_assumptions_1 = list(theorem.assumptions)
    new_assumptions_1.remove(assumption)
    new_assumptions_1.append(assumption.fst_operand)
    new_subgoal_1 = Theorem(new_assumptions_1, theorem.conclusion)
    subgoals.append(new_subgoal_1)
    
    new_assumptions_2 = list(theorem.assumptions)
    new_assumptions_2.remove(assumption)
    new_assumptions_2.append(assumption.snd_operand)    
    new_subgoal_2 = Theorem(new_assumptions_2, theorem.conclusion)
    subgoals.append(new_subgoal_2)

    return True



def negation_introduction(theorem):

    if not isinstance(theorem.conclusion, Not):
        return False

    subgoals.remove(theorem)

    new_assumptions = theorem.assumptions
    new_assumptions.append(theorem.conclusion.sub_formula)
    new_subgoal = Theorem(new_assumptions, FalseClass())
    
    subgoals.append(new_subgoal)

    return True



def negation_elimination(theorem, assumption):

    if not isinstance(assumption, Not) or not assumption.sub_formula in theorem.assumptions:
        return False

    theorem.assumptions.append(theorem.conclusion)

    return True



def implication_introduction(theorem):

    if not isinstance(theorem.conclusion, Implication):
        return False

    subgoals.remove(theorem)

    new_assumptions = theorem.assumptions
    new_assumptions.append(theorem.conclusion.fst_operand)
    
    new_subgoal = Theorem(new_assumptions, theorem.conclusion.snd_operand)
    subgoals.append(new_subgoal)

    return True



def modus_ponens(theorem, assumption):

    if not isinstance(assumption, Implication):
        return False

    new_assumptions = list(theorem.assumptions)
    new_assumptions.remove(assumption)

    subgoals.append(Theorem(new_assumptions, assumption.fst_operand))
    subgoals.remove(theorem)

    subgoals.append(Theorem(theorem.assumptions + [assumption.snd_operand], theorem.conclusion))

    return True



def universal_introduction(theorem):

    if not isinstance(theorem.conclusion, Forall):
        return False

    subgoals.remove(theorem)

    arbitrary_variable = Variable('X_arbitrary')

    forall_formula = theorem.conclusion
    
    new_subgoal = Theorem(theorem.assumptions,
                          forall_formula.sub_formula.substitute(
                                forall_formula.variable, arbitrary_variable))

    subgoals.append(new_subgoal)
    return True

    

def universal_elimination(theorem, assumption, term):

    if not isinstance(assumption, Forall):
        return False

    theorem.assumptions.append(assumption.sub_formula.substitute(assumption.variable, term))
    
    return True



def existential_introduction(theorem, term):

    if not isinstance(theorem.conclusion, Exists):
        return False

    subgoals.remove(theorem)

    exists_formula = theorem.conclusion


    new_conclusion = exists_formula.sub_formula.substitute(exists_formula.variable, term)
    subgoals.append(Theorem(theorem.assumptions, new_conclusion))

    return True


    
def existential_elimination(theorem, assumption):

    if not isinstance(assumption, Exists):
        return False

    arbitrary_variable = Variable('X_arbitrary')

    new_assumptions = list(theorem.assumptions)
    new_assumptions.remove(assumption)
    new_assumptions.append(assumption.sub_formula.substitute(assumption.variable, arbitrary_variable))

    subgoals.remove(theorem)
    subgoals.append(Theorem(new_assumptions, theorem.conclusion))


    return True
    


def apply_assumption(theorem):

    if not theorem.conclusion in theorem.assumptions:
        return False
    
    subgoals.remove(theorem)
    return True



def str_subgoals():

    if len(subgoals) == 0:
        return 'Success!'

    res = ''

    i = 1
    for subgoal in subgoals:
        res = res + 'Subgoal ' + str(i) + ': '
        res = res + '\n'
        i = i+1
        res = res + str(subgoal)
        res = res + '\n---------------------------------------'
        res = res + '\n'

    return res

