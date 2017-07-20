"""6.009 Lab 8A: carlae Interpreter"""

import sys

class Environment:
    def __init__(self, parent, bindings={}):
        self._parent = parent
        self._bindings = bindings

    def define(self, name, arg):
        self._bindings[name] = arg

    def find(self, item):
        if item in self._bindings:
            return self._bindings[item]
        if self._parent is None:
            raise EvaluationError("an error occurred")
        return self._parent.find(item)


class Function:
    def __init__(self, params, expression, env):
        self.params = params
        self.expression = expression
        self.env = env

    def evaluate(self, variables):
        new_env = Environment(self.env)
        for p in range(len(self.params)):
            new_env.define(self.params[p], variables[p])
        return evaluate(self.expression, new_env)


class EvaluationError(Exception):
    """Exception to be raised if there is an error during evaluation."""
    pass


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
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


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def is_number(s):
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
    Tokenized: ['(', 'define', 'circle-area', '(', 'lambda', '(', 'r', ')', '(', '*', '3.14', '(', '*', 'r', 'r', ')', ')', ')', ')']
    Parsed: ['define', 'circle-area', ['lambda', ['r'], ['*', 3.14, ['*', 'r', 'r']]]]
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


def prod(iterable):
    p = 1
    for n in iterable:
        p *= n
    return p


def div(iterable):
    p = float(iterable[0])
    for n in iterable[1:]:
        p /= n
    return p


carlae_builtins = {
    # takes in input as a list
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': lambda args: args[0] if len(args) == 1 else prod(args),
    '/': lambda args: args[0] if len(args) == 1 else div(args)
}


def result_and_env(tree, env=None):
    par = Environment(None, carlae_builtins)
    if env is None:
        # Empty environment
        env = Environment(par, {})

    return evaluate(tree, env), env

# Errors here
def evaluate(tree, env=None):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    # if tree != 0 and not tree:
    #     raise EvaluationError
    #print("tree ", tree)
    #print("env ", env._bindings)
    if env is None:
        par = Environment(None, carlae_builtins)
        env = Environment(par, {})

    if type(tree) is float or type(tree) is int:
        return tree

    if isinstance(tree, list):
        op = tree[0]
        if op == 'define':
            name = tree[1]
            # s expression
            if isinstance(name, list):
                name = name[0]
                params = tree[1][1:]
                exp = tree[2]
                value = Function(params, exp, env)
            else:
                value = evaluate(tree[2], env)
            env.define(name, value)
            return value

        elif op == 'lambda':
            return Function(tree[1], tree[2], env)

        elif op is type(str) and op in carlae_builtins:
            func = tree[0]
            out = []
            for t in tree[1:]:
                out.append(evaluate(t, env))
            return carlae_builtins[func](out)

    if type(tree) is str:
        #print("find ", env.find(tree))
        return env.find(tree)

    if isinstance(tree, list):
        func = evaluate(tree[0], env)
        if isinstance(func, Function):
            #print("entered if")
            # if isinstance(tree[1], list):
            #     # need to evaluate second argument
            #     params = [evaluate(tree[1], env)]
            #     return func.evaluate(params)
            # else:
            return func.evaluate([evaluate(x, env) for x in tree[1:]])

        #print(env._bindings)
        new_list = [evaluate(x, env) for x in tree[1:]]
        #print(new_list)
        return func(new_list)


if __name__ == '__main__':
    env = None
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