import abc


class Token(object):
    __metaclass__ = abc.ABCMeta

    COMPLETENESS = False

    def __init__(self, previous):
        self.previous = previous
        self.name = self.__class__.__name__

    @abc.abstractmethod
    def process(self):
        pass

    def append(self, symbol):
        return True


class OpenBracket(Token):

    next_tokens = {'OpenBracket', 'CloseBracket', 'OpenBrace', 'NoneToken', 'TrueToken', 'FalseToken',
                                'StringToken', 'NumberToken'}

    def __init__(self, previous):
        super().__init__(previous)

    def __str__(self):
        return "'['"

    def process(self):
        pass


class CloseBracket(Token):

    next_tokens = {'CloseBracket', 'CloseBrace', 'Comma'}

    def __init__(self, previous):
        super().__init__(previous)

    def __str__(self):
        return "']'"

    def process(self):
        pass


class OpenBrace(Token):

    next_tokens = {'CloseBrace', 'NoneToken', 'TrueToken', 'FalseToken', 'StringToken', 'NumberToken'}

    def __init__(self, previous):
        super().__init__(previous)

    def __str__(self):
        return "'{'"

    def process(self):
        pass


class CloseBrace(Token):

    next_tokens = {'CloseBracket', 'CloseBrace', 'Comma'}

    def __init__(self, previous):
        super().__init__(previous)

    def __str__(self):
        return "'}'"

    def process(self):
        pass


class Colon(Token):

    next_tokens = {'OpenBracket', 'OpenBrace', 'NoneToken', 'TrueToken', 'FalseToken', 'StringToken', 'NumberToken'}

    def __init__(self, previous):
        super().__init__(previous)

    def __str__(self):
        return "':'"

    def process(self):
        pass


class Comma(Token):

    next_tokens = {'OpenBracket', 'OpenBrace', 'NoneToken', 'TrueToken', 'FalseToken', 'StringToken', 'NumberToken'}

    def __init__(self, previous):
        super().__init__(previous)

    def __str__(self):
        return "','"

    def process(self):
        pass


class ValueToken(Token):
    __metaclass__ = abc.ABCMeta

    COMPLETENESS = True

    VALID = ''
    VALUE = None
    MESSAGE = ''

    next_tokens = {'CloseBracket', 'CloseBrace', 'Colon', 'Comma'}

    def __init__(self, previous, value):
        super().__init__(previous)
        self.value = value

    def __str__(self):
        return '{}'.format(type(self.value))

    def append(self, symbol):
        """
        Returns True if value ready.
        :param symbol: the symbol to append
        :return:
        """
        self.value += symbol

        if self.value == self.VALID:
            self.value = self.VALUE
            return True
        elif self.value in self.VALID:
            return False
        else:
            raise ValueError(self.MESSAGE)


class NoneToken(ValueToken):
    VALID = 'null'
    VALUE = None
    MESSAGE = 'Incorrect NoneType value'

    def __init__(self, previous):
        super().__init__(previous, 'n')

    def process(self):
        pass


class TrueToken(ValueToken):
    VALID = 'true'
    VALUE = True
    MESSAGE = 'Incorrect bool value'

    def __init__(self, previous):
        super().__init__(previous, 't')

    def process(self):
        pass


class FalseToken(ValueToken):
    VALID = 'false'
    VALUE = False
    MESSAGE = 'Incorrect bool value'

    def __init__(self, previous):
        super().__init__(previous, 'f')

    def process(self):
        pass


class StringToken(ValueToken):

    def __init__(self, previous):
        super().__init__(previous, '')

    def append(self, symbol):
        """
        Returns True if value ready.
        :param symbol: the symbol to append
        :return:
        """
        if symbol != '"':
            self.value += symbol
            return False
        else:
            return True

    def process(self):
        pass


class NumberToken(ValueToken):

    COMPLETENESS = False
    SIGN = ('-', '+')

    def __init__(self, previous, digit):
        if not (digit.isdigit() or digit in NumberToken.SIGN):
            raise ValueError(digit)
        super().__init__(previous, digit)

        self.cast = int

    def append(self, symbol):
        """
        Returns True if value ready.
        :param symbol: the symbol to append
        :return:
        """
        if symbol in ('.', 'e', 'E'):
            self.cast = float
        elif not (symbol.isdigit() or symbol in NumberToken.SIGN):
            self.value = self.cast(self.value)
            return True

        self.value += symbol
        return False

    def process(self):
        pass


class UnexpectedToken(Exception):
    pass


def tokenizer(stream):

    tokens = {
        '[': OpenBracket,
        ']': CloseBracket,
        '{': OpenBrace,
        '}': CloseBrace,
        ':': Colon,
        ',': Comma,
        'n': NoneToken,
        't': TrueToken,
        'f': FalseToken,
        '"': StringToken,
    }

    ignored = [' ', '\n', '\t', '\r']

    previous = None
    token = None
    symbol = None
    for symbol in stream:

        if token:

            if token.append(symbol):
                yield token
                if token.COMPLETENESS:
                    token = None
                    continue
                token = None
            else:
                continue

        if symbol in ignored:
            continue

        # token initialization

        if symbol.isdigit() or symbol in ('-', '+'):
            token = NumberToken(previous, symbol)
        elif symbol in tokens:
            token = tokens[symbol](previous)
        else:
            raise ValueError('Unexpected symbol', symbol)

        previous = token

    if isinstance(token, NumberToken) and token.append(','):
        yield token
    elif symbol and token.append(symbol):
        yield token


def parse(tokens, token=None):

    first = token or tokens.__next__()
    if first.name == 'OpenBracket':
        container = []
    elif first.name == 'OpenBrace':
        container = {}
    elif isinstance(first, ValueToken):
        return first.value
    else:
        raise UnexpectedToken(first)

    key = None

    for token in tokens:

        if token.name not in token.previous.next_tokens:
            raise UnexpectedToken('{} doesn\'t support {} as next'.format(token.previous, token))

        if token.name in ('OpenBracket', 'OpenBrace'):
            if isinstance(container, list):
                container.append(parse(tokens, token))
            elif isinstance(container, dict):
                if not key:
                    raise UnexpectedToken(token)
                container[key] = parse(tokens, token)
                key = None

        elif token.name == 'CloseBracket':
            return container

        elif token.name == 'CloseBrace':
            return container

        elif token.name == 'Colon' and isinstance(container, list):
            raise UnexpectedToken('list doesn\'t support {} inside'.format(token))

        elif token.name == 'Comma':
            pass

        elif isinstance(token, ValueToken):
            if isinstance(container, list):
                container.append(token.value)
            elif isinstance(container, dict):
                if not key:
                    key = token.value
                    continue
                value = token.value

                if token.name in ('OpenBracket', 'OpenBrace'):
                    value = parse(tokens, value)
                container[key] = value
                key = None


def loads(source):

    tokens = tokenizer(iter(source))

    result = parse(tokens)
    return result


if __name__ == '__main__':
    import json

    source = '{"a": {"b": [1, -2, -1.8e7]}, "c": [3e-5, -3e-5, -3e+5], "d": [2e+7, 2e7], "e": "-10"}'

    expected = json.loads(source)
    print(expected)

    result = loads(source)
    print(result)

    assert result == expected
