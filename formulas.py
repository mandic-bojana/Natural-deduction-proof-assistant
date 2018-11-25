class Formula(object):
    
    def __init__(self):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not self == other

    def substitute(self, x, term):
        pass
        
    def free_vars(self):
        pass

class BinaryFormula(Formula):

    def __init__(self, fst_operand, snd_operand, operator):
        
        super(BinaryFormula, self).__init__()
        self.fst_operand = fst_operand
        self.snd_operand = snd_operand
        self.operator = operator

    def __str__(self):
        
        return str(self.fst_operand) + self.operator + str(self.snd_operand)

    
    def free_vars(self):
        free_vars_set = free_vars(self.fst_operand) + free_vars(self.snd_operand)
        return free_vars

    

class Conjunction(BinaryFormula):

    def __init__(self, fst_operand, snd_operand):

        super(Conjunction, self).__init__(fst_operand, snd_operand, ' /\\ ')

    def __eq__(self, other):
        if not isinstance(other, Conjunction):
            return False
        return self.operator == other.operator and self.fst_operand == other.fst_operand and self.snd_operand == other.snd_operand
        
    def substitute(self, x, term):
        return Conjunction(self.fst_operand.substitute(x, term),
                           self.snd_operand.substitute(x, term))

class Disjunction(BinaryFormula):

    def __init__(self, fst_operand, snd_operand):

        super(Disjunction, self).__init__(fst_operand, snd_operand, ' \\/ ')

    def __eq__(self, other):
        if not isinstance(other, Disjunction):
            return False
        return self.operator == other.operator and self.fst_operand == other.fst_operand and self.snd_operand == other.snd_operand
        
    def substitute(self, x, term):
        return Disjunction(self.fst_operand.substitute(x, term),
                            self.snd_operand.substitute(x, term))

                           
class Implication(BinaryFormula):

    def __init__(self, fst_operand, snd_operand):

        super(Implication, self).__init__(fst_operand, snd_operand, ' -> ')


    def substitute(self, x, term):
        return Implication(self.fst_operand.substitute(x, term),
                            self.snd_operand.substitute(x, term))
                           
    def __eq__(self, other):
        if not isinstance(other, Implication):
            return False
        return self.operator == other.operator and self.fst_operand == other.fst_operand and self.snd_operand == other.snd_operand
   

class Equivalention(BinaryFormula):

    def __init__(self, fst_operand, snd_operand):

        super(Equivalention, self).__init__(fst_operand, snd_operand, ' <=> ')

    def substitute(self, x, term):
        return Equivalention(self.fst_operand.substitute(x, term),
                              self.snd_operand.substitute(x, term))
    
    def __eq__(self, other):
        if not isinstance(other, Equivalention):
            return False
        return self.operator == other.operator and self.fst_operand == other.fst_operand and self.snd_operand == other.snd_operand
   

    
class Quantifier(Formula):

    def __init__(self, variable, sub_formula, symbol):

        super(Quantifier, self).__init__()
        self.variable = variable
        self.sub_formula = sub_formula
        self.symbol = symbol

    def __str__(self):
        
        return self.symbol + ' ' + str(self.variable) + ': ' + str(self.sub_formula)

    
    def free_vars(self):
        free_vars_set = free_vars(self.sub_formula)
        free_vars.remove(self.variable)
        return free_vars

        

class Forall(Quantifier):

    def __init__(self, variable, sub_formula):

        super(Forall, self).__init__(variable, sub_formula, 'forall')

    def __eq__(self, other):
        if not isinstance(other, Forall):
            return False
        return self.variable == other.variable and self.sub_formula == other.sub_formula
    

    
    def substitute(self, x, term):
        if x == self.variable:
            return self
        elif term == self.variable:
            new_variable = new_var()
            return Forall(new_variable, self.sub_formula.substitute(self.variable, new_variable).substitute(x, term))
        else:
            return Exists(self.variable, self.sub_formula.substitute(x, term))
    
class Exists(Quantifier):

    def __init__(self, variable, sub_formula):

        super(Exists, self).__init__(variable, sub_formula, 'exists')

    def __eq__(self, other):
        if not isinstance(other, Exists):
            return False
        return self.variable == other.variable and self.sub_formula == other.sub_formula

    
    def substitute(self, x, term):
        if x == self.variable:
            return self
        elif term == self.variable:
            new_variable = new_var()
            return Exists(new_variable, self.sub_formula.substitute(self.variable, new_variable).substitute(x, term))
        else:
            return Exists(self.variable, self.sub_formula.substitute(x, term))
        
        

class Not(Formula):

    def __init__(self, sub_formula):

        super(Formula, self).__init__()
        self.sub_formula = sub_formula
        
    def __str__(self):
    
        return '~' + str(self.sub_formula)

    def __eq__(self, other):
        if not isinstance(other, Not):
            return False
        return other.sub_formula == self.sub_formula

    def free_vars(self):
        return free_vars(self.sub_formula)
    
    def substitute(self, x, term):
        return Not(substitute(self.sub_formula, x, term))
        

class TrueClass(Formula):
    
    def __init__(self):
        
        super(TrueClass, self).__init__()

    def __str__(self):
    
        return 'true'
    
    def __eq__(self, other):
        if isinstance(other, TrueClass):
            return True
        return False

    def free_vars(self):
        return []
    
    def substitute(self, x, term):
        return self


class FalseClass(Formula):
    
    def __init__(self):
        
        super(FalseClass, self).__init__()

    def __str__(self):
    
        return 'false'

    def __eq__(self, other):
        if isinstance(other, FalseClass):
            return True
        return False

    def free_vars(self):
        return []
        
    def substitute(self, x, term):
        return self


class Predicate(Formula):
    
    def __init__(self, symbol, arguments):
        
        super(Predicate, self).__init__()
        self.symbol = symbol
        self.arguments = arguments

    def __str__(self):
        
        if len(self.arguments) == 0:
            return self.symbol

        return self.symbol + '(' + ", ".join([str(arg) for arg in self.arguments])  + ')'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return all([op1 == op2 for op1, op2 in zip(self.arguments, other.arguments)]
                 ) and self.symbol == other.symbol and len(self.arguments) == len(other.arguments)
            
        return False

    def free_vars(self):
        return self.arguments
    
    def substitute(self, x, term):
        return Predicate(self.symbol, map(lambda arg: arg.substitute(x, term), self.arguments))

class Term(object):
    
    def __init__(self):
        pass
        
    def __str__(self):
        pass
    
    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not self == other
    
    def substitute(self, x, term):
        pass


class FunctionTerm(Term):
    
    def __init__(self, symbol, arguments):
        
        super(Term, self).__init__()
        self.symbol = symbol
        self.arguments = arguments

    def __str__(self):
        
        if len(self.arguments) == 0:
            return self.symbol

        return self.symbol + '(' + ", ".join([str(arg) for arg in self.arguments])  + ')'

    def __eq__(self, other):
        if isinstance(other, FunctionTerm):
            return all([op1 == op2 for op1, op2 in zip(self.arguments, other.arguments)]
                 ) and self.symbol == other.symbol and len(self.arguments) == len(other.arguments)
            
    
    def substitute(self, x, term):
        return FunctionTerm(self.symbol, map(lambda arg: arg.substitute(x, term), self.arguments))


class Variable(Term):
    
    def __init__(self, name):
        
        super(Term, self).__init__()
        self.name = name

    def __str__(self):
        
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def substitute(self, x, term):
        return self if x != self else term
        


def new_var():
    return Variable('X_new')



