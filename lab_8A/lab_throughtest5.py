"""6.009 Lab 8A: carlae Interpreter"""

import sys

class Environment:
    def __init__(self, parent, bindings={}):
        self.parent = parent
        self.bindings = bindings

    def define(self, name, arg):
        self.bindings[name] = arg

    def find(self, item):
        if item in self.bindings:
            return self.bindings[item]
        if self.parent is None:
            raise EvaluationError("an error occurred")
        return self.parent.find(item)


class Function:
    def __init__(self, params, expression, env):
        self.params = params
        self.expression = expression
        self.env = env

    def get_params(self):
        return self.params

    def get_expression(self):
        return self.expression

    def get_env(self):
        return self.env

    def evaluate(self, variables):
        params = self.get_params()
        expression = self.get_expression()
        new_env = Environment(self.get_env)
        for p in range(len(params)):
            new_env.define(params[p], variables[p])
        return evaluate(expression, new_env)


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
    if type(tree) is float or type(tree) is int:
        return tree

    if env is None:
        par = Environment(None, carlae_builtins)
        env = Environment(par, {})

    if tree[0] in env.bindings:
        return env.bindings[tree[0]]

    if type(tree) is str:
        return env.find(tree)

    if isinstance(tree, list):

        if tree[0] == 'define':
            name = tree[1]
            if isinstance(tree[2], list):
                # create new function according to the tree's body
                # set function as value in the environment
                # evaluate the new function in the environment
                arg = evaluate(tree[2], env)
                env.define(name, arg)
                return env.bindings[name]
            else:
                env.set(name, tree[2])
            # name = tree[1]

        if tree[0] == 'lambda':
            return Function(tree[1], tree[2], env)

        if tree[0] in carlae_builtins:
            func = tree[0]
            out = []
            for t in tree[1:]:
                out.append(evaluate(t, env))
            return carlae_builtins[func](out)

        # compound expression
        return Function(evaluate(tree[0], env), tree[1:], env)

        # if tree[0] in carlae_builtins:
        #     func = tree[0]
        #     out = []
        #     for t in tree[1:]:
        #         out.append(ev(t, env))
        #     return carlae_builtins[func](out)
        #
        # if type(tree[0]) is str:
        #     func = env.find(tree[0])
        #     if isinstance(func, Function):
        #         return func.evaluate(tree[1:])
        #     return func(tree[1:])


if __name__ == '__main__':
    command = input("in> ")
    while command != "QUIT":
        try:
            tokens = tokenize(command)
            expression = parse(tokens)
            evaluated = evaluate(expression)
            print("out> " + str(evaluated))
            command = input("in> ")
        except SyntaxError:
            print("Error")
            command = input("in> ")