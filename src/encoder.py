def check_key(element):
    if element is None:
        return '"null"'
    elif element is True:
        return '"true"'
    elif element is False:
        return '"false"'
    elif isinstance(element, (str, int, float)):
        return '"{}"'.format(element)
    else:
        raise TypeError('{} key of incorrect type {}'.format(element, type(element)))


def check_value(element):
    if element is None:
        return 'null'
    elif element is True:
        return 'true'
    elif element is False:
        return 'false'
    if isinstance(element, (int, float)):
        return str(element)
    elif isinstance(element, str):
        return '"{}"'.format(element)
    else:
        raise TypeError('{} element of incorrect type {}'.format(element, type(element)))


def dumps(container):

    separator = ', '

    if isinstance(container, (list, tuple)):
        json_str = '['

        first = True
        for element in container:

            if first:
                first = False
            else:
                json_str += separator

            if isinstance(element, (list, tuple, dict)):
                json_str += dumps(element)
            else:
                json_str += check_value(element)

        json_str += ']'

    elif isinstance(container, dict):
        json_str = '{'

        first = True
        for key, value in container.items():

            if first:
                first = False
            else:
                json_str += separator

            json_str += check_key(key)
            json_str += ': '

            if isinstance(value, (list, tuple, dict)):
                json_str += dumps(value)
            else:
                json_str += check_value(value)

        json_str += '}'

    else:
        json_str = check_value(container)

    return json_str


if __name__ == '__main__':
    import json

    source = {
        "a": {
            "b": [1, -2, False, None, True, [], ["python"]],
            'c': 9
        },
        "d": -3,
        "e": [True, False, [[5, [[9, 7]]]]],
        "f": "-10", True: 8,
        5: [2e+7, -2e7]
    }

    expected = json.dumps(source)
    print(expected)

    result = dumps(source)
    print(result)

    assert result == expected
