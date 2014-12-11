import interpreter

class Interface():
    
    prompt = 'lisp> '
    intro = '''Lukas\'s LISP interpreter
        For help in how to use it, type in help
    '''
    
    '''
        Sets up the environment prior to starting the interpreter
    '''
    def __init__(self):
        self._environment = interpreter.Environment()
        print self.intro
    
    '''
        Basically just calls the parser on the input
    '''
    def _callParser(self, input):
        try:
            var = interpreter.Parser(input) # parse
            var.parse()
            
            for statement in var.getStatements():
                print interpreter.Interpreter.interpret(statement, self._environment)
        except Exception, e:
            try:
                print e
                e.printError()
            except Exception, w:
                print "Unknown error. Please check your input"
    '''
        Displays help message
    '''
    def _help(self):
        print '''
        The way the interpreter works is that it interprets the input and outputs it onto the next line. It also can read
        the input from a file.
        
        Options:
        
        help             displays this menu
        load filename    loads the file in the folder, from which to execute the function
        exit             exits the interpreter
        
        '''
        
    '''
        Read the provided file and read it into the string 
    '''
    def _load(self, file):
        try:
            with open (file, "r") as myfile:
                    data = myfile.read().replace('\n', '')
            self._callParser(data)
        except:
            print "Wrong file name. Please try again."
            
    '''
        Takes the input from the user and handles it
    '''
    def loop(self):
        while True:
            # take input in
            input = raw_input(self.prompt)
            
            if input.lower() == "exit": # exit program
                print "Exiting..."
                break
            elif input.lower() == "help":
                self._help()
            elif input.split()[0] == "load": # load the file
                self._load(input.split()[1])
                continue
            
            self._callParser(input)