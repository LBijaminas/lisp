###
### Defined exception handling classes
###

class IncorrectNumberParamsException(Exception):
    # My defined exception to be raised if the number of parameters given
    # does not match up with the number of params needed
    def __init__(self, name, num_received, num_needed):
        self._name = name
        self._num_r = num_received
        self._num_n = num_needed
    def __str__(self):
        return repr(self._name)
    
    def printError(self):
        print "The function \"" + self._name + "\" received " + str(self._num_r) + " parameters while it needed " + str(self._num_n)
        
    def getNumReceived(self):
        return self._num_r

class UnmatchedParenException(Exception):
    # Will be raised when the number of the parenthesis is not matched
    
    def printError(self):
        print "The parenthesis are unmatched in the given input"
        
class NotAFunctionException(Exception):
    # Will be raised when the first param after the parenthesis is not a function
    
    def __init__(self, value):
        self._value = value
        
    def printError(self):
        print "The first parameters after the parenthesis is not a function: " + str(self._value)
        
class WrongParameterTypeException(Exception):
    # Will be raised when the type of the parameter passed is not the type of
    # the parameter expected
    
    def __init__(self, name, expected_type):
        self._name = name
        self._expected = expected_type
        
    def printError(self):
        print "The expected parameter type is " + self._expected + " at a function: " + self._name

class DivisionByZeroException(Exception):
    
    def printError(self):
        print "Division by 0 not allowed."
       
        
'''
    Helper class that will hold all random helper functions
'''
class Helper(object):
    
    '''
        Checks whether the parameter is a floating point number
        
        @param num: parameter to be checked
    '''
    @staticmethod
    def isFloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    
    '''
        Checks whether the parameter is numeric
        
        @param num: is to be checked
    '''
    @staticmethod
    def isNumeric(num):
        return isinstance(num, int) or Helper.isFloat(num)
    
    '''
        Processes the QUOTEd string for CAR or CDR
        
        @param substr: the string to be processed
        @param func_name: function name
    '''
    @staticmethod
    def processString(substr, func_name):
        open_lvl = closed_lvl = 0
        for i in range(len(substr)):
            if substr[i] == "(":
                open_lvl+=1
            elif substr[i] == ")":
                closed_lvl+=1
            
            if open_lvl == closed_lvl:
                if func_name == "CAR":
                    return substr[:i]
                elif func_name == "CDR":
                    return substr[i+2:]
    '''
        Returns the count of the elements at the top most level
        
        @param substr: is the string for which to check the count
    '''
    @staticmethod
    def getCount(substr):
        open_lvl = closed_lvl = count = 0
        
        # first_time is a special var to handle when there is only one element in the array
        first_time = True
        for i in range(len(substr)):
            if substr[i] == "(":
                open_lvl+=1
            elif substr[i] == ")":
                closed_lvl+=1
            
            if open_lvl == closed_lvl:
                if first_time or substr[i] == " ":
                    first_time = False
                    count +=1
                
        return count
    
