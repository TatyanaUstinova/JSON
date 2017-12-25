# JSON
JSON encoder &amp; decoder representation

You can use these loads &amp; dumps functions in the usual way.
 
Example:

    >>> source = '{"a": {"b": [1, -2, -1.8e7]}, "c": [3e-5, -3e-5, -3e+5], "d": [2e+7, 2e7], "e": "-10"}'
    >>> result = loads(source)
    >>> print(result)
    
    {'a': {'b': [1, -2, -18000000.0]}, 'c': [3e-05, -3e-05, -300000.0], 'd': [20000000.0, 20000000.0], 'e': '-10'}


    >>> source = {
        "a": {
            "b": [1, -2, False, None, True, [], ["python"]],
            'c': 9
        },
        "d": -3,
        "e": [True, False, [[5, [[9, 7]]]]],
        "f": "-10", True: 8,
        5: [2e+7, -2e7]
    }
    >>> result = dumps(source)
    >>> print(result)
    
    {"a": {"b": [1, -2, false, null, true, [], ["python"]], "c": 9}, "d": -3, "e": [true, false, [[5, [[9, 7]]]]], "f": "-10", "true": 8, "5": [20000000.0, -20000000.0]}
