from helpers import *
import re

class FunctionHolder(object):
    _functions = ["QUOTE", "CAR", "CDR", "CONS", "SET", "PLUS", "MINUS", "MULT", "DIV", "LENGTH", "LIST",
                  "AND", "OR", "NOT", "ATOMP", "LISTP", "EQUALP", "COND", "DEFUN", "PROG", "+", "-", "/", "*"]
    
    def __init__(self, input = None, env = None, _name = None):
        if input:
            self._name = Interpreter.getFirstElementVal(input).upper()
            self._params = input[1:]
        elif _name:
            self._name = _name.upper()
        self._env = env

        
    '''
        Says what the name does - if the function exists
        
        @param name: the name of the function to be checked
    '''
    @staticmethod
    def checkIfExists(name):
        try:
            return True if name.upper() in FunctionHolder._functions else False
        except:
            return False
    
    
    '''
        Returns a reference to a function to be executed
    '''
    def getFunction(self):
        # nested function is the only way I could simulate an anonymous function
        # behavior. Lambdas could've worked but it wouldn't work for more complicated
        # functions
        
        ####
        ####
        #### Defined below will be all of the LISP's functions
        ####
        ####
        
        '''
            All functions have appropriate try/catch statements to handle that the
            functions are given correct parameters
        '''
        def _plus(params):
            # gets called when PLUS or + is called
            sum = 0
            
            for item in params:
                if not Helper.isNumeric(item):
                    raise WrongParameterTypeException("PLUS", "number")
                sum += item
                
            return sum
        
        def _minus(params):
            # gets called when MINUS or - is called
            
            if not Helper.isNumeric(params[0]):
                raise WrongParameterTypeException("MINUS", "number")
            
            try:
                sum = params[0]
            except:
                raise IncorrectNumberParamsException("MINUS", 0, 1)
            
            for i in range(1, len(params)):
                if not Helper.isNumeric(params[i]):
                    raise WrongParameterTypeException("MINUS", "number")
                sum -= params[i]
                
            return sum
        
        def _mult(params):
            # gets called when MULT or * is called
            sum = 1
            
            for item in params:
                if not Helper.isNumeric(item):
                    raise WrongParameterTypeException("MULT", "number")
                sum *= item
                
            return sum
        
        def _div(params):
            # gets called when DIV or / is called
            try:
                sum = params[0]
            except:
                raise IncorrectNumberParamsException("DIV", 0, 1)
            
            if not Helper.isNumeric(params[0]):
                raise WrongParameterTypeException("DIV", "number")
            
            for i in range(1, len(params)):
                if not Helper.isNumeric(params[i]):
                    raise WrongParameterTypeException("DIV", "number")
                if params[i] == 0:
                    raise DivisionByZeroException
                
                sum /= params[i]
                
            return sum
        
        def _quote(params):
            # let's make sure params only has one variable
            try:
                params[1]
            except:
                # only 1 param passed
                try:
                    str = params[0]
                    
                    try:
                        length = len(re.findall(r'(["\'])((?:(?!\1)[^\\]|(?:\\\\)*\\[^\\])*)\1', str))
                    except:
                        length = 0
                        
                    if Helper.isNumeric(str) or not Atom.isNil(_listp(str)):
                        # its a list or a single numeric value. safe to return
                        return str
                    elif length > 1:
                        # the parameter is a string and there are more than one params passed
                        raise IncorrectNumberParamsException("QUOTE", length, 1)
                    elif length == 1:
                        # there is one string passed at least
                        # basically can start with ' or ", so let's find which it starts with
                        dbl_quote = True
                        l_quote = str.find('"')
                        
                        if l_quote == -1: 
                            l_quote = str.find("'")
                            dbl_quote = False
                            
                        r_quote = str.rfind('"') if dbl_quote else str.rfind("'")

                        # so at this point we have the indices of the beginning and the end of the string
                        # let's getVar a right-most and left-most space chars
                        
                        l_space = str.find(" ")
                        r_space = str.rfind(" ")
                        
                        if l_space == -1:
                            # no spaces, it's a one-word string
                            return str
                        
                        if l_space == r_space:
                            # we only have one space
                            if l_space > l_quote and r_quote > l_space:
                                # the space is inside of the string. condition satisfied
                                return str
                            else:
                                # two params passed
                                raise IncorrectNumberParamsException("QUOTE", 2, 1)
                        else:
                            # more than one space
                            if not ((l_space > l_quote and r_quote > l_space) and (r_space > l_quote and r_quote > r_space)):
                                # left-most space or right-most space (or both) is outside of the parens
                                raise IncorrectNumberParamsException("QUOTE", "more than 1", 1)
                            else:
                                # both of the spaces are inside of the parens
                                return str
                    elif str.find(" ") != -1:
                        # there are no strings and no lists, but there is a space - too many params
                        raise IncorrectNumberParamsException("QUOTE", len(str.split()), 1)
                    else:
                        # param is a variable. just return it
                        return str
                except IncorrectNumberParamsException, e:
                    # the exception came from _listp, which means the quoted 
                    # stuff is not a list, but its not an atom either
                    raise IncorrectNumberParamsException("QUOTE", e.getNumReceived(), 1)
                except:
                    # no params given
                    raise IncorrectNumberParamsException("QUOTE", 0, 1)
            else:
                # params[1] succeeds
                raise IncorrectNumberParamsException("QUOTE", len(params), 1)
            
        def _car(params):
            # let's make sure params only has one variable
            try:
                params[1]
            except:
                # only 1 param passed
                try:
                    str = params[0]
                except:
                    raise IncorrectNumberParamsException("CAR", 0, 1)  
                
                if Atom.isNil(str):
                    return Atom.getAtom("nil")()
                
                # checks if the param is a list
                if Atom.isNil(_listp(params)):
                        raise WrongParameterTypeException("CAR", "list") 
                
                if str[1] == "(":
                    # process the list
                    return Helper.processString(str[1:], "CAR") + ")"
                else:
                    return str[1:].split()[0]
            
            else:
                # params[1] succeeds
                raise IncorrectNumberParamsException("CAR", len(params), 1)
        
        def _cdr(params):
            # let's make sure params only has one variable
            try:
                params[1]
            except:
                # only 1 param passed
                try:
                    str = params[0]
                except:
                    raise IncorrectNumberParamsException("CDR", 0, 1)               
                
                if Atom.isNil(str):
                    return Atom.getAtom("nil")()
                
                # checks if the param is a list
                if Atom.isNil(_listp(params)):
                        raise WrongParameterTypeException("CDR", "list")
                
             
                if str[1] == "(":
                    # process the list
                    return "(" + Helper.processString(str[1:], "CDR")
                else:
                    return "(" + " ".join(str.split()[1:])
            
            else:
                # params[1] succeeds
                raise IncorrectNumberParamsException("CDR", len(params), 1)
            
        def _cons(params):
            # let's make sure params only has two variables
            try:
                params[2]
            except:
                # only 1 param passed
                try:
                    p1 = params[0]
                    p2 = params[1]
                except:
                    raise IncorrectNumberParamsException("CONS", len(params), 2)              
                
                # params have to be values. that means they cannot be unnamed variables
                if p1 is None:
                    raise WrongParameterTypeException("CONS", "Atom")
                elif p2 is None:
                    raise WrongParameterTypeException("CONS", "atom or list")
                
                try:
                    p2.index(" ")
                except:
                    # second param not a list. special handling needed
                    # according my lisp interpreter, the result should be:
                    # (p1 . p2)

                    return "(" + str(p1) + ((" . " + str(p2)) if not Atom.isNil(str(p2)) else "") + ")" 
                else:
                    # second param is a list, we can handle a generic case
                    return "(" + str(p1) + " " + p2[1:len(p2) - 1] + ")"
            
            else:
                # params[2] succeeds
                raise IncorrectNumberParamsException("CONS", len(params), 1)
        
        def _set(params):
            # let's make sure params only has two variables
            try:
                params[2]
            except:
                try:
                    var = params[0]
                    val = params[1]
                except:
                    # 0 or 1 var passed
                    raise IncorrectNumberParamsException("SET", len(params), 1)
                else:
                    
                    # we have to check to make sure that the variable has only allowed chars
                    if Atom.checkIfAtomVar(var):
                        self._env.setParam(var, val)
                        return val
                    else:
                        raise WrongParameterTypeException("SET", "ATOM")
            else:
                # params[2] succeeds
                raise IncorrectNumberParamsException("SET", len(params), 1)
        
        def _list(params):
            # let's make sure params only has one variable
            try:
                p = params[0]
            except:
                # no params passed
                return Atom.getAtom("nil")
            else:
                try:
                    p = params[1]
                except:
                    # only 1 param passed
                    return "(" + p + ")"
                else:
                    # n params passed
                    p = "("
                    for item in params:
                        p += str(item) + " "
                        
                    return p.strip() + ")"
        
        def _length(params):
            # let's make sure params only has one variable
            try:
                params[1]
            except:
                # only 1 param passed
                try:
                    str = params[0]
                except:
                    raise IncorrectNumberParamsException("LENGTH", 0, 1)               
                
                if Atom.isNil(str):
                    return Atom.getAtom("nil")()
                
                # checks if the param is a list
                if Atom.isNil(_listp(params)):
                        raise WrongParameterTypeException("LENGTH", "list")
                
                
                if str[1:].find("(") != -1:
                    # process the list
                    return Helper.getCount(str[1:])
                else:
                    return len(str.split())
            
            else:
                # params[1] succeeds
                raise IncorrectNumberParamsException("LENGTH", len(params), 1)
        
        def _and(params):
            if len(params) > 0:
                for item in params:
                    if Atom.isNil(item) or Atom.isFalse(item):
                        return Atom.getAtom("nil")()
                # if the expression is true, CLISP interpreter returns the last item
                return params[len(params) - 1] 
            
            # by default, CLISP interpreter returns t
            return Atom.getAtom("t")
        
        def _or(params):
            for item in params:
                if not (Atom.isNil(item) or Atom.isFalse(item)):
                    # i was thinking of returning "t", but the way CLISP interpreter does it is return the first 
                    # true element
                    return item
            return Atom.getAtom("nil")()
        
        def _not(params):
            # let's make sure params only has one variable
            try:
                params[1]
            except:
                try:
                    if Atom.isNil(params[0]) or Atom.isFalse(params[0]):
                        return Atom.getAtom("t")()
                    else:
                        return Atom.getAtom("nil")()
                except:
                    raise IncorrectNumberParamsException("NOT", 0, 1)
            else:
                # params[1] succeeds
                raise IncorrectNumberParamsException("NOT", len(params), 1)
        
        def _atomp(params):
            # let's make sure params only has one variable
            try:
                params[1]
            except:
                try:
                    if Helper.isNumeric(params[0]):
                        return Atom.getAtom("t")()
                    else:
                        # basically utilizes _listp function to determine whether its a list or not and reverse the decision
                        # however, nil is both atom and list, so handler it separately
                        return (Atom.getAtom("t")() if Atom.isNil(_listp(params)) else Atom.getAtom("nil")()) if not Atom.isNil(params[0]) else Atom.getAtom("t")()
                except:
                    raise IncorrectNumberParamsException("ATOMP", 0, 1)
            else:
                # params[1] succeeds
                raise IncorrectNumberParamsException("ATOMP", len(params), 1)
        
        def _listp(params):
            # let's make sure params only has one variable
            try:
                # trivial check is needed for it to work properly
                
                if type(params) is str:
                    raise Exception
                else:
                    params[1]
            except:
                # only 1 param passed
                try:
                    if Helper.isNumeric(params[0]):
                        return Atom.getAtom("nil")()
                    else:
                        return Atom.getAtom("t")() if (Atom.isNil(params[0]) or params[0][0] == "(") else Atom.getAtom("nil")()
                except:
                    raise IncorrectNumberParamsException("LISTP", 0, 1)
            else:
                # params[1] succeeds
                raise IncorrectNumberParamsException("LISTP", len(params), 1)
        
        def _equalp(params):
            try:
                params[2]
            except:
                try:
                    p1 = params[0]
                    p2 = params[1]
                except:
                    raise IncorrectNumberParamsException("EQUALP", len(params), 2)
                else:
                    # we will have two cases: a list and not
                    
                    # first, let's make sure that they are either both lists or not
                    if Atom.isNil(_listp([p1])) and Atom.isNil(_listp([p2])):
                        # both are non-lists
                        
                        ##    Possible scenarios:
                        ##    both are numerics - type doest matter - compare
                        ##    both are strings - case insensitive, compare
                        ##    both are Atoms - compare
                        #    nil != f
                        
                        if Helper.isNumeric(p1) and Helper.isNumeric(p2):
                            #both numbers
                            return Atom.getAtom("t")() if p1 == p2 else Atom.getAtom("nil")()
                        elif Atom.checkIfAtom(p1) and Atom.checkIfAtom(p2):
                            return Atom.getAtom("t")() if Atom.getAtom(p1)() == Atom.getAtom(p2)() else Atom.getAtom("nil")()
                        elif p1.lower() == p2.lower():
                            return Atom.getAtom("t")()
                        else:
                            return Atom.getAtom("nil")()
                    elif not (Atom.isNil(_listp([p1])) or Atom.isNil(_listp([p2]))):
                        # both are lists
                        
                        # let's split both into elements
                        # it doesnt matter if the strings are split, as they can be compared by elements
                        # within itself as well, so it will work
                        p1_array = p1.replace("(","").replace(")", "").split()
                        p2_array = p2.replace("(","").replace(")", "").split()
                        
                        if len(p1_array) != len(p2_array):
                            # lengths don't match, lists are clearly not the same
                            return Atom.getAtom("nil")()
                        
                        for i in range(len(p1_array)):
                            item1 = p1_array[i]
                            item2 = p2_array[i]
                            if Helper.isNumeric(item1) and Helper.isNumeric(item2):
                                # both items are numerics, can compare
                                if float(item1) != float(item2):
                                    return Atom.getAtom("nil")()
                            elif Helper.isNumeric(item1) or Helper.isNumeric(item2):
                                # only one of them is numeric, not equal
                                return Atom.getAtom("nil")()
                            elif Atom.checkIfAtom(item1) and Atom.checkIfAtom(item2):
                                # both are atoms
                                if Atom.getAtom(item1) != Atom.getAtom(item2):
                                    return Atom.getAtom("nil")()
                            elif Atom.checkIfAtom(item1) or Atom.checkIfAtom(item2):
                                # only one atom
                                return Atom.getAtom("nil")()
                            else:
                                # string
                                if item1.lower() != item2.lower():
                                    return Atom.getAtom("nil")()
                        return Atom.getAtom("t")()
                    else:
                        # types don't match - definitely not equal
                        return Atom.getAtom("nil")()
            else:
                raise IncorrectNumberParamsException("EQUALP", len(params), 2)
        
        def _cond(params):
            try:
                params[0]
            except:
                # no params, just return nil
                return Atom.getAtom("nil")()
            else:
                # at least one param passed
                for item in params:
                    # the param must be a list.
                    # interestingly in CLISP interpreter, the type checking is done one at a time, 
                    # so thats what kind of approach I will take
                    if not isinstance(item, list): 
                        raise WrongParameterTypeException("COND", "LIST")
                    
                    if not Atom.isNil(item[0]):
                        return item[len(item) - 1]
        
        def _defun(params):
            ###
            ### We have a separate mini-parser to parse through the params
            ###
            def _parseFunctions(params, results = []):
                try:
                    char = params.pop(0)
                except:
                    return results.pop()
                    
                if char == "(":
                    results.append(_parseFunctions(params, []))
                    
                    return _parseFunctions(params, results)
                elif char == ")":
                    return results
                else:
                    # append to the formal params list
                    results.append(char)
                    
                    return _parseFunctions(params, results)
            
            # not the best way but it should 
            parsedInput = Parser.tokenize(params[0])
            
            formalParams = []
            # first param must an atomVar
            if Atom.checkIfAtomVar(parsedInput[0]):
                # define function name
                func_name = parsedInput.pop(0)
            else:
                raise WrongParameterTypeException("DEFUN", "ATOM")
            
            # the second params must be a list
            if parsedInput.pop(0) != "(":
                # not a list
                raise WrongParameterTypeException("DEFUN", "LIST")
            else:
                while True:
                    try:
                        char = parsedInput.pop(0)
                    except:
                        # there is no closing parenthesis - error
                        raise WrongParameterTypeException("DEFUN", "LIST")
                    
                    if char == ")":
                        break
                    else:
                        # append to the formal params list
                        formalParams.append(char)
                        
            #func_body = parsedInput
            #self._env.createFunction(func_name, formalParams, _parseFunctions(func_body))            
            self._env.createFunction(func_name, formalParams, parsedInput) 
            return func_name
        # returns the appropriate function based on func call
        
        def _prog(params):
            
            # has no params - cant happen
            if len(params) == 0:
                raise IncorrectNumberParamsException('PROG', 0, "1+")
            
            ###
            ### There is not much to do in this function, as the interpreter already automatically evaluates all the statements
            ### so all we have to do is just return the result of the last statement
            ###
            
            return params[len(params) - 1]
            
        '''    
            Selector to decide which function to select
        '''           
        def _compareFunction():
            if self._name == "PLUS" or self._name == "+":
                return _plus
            elif self._name == "MINUS" or self._name == "-":
                return _minus
            elif self._name == "MULT" or self._name == "*":
                return _mult
            elif self._name == "DIV" or self._name == "/":
                return _div
            elif self._name == "QUOTE":
                return _quote
            elif self._name == "CAR":
                return _car
            elif self._name == "CDR":
                return _cdr
            elif self._name == "CONS":
                return _cons
            elif self._name == "SET":
                return _set
            elif self._name == "LENGTH":
                return _length
            elif self._name == "LIST":
                return _list
            elif self._name == "AND":
                return _and
            elif self._name == "OR":
                return _or
            elif self._name == "NOT":
                return _not
            elif self._name == "ATOMP":
                return _atomp
            elif self._name == "LISTP":
                return _listp
            elif self._name == "EQUALP":
                return _equalp
            elif self._name == "COND":
                return _cond
            elif self._name == "DEFUN":
                return _defun
            elif self._name == "PROG":
                return _prog
            else:
                try:
                    return self._env.getFunction(self._name)
                except:
                    raise NotAFunctionException(self._name)
            
        return _compareFunction()
        
class Interpreter(object):
    
    '''
        This function gets the value of the first element of the list, to be used for the comparison whether it is a function
        or not. If the element throws exception, it means it is not a function - move on
        
        @param input: the input of which first elem to return
    '''
    @staticmethod
    def getFirstElementVal(input):
        try:
            return input[0]['value']
        except Exception, e:
            return False
    
    '''
        The function gets the level for the depth of recursion, in case there are nested levels of recursion
        
        @deprecated: don't really use this function
    '''
    @staticmethod
    def getDepthList(input):
        try:
            input[0]['value']
            return input
        except Exception, e:
            return Interpreter.getDepthList(input[0])
    
    '''
        The function interprets the input
        
        @param input: the input to be interpreted
        @param env: the environment instance
    '''
    @staticmethod
    def interpret(input, env):
        # first time around, just initialize the environment
        if isinstance(input, list): #if is array, interpret it
            return Interpreter.interpretArray(input, env)
        elif input['type'] == "id": # getVar variable's value
            return env.getVar(input['value'])
        else: #literal          
            return input['value']

    '''
        Interprets the list
        
        @param input: the list to be interpreted
        @param env: the environment instance
    '''
    @staticmethod
    def interpretArray(input, env):
        if len(input) > 0 and (FunctionHolder.checkIfExists(Interpreter.getFirstElementVal(input)) or env.checkIfFunction(Interpreter.getFirstElementVal(input))):
            # evaluate function
            func = FunctionHolder(input, env)

            array = map(lambda x: Interpreter.interpret(x, env), input[1:])
            
            return func.getFunction()(array)
        else:
            # empty array means just ()
            if len(input) == 0:
                return "nil"
            
            ###
            ###
            ### SPECIAL CASE! Can only happen with COND or (), because
            ### COND allows the lists not to have a function as a first param
            ###
            ###
            
            # recursively go through each of the functions and put the interpreted
            # values into the array
            array = map(lambda x: Interpreter.interpret(x, env), input) 
           
            return array
  
class Parser(object):
    
    def __init__(self, input):
        self._input = input
        
        # parenthesis count will be used to determine whether the parenthesis match
        self._parenCount = 0 
        
        # will significe at which level of the paren count qoute appeared
        self._quoteParen = self._condParen = 0
        
        # QUOTE flag is off by default. if it's on, that means that we're not evaluating and just
        # QUOTING the element and using it as a string
        
        # COND flag is used when we have cond, because the first param for cond lists dont have to be
        # necessarily functions
        self._quoteFlag = self._condFlag =  False
         
        # QUOTE holder is to hold the quoted string temporarily
        self._quoteHolder = ""
        
        # Used for quoting to determine whether the param is a list or not
        self._isList = False
        
        
        ###
        ###
        ### NEED TO IMPLEMENT THE COUNT FOR THE PARENTHESIS!!!
        ###
        ###
        self._statements = []
    

    '''
        Tokenizes the input strings into tokens
    '''
    def _tokenize(self):
        # make sure that the characters all have at least one space in between
        # so it would be easy to split the input into an array
        str = self._input.replace("(", " ( ")
        str = str.replace(")", " ) ").strip()
        
        return str.split()
    
    '''
        A static tokenizer for the DEFUN
    '''
    @staticmethod
    def tokenize(input):
        parser = Parser(input)
        return parser._tokenize()
    
    '''
        Splits the input array into the two categories: literal or id
        
        @param input is the token to be tested against given categories
        @param isFirst is used to determined whether it is the first param of the input. 
                if isFirst is setParam, the char must be a function; otherwise - raise an exception
    '''
    def _splitCategory(self, input, isFirst = False):
        if input.isdigit() and (not isFirst or self._condFlag):
            return {"type": "literal", "value": int(input)}
        elif Helper.isFloat(input) and (not isFirst or self._condFlag):
            return {"type": "literal", "value": float(input)}
        elif self._quoteFlag:
            return {"type" : "quote", "value" : input}
        elif input[0] == '"' and input[-1] == '"' and (not isFirst or self._condFlag):
            return {"type" : "literal", "value": input[1:-1]}
        elif Atom.checkIfAtom(input) and (not isFirst or self._condFlag):
            return {"type" : "literal", "value" : input}
        elif isFirst and (input.isdigit() or Helper.isFloat(input) or (input[0] == '"' and input[-1] == '"')):
            raise NotAFunctionException(input)
        else:
            # basically an ID is either a variable or a function.
            # there is no need to separate it as the checks for them
            # occur separately and it wouldn't intersect
            return {"type" : "id", "value": input}
    
    '''
        Splits the items into levels of recursion, as according to the levels
        of parenthesis that it is in
        
        @param input is the tokenized input array/stack. In reality, it is an array, but it is treated as a 
                stack through pop/append functions
        @param list is the array in which the given level of recursion is stored
        @param isFirst is used to determined whether it is the first param of the input. 
                if isFirst is setParam, the char must be a function; otherwise - raise an exception
                
    '''
    def _splitParen(self, input, list = None, isFirst = False):
        if list is None:
            # Python considers [] passed to be None. Let's fix that
            list = []
    
        # let's getVar the first char of the array
        try:
            char = input.pop(0) # always pop the first char
        except:
            #array is finished
            
            # need to check if the statements array is empty because
            # if not checked, it wouldn't work for scalars
            
            try:
                elem = list.pop() # getVar the last element from the array
            except:
                # if the program gets here, that means that the list is empty
                # when the pop is called. The only way that can occur is if 
                # an unmatched opening parenthesis is called
                raise UnmatchedParenException
            if len(self._statements) == 0:
                self._statements.append(elem)
                
            
            return elem
        
        
        if self._quoteFlag:
            # We're quoting. No need to evaluate
            
            # variable to determine whether a space after a char is needed
            nospace = False
            if char == "(":
                self._parenCount += 1
                
                # again, to maintain Lisp-like string style
                nospace = True
                self._isList = True

            elif char == ")":
                self._parenCount -= 1

                # need to strip again, to maintain the Lisp-like style
                self._quoteHolder = self._quoteHolder.rstrip()
                
                # let's reset COND flag, once cond level closes
                if self._condParen == self._parenCount:
                    self._condFlag = False
                    
                if self._parenCount == 0:
                    self._statements.append(list)
                    
            if self._parenCount == self._quoteParen:
                # QUOTE done

                # evaluation of the quote is done - let's append it to the list
                list.append(self._splitCategory(self._quoteHolder.replace("()", "nil")))
                
                # reset the quote flag as well as the quote holder
                self._quoteHolder = ""
                self._quoteFlag = False
                self._isList = False
                
                return list
            else:
                self._quoteHolder += char + (" " if not nospace else "") #shortcut to handle whether the space is needed or not
                return self._splitParen(input, list)
            
            
        if char == "(":
            self._parenCount += 1
            
            # enter another level of recursion
            list.append(self._splitParen(input, isFirst = True))
            
            return self._splitParen(input, list)
        
        elif char == ")":
            self._parenCount -= 1
            if self._parenCount == 0:
                self._statements.append(list)
                
            # done with this level of recursion
            return list
        else:
            # any literal or function need to be assigned their category
            list.append(self._splitCategory(char, isFirst))
            
            if char.upper() == "QUOTE" or char.upper() == "DEFUN":
                # QUOTE needs special handling when parsing
                # DEFUN is here because everything I will getVar into DEFUN,
                # I will take as a string from there on and perform all
                # the checking at the interpretation level
            
                # previous level of recursion is what called QUOTE.
                # let's make note of that
                self._quoteParen = self._parenCount - 1
                self._quoteFlag = True
                
            elif char.upper() == "COND":
                # COND needs special handling, similar like QUOTE
                self._condParen = self._parenCount - 1
                self._condFlag = True
            
            
            return self._splitParen(input, list)
    
    '''
        Calls the appropriate functions to parse the input
    '''
    def parse(self):
        input = self._tokenize()
        parsedArray = self._splitParen(input)
        
        if self._parenCount != 0:
            raise UnmatchedParenException
        
        self._parsedInput = parsedArray
    
    '''
        Returns the parsed input
    '''
    def getParsedInput(self):
        return self._parsedInput
    
    '''
        Returns the statement list
    '''
    def getStatements(self):
        return self._statements

class Environment(object):
    
    def __init__(self, scope = None, parent = None, func_table = None):
        # if scope is none, make it an empty list
        self._scope = scope if scope is not None else {}
        self._parent = parent
        self._func_table = func_table if func_table is not None else {}
    
    '''
        Retrieves the variable based on identification
        
        @param id: the identification of the parameter
    '''
    def getVar(self, id):
        try:
            if id.upper() in self._scope:
                return self._scope[id.upper()]
            elif self._parent is not None:
                return self._parent.getVar(id.upper())
        except:
            return False
    
    '''
        Sets the parameter
        
        @param id: the id to be created or set
        @param new_val: the value to be set
    '''
    def setParam(self, id, new_val):
        self._scope[id.upper()] = new_val
     
    '''
        Creates a function in the function table
        
        @param func_name: function name
        @param formal_params: the list of formal parameters
        @param func_body: function body
    '''   
    def createFunction(self, func_name, formal_params, func_body):
        self._func_table[func_name.upper()] = {'params' : formal_params, 'body' : func_body}
    
    '''
        Checks whether it is a function based on a given name
        
        @param name: the name to be checked
    '''
    def checkIfFunction(self, name):
        if name.upper() in self._func_table:
            return True
        elif self._parent is not None:
            return self._parent.checkIfFuntion(name)
        else:
            return False

    '''
        Returns the instance based on a given function name
        
        @param name: the function name
    '''
    def getFunction(self, name):
        body = self._func_table[name]['body']
        formal_params = self._func_table[name]['params']
        environment = Environment(parent = self)

        
        def _function(actual_params):
        # first of all, the number of params must match, otherwise - error
            if len(formal_params) != len(actual_params):
                raise IncorrectNumberParamsException(name, len(actual_params), len(formal_params))
            
            # secondly, let's assign the parameters
            for i in range(len(formal_params)):
                environment.setParam(formal_params[i], actual_params[i])
            
            # next, let's parse it
            parser = Parser(body)
            parser._splitParen(body)
            
            statement = parser.getStatements()[0]
            return Interpreter.interpret(statement, environment)
                     
        return _function
    
    def printScope(self):
        print self._scope
    
    def printFunctions(self):
        print self._func_table
            
class Atom(object):
    _atoms = ["nil", "t", "f"] 
    
    '''
        Checks whether the item is a nil, true or false
        
        @param item: item to be checked
    '''
    @staticmethod   
    def checkIfAtom(item):
        # the regex matches the string provided in the instructions of what is considered to be an atom
        return True if item.lower() in Atom._atoms else False
    
    '''
        Checks whether the item is a string
        @param item: item to be checked
    '''
    @staticmethod
    def checkIfAtomVar(item):
        # the regex matches the string provided in the instructions of what is considered to be an atom
        return True if len(re.findall(r'^\d*[a-zA-Z_\$][a-zA-Z0-9_\$]*$', item)) > 0 else False
    
    '''
        Checks if the item is nil
        
        @param item: item to be checked
    '''
    @staticmethod
    def isNil(item):
        return True if (not Helper.isNumeric(item)) and (item.lower() == "nil" or item == "()") else False 
    
    '''
        Checks if the item is false
        
        @param item: item to be checked
    '''
    @staticmethod
    def isFalse(item):
        return True if (not Helper.isNumeric(item)) and item.lower() == "f" else False 
    
    '''
        Retrieves the nil, t, or f atoms
        
        @param name: the name of the atom
    '''
    @staticmethod
    def getAtom(name):
        
        def getNil():
            return "nil"
        
        def getFalse():
            return "F"
        
        def getTrue():
            return "T"
        
        if name.lower() == "t":
            return getTrue
        elif name.lower() == "f":
            return getFalse
        elif name.lower() == "nil":
            return getNil