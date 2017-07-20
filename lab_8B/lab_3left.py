"""6.009 Lab 8B: carlae Interpreter"""

import sys


class Environment:
    """
    Creates an environment object.
    
    self._parent: parent environment object of that environment
    self._bindings: the variables stored in the environment
    """
    def __init__(self, parent, bindings={}):
        self._parent = parent
        self._bindings = bindings

    # declares a new variable in the environment
    def define(self, name, arg):
        self._bindings[name] = arg

    # resets a binding in the environment
    def set(self, name, arg):
        if name in self._bindings:
            self.define(name, arg)
            return
        if self._parent is None:
            raise EvaluationError("an error occurred")
        return self._parent.set(name, arg)

    # finds item recursively in the environment, raises error if not found
    def find(self, item):
        if item in self._bindings:
            return self._bindings[item]
        if self._parent is None:
            raise EvaluationError("an error occurred")
        return self._parent.find(item)


class Function:
    """
    A user-defined function: ie. a function not defined in carlae_builtins
    
    self.params: The parameters of the function
    self.expression: The expression to be evaluated
    self.env: The environment in which the function belongs/will be evaluated in
    """
    def __init__(self, params, expression, env):
        self.params = params
        self.expression = expression
        self.env = env

    # evaluates function
    def evaluate(self, variables):
        new_env = Environment(self.env)
        for p in range(len(self.params)):
            new_env.define(self.params[p], variables[p])
        return evaluate(self.expression, new_env)


class EvaluationError(Exception):
    """Exception to be raised if there is an error during evaluation."""
    pass


class LinkedList:
    """
    Forms a single cell of a linked list.
    
    self.elt: the element at the specific index in the linked list
    self.next: pointer to the next LinkedList object in the chain
    """
    def __init__(self, elt='', next=None):
        self.elt = elt
        self.next = next

    # finds the element at a certain index recursively
    def ind(self, index):
        next_link = self.next
        if next_link is None and index > 0:
            raise EvaluationError
        if index == 0:
            return self.elt
        return next_link.ind(index - 1)

    # length of the chain
    def length(self, count=0):
        if self.next is None and self.elt == '':
            return count
        if self.next is None:
            return count+1
        return self.next.length(count+1)

    # returns all elts as a list
    def all_elts(node):
        nodelist = []
        while node:
            if node.elt != '':
                nodelist.append(node.elt),
            node = node.next
        return nodelist

    # string representation of the list
    def __str__(self):
        return str(self.all_elts())


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
                      
    >>> tokenize("(define (x 2) (* x x))")
    ['(', 'define', '(', 'x', '2', ')', '(', '*', 'x', 'x', ')', ')']
    """
    tokens = []
    temp = ''
    comment = False
    com = ''
    for letter in source:
        if comment:
            com = com + letter
            if '\n' in com:
                comment = False
                com = ''
        elif letter.isspace():
            if len(temp) > 0:
                tokens.append(temp)
                temp = ''
        elif letter is '(' or letter is ')':
            if len(temp) > 0:
                tokens.append(temp)
                temp = ''
            tokens.append(letter)
        elif letter is ';':
            comment = True
        else:
            temp = temp + letter
    if len(temp) > 0:
        tokens.append(temp)
    return tokens


# parses number from string
def num(s):
    """
    Parses number from a str
    :param s: str representation of a number
    :return: number
    """
    try:
        return int(s)
    except ValueError:
        return float(s)


# checks if number
def is_number(s):
    """
    Checks if a str contains a number
    :param s: str to check
    :return: True if number, False otherwise
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
        
    (define circle-area (lambda (r) (* 3.14 (* r r))))
    >>> parse(['(', 'define', 'circle-area', '(', 'lambda', '(', 'r', ')', '(', '*', '3.14', '(', '*', 'r', 'r', ')', ')', ')', ')'])
    ['define', 'circle-area', ['lambda', ['r'], ['*', 3.14, ['*', 'r', 'r']]]]
    """

    def check_valid(tokens):
        open = 0
        close = 0
        for t in tokens:
            if t == "(":
                open+=1
            if t == ')':
                close+=1
        if open == close:
            return True
        return False

    def build_list(tokens):
        if tokens[0] == ')':
            raise SyntaxError

        if tokens[0] == '(':
            out = []
            tokens.pop(0)
            try:
                while tokens[0] != ')':
                    out.append(build_list(tokens))
                    tokens.pop(0)
            except IndexError:
                raise SyntaxError

            return out

        if is_number(tokens[0]):
            return num(tokens[0])

        if isinstance(tokens[0], str):
            return tokens[0]

    if check_valid(tokens):
        ans = build_list(tokens)
        return ans
    raise SyntaxError


# product
def prod(iterable):
    """
    Carlae builtins product operation
    :param iterable: list of parameters
    :return: product of all elts in the list
    """
    p = 1
    for n in iterable:
        p *= n
    return p


# division
def div(iterable):
    """
    Carlae builtins division operation
    :param iterable: list of parameters
    :return: division of all elts in the list
    """
    p = float(iterable[0])
    for n in iterable[1:]:
        p /= n
    return p


# evaluate file
def evaluate_file(file_path, env=None):
    """
    Evaluates the contents of the file and returns the outcome
    :param file_path: str name of the file
    :param env: environment for the file to be evaluated in
    :return: evaluated expression
    """
    with open(file_path) as f:
        mylist = f.read().splitlines()
    single = []
    for i in mylist:
        single += i
    tokens = tokenize(single)
    parsed = parse(tokens)
    return evaluate(parsed, env)


def linked_list(iterable):
    """
    Recursively constructs a linked list
    :param iterable: list of elements to include in the linked list
    :return: linked list
    """
    if len(iterable) == 0:
        return LinkedList()
    if len(iterable) == 1:
        return LinkedList(iterable.pop(0))
    return LinkedList(iterable.pop(0), linked_list(iterable))


# filters a list
def list_filter(l, func):
    """
    Filters a list according to a boolean expression
    
    :param l: list to be filtered
    :param func: boolean expression
    :return: list with elements not meeting the boolean condition removed
    """
    all_elts = l.all_elts()
    filtered = []
    for e in all_elts:
        if func.evaluate([e]) == '#t':
            filtered.append(e)
    return linked_list(filtered)


# maps a list
def map(func, l):
    """
    Applies a function to all elts in a list
    
    :param func: function to apply to the list
    :param l: linked list of values
    :return: new mapped linked list
    """
    all_elts = l.all_elts()
    mapped = []
    for e in all_elts:
        if l.elt != '':
            if isinstance(func, Function):
                mapped.append(func.evaluate([e]))
            else:
                mapped.append(func([e]))
    return linked_list(mapped)


# reduces a list
def reduce(func, l, initval):
    """
    Reduces a list according to the function passed
    :param func: function to apply to list
    :param l: linked list to evaluate
    :param initval: initial value of the reduction
    :return: an int solution
    """
    all_elts = l.all_elts()
    if isinstance(func, Function):
        temp_elt = func.evaluate([initval, all_elts.pop(0)])
        while all_elts:
            temp_elt = func.evaluate([temp_elt, all_elts.pop(0)])
    else:
        temp_elt = func([initval, all_elts.pop(0)])
        while all_elts:
            temp_elt = func([temp_elt, all_elts.pop(0)])
    return temp_elt

carlae_builtins = {
    # takes in input as a list
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': lambda args: args[0] if len(args) == 1 else prod(args),
    '/': lambda args: args[0] if len(args) == 1 else div(args),
    '=?': lambda args: '#t' if all(earlier == later for earlier, later in zip(args, args[1:])) else '#f',
    '>': lambda args: '#t' if all(earlier > later for earlier, later in zip(args, args[1:])) else '#f',
    '>=': lambda args: '#t' if all(earlier >= later for earlier, later in zip(args, args[1:])) else '#f',
    '<': lambda args: '#t' if all(earlier < later for earlier, later in zip(args, args[1:])) else '#f',
    '<=': lambda args: '#t' if all(earlier <= later for earlier, later in zip(args, args[1:])) else '#f',
    'list': lambda args: linked_list(args),
    '#t': True,
    '#f': False
}


def result_and_env(tree, env=None):
    """
    Returns the evaluated expression and the environment in a tuple.
    :param tree: parsed expression to be evaluated
    :param env: environment to evaluate in
    :return: product of evaluation and environment in a tuple
    """

    if env is None:
        # empty environment
        par = Environment(None, carlae_builtins)
        env = Environment(par, {})

    return evaluate(tree, env), env


def evaluate(tree, env=None):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """

    # no tree
    if tree == []:
        raise EvaluationError

    # resets env if none passed
    if env is None:
        par = Environment(None, carlae_builtins)
        env = Environment(par, {})

    # number
    if type(tree) is float or type(tree) is int:
        return tree

    # list
    if isinstance(tree, list):
        op = tree[0]
        # first element is not a function
        if type(op) is int:
            raise EvaluationError

        # if operator
        if op == 'if':
            comb = tree[1][0]
            true = tree[2]
            false = tree[3]

            # comparator
            if comb in carlae_builtins:
                bool = evaluate(tree[1], env)
                if bool == '#t':
                    return evaluate(true, env)
                elif bool == '#f':
                    return evaluate(false, env)
            # and
            elif comb == 'and':
                for exp in tree[1][1:]:
                    if evaluate(exp, env) == '#f':
                        return evaluate(false, env)
                return evaluate(true, env)
            # or
            elif comb == 'or':
                for exp in tree[1][1:]:
                    if evaluate(exp, env) == '#t':
                        return evaluate(true, env)
                return evaluate(false, env)
            # not
            elif comb == 'not':
                bool = evaluate(tree[1][1], env)
                if bool == '#t':
                    return evaluate(false, env)
                elif bool == '#f':
                    return evaluate(true, env)

        # define function
        if op == 'define':
            name = tree[1]
            # s expression - easier function definitions
            if isinstance(name, list):
                name = name[0]
                params = tree[1][1:]
                exp = tree[2]
                value = Function(params, exp, env)

            # traditional function definitions
            else:
                value = evaluate(tree[2], env)
            env.define(name, value)
            return value

        # lambda
        elif op == 'lambda':
            return Function(tree[1], tree[2], env)

        # concatenate
        elif op == 'concat':
            if len(tree) == 1:
                return LinkedList()
            original = evaluate(tree[1], env).all_elts()
            for l in tree[2:]:
                original += evaluate(l, env).all_elts()
            return linked_list(original)

        # elt-at-index
        elif op == 'elt-at-index':
            l = evaluate(tree[1], env)
            if l.length() == 0:
                raise EvaluationError
            return l.ind(tree[2])

        # first list element
        elif op == 'car':
            if evaluate(tree[1], env).elt == '':
                raise EvaluationError
            return evaluate(tree[1], env).elt

        # list except for first element
        elif op == 'cdr':
            if evaluate(tree[1], env).next is None:
                raise EvaluationError
            return evaluate(tree[1], env).next

        # length
        elif op == 'length':
            return evaluate(tree[1]).length()

        # map
        elif op == 'map':
            l = evaluate(tree[2], env)
            func = evaluate(tree[1], env)
            return map(func, l)

        # filter
        elif op == 'filter':
            l = evaluate(tree[2], env)
            func = evaluate(tree[1], env)
            return list_filter(l, func)

        # reduce
        elif op == 'reduce':
            func = evaluate(tree[1], env)
            l = evaluate(tree[2], env)
            initval = evaluate(tree[3], env)
            return reduce(func, l, initval)

        # begin
        elif op == 'begin':
            for t in tree[1:-1]:
                evaluate(t, env)
            return evaluate(tree[-1], env)

        # let
        elif op == 'let':
            env2 = Environment(env)
            for v in tree[1]:
                arg = evaluate(v[1], env)
                env2.define(v[0], arg)
            return evaluate(tree[2], env2)

        # set!
        elif op == 'set!':
            name = tree[1]
            exp = evaluate(tree[2], env)
            env.set(name, exp)
            return exp

        # carlae built-in function
        elif op is type(str) and op in carlae_builtins:
            func = tree[0]
            out = [evaluate(x, env) for x in tree[1:]]
            return carlae_builtins[func](out)

    # variable lookup
    if type(tree) is str:
        return env.find(tree)

    # list - function evaluation
    if isinstance(tree, list):
        func = evaluate(tree[0], env)
        if isinstance(func, Function):
            return func.evaluate([evaluate(x, env) for x in tree[1:]])

        new_list = [evaluate(x, env) for x in tree[1:]]
        return func(new_list)


if __name__ == '__main__':
    par = Environment(None, carlae_builtins)
    env = Environment(par, {})

    file_list = sys.argv[1:]
    for f in file_list:
        evaluate_file(f, env)

    command = input("in> ")
    while command != "QUIT":
        try:
            tokens = tokenize(command)
            expression = parse(tokens)
            evaluated, env = result_and_env(expression, env)
            print("out> " + str(evaluated))
            command = input("in> ")
        except SyntaxError:
            print("Error")
            command = input("in> ")