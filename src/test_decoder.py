import unittest
import json

import decoder


class DecoderTestCase(unittest.TestCase):

    JSON = [
        '[]',
        '[[]]',
        '[[], []]',
        '[[[]], []]',
        '[[], [[[]]], []]',
        '  [  [ ],    [], [ [],  [  ] ]]',
        '  [[], [], [[], [[[], [], [[[]]]], []]]]',
        '  [  [ ],    [], [ [],  [ [[], [], [[[]]]  ] ] ]]',
        '[null]',
        '[[], [[[null]]]]',
        '[[], [[[null]]], []]',
        '[true]',
        '[false]',
        '[[true], [[[null]]], [false]]',
        '[true, true, [], false]',
        '[1]',
        '[10]',
        '[1.0]',
        '[   1, 2, 3]',
        '[   10, 2.0, 3]',
        '[   10, 2.0, true]',
        '[ [false, null],  10, 2.0, true]',
        '["python"]',
        '["python", "SQL"]',
        '[["python", 5], true, "SQL"]',
        '["python 3", "SQL"]',
        '[   ["python 3.6", 5], true, "SQL"]',
        '[  ".", 13, ["python 3.6", 5], true, 7.05, "SQL"]',
        '  [ " ,", null, 1,[["."]], 13, [[], [[["["]], 9]], ["python 3.6", 5], true, 7.05, "SQL"]',
        '  [ " ,", \t null, 1,[["."]], 13, [false, [], \r[[["["]], 9]], \n["python 3.6", 5], true, 7.05, "SQL"]',
        '{}',
        '{"a": 1}',
        '{"a": 1, "b": 2, "c": 3}',
        '{"a": [1]}',
        '{"a": [1, 2]}',
        '{"a": [1, 2, [3]]}',
        '{"a": [1, 2, [3], 4]}',
        '{"a": [1, 2, [3, {"b": 5}], 4]}',
        '{"a": {"b": 1}}',
        '{"a": {"b": [1, 2, true]}, "c": 3}',
        '{"a": {"b": [1, -2, null]}, "c": -3, "d": [true, false], "e": "-10"}',
        '{"a": {"b": [1, -2, -1.8e7]}, "c": [3e-5, -3e-5, -3e+5], "d": [2e+7, 2e7], "e": "-10"}',
        '"python"',
        '73'
    ]

    INCORRECT_JSON = [
        '[[[]] []]',
        ',[[[]], []]',
        '][[[]], []]',
        '[[[,]], []]',
        '[[[]] []],',
        '{"a": {"b"]: [1, 2, true]}, "c": 3}',
        '{"a": {"b": [1, 2, truetrue]}, "c": 3}',
        '{"a": {"b""d": [1, 2, true]}, "c": 3}',
        '{"a": {"b",: [1, 2, true]}, "c": 3}',
        ':',
    ]

    def test_loads(self):

        for string in DecoderTestCase.JSON:
            try:
                res = decoder.loads(string)
            except:
                print(string)
                raise
            self.assertEqual(res, json.loads(string), msg=string)

        for string in DecoderTestCase.INCORRECT_JSON:
            with self.assertRaises(decoder.UnexpectedToken, msg=string):
                decoder.loads(string)


if __name__ == '__main__':
    unittest.main()
