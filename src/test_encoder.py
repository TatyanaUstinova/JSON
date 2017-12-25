import unittest
import json

import encoder


class EncoderTestCase(unittest.TestCase):

    JSON = [
        [],
        [[],    [], [[],  [[[], [], [[[]]]]]]],
        [None],
        [[True], [[[None]]], [False]],
        [[False, None],  10, 2.0, True],
        ["python"],
        [["python 3.6", 5], True, "SQL"],
        {1: 'a'},
        (),
        {1: ('a',)},
        {1.0: 'a'},
        {True: 'a'},
        {None: 'a'},
        {"a": {"b": [1, 2, "python", True]}, "c": 3},
        {
            "a": {
                "b": [1, -2, False, None, True, [], ["python"]],
                'c': 9
            },
            "d": -3,
            "e": [True, False, [[5, [[9, 7]]]]],
            "f": "-10", True: 8,
            5: [2e+7, -2e7]
        },
        10,
        "python",
        None,
        True,
    ]

    INCORRECT_JSON = [
        {7},
    ]

    def test_dumps(self):

        for string in EncoderTestCase.JSON:
            try:
                res = encoder.dumps(string)
            except:
                print(string)
                raise
            self.assertEqual(res, json.dumps(string), msg=string)

        for string in EncoderTestCase.INCORRECT_JSON:
            with self.assertRaises(TypeError, msg=string):
                encoder.dumps(string)


if __name__ == '__main__':
    unittest.main()
