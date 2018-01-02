import unittest

from eval_global import ext_eval_global
from parse import parse


class TestInt(unittest.TestCase):
    def test_integers(self):
        test = [("1", "1"),
                ("(1)", "1"),
                ("1 - 2", "-1"),
                ("4 / 2 * 3", "6"),
                ("4 * 2 / 3", "2"),
                ("1 + 2 * 3", "7"),
                ("(1 + 2) * 3", "9"),
                ("-1 + -1 + (-1 - -1)", "-2"),
                ("-1 + -1 - (-1 - -1)", "-2"),
                ("(-1 + -1 - (-1 - -1))", "-2"),
                ("((-1 + -1 - (-1 - -1)))", "-2"),
                ("((1+(2*3))*(4*5))", "140"),
                ("(4+6)-5*9", "-35")]

        for e in range(len(test)):
            with self.subTest(e=e):
                self.assertEqual(str(ext_eval_global(test[e][0])), str(test[e][1]))


class TestBool(unittest.TestCase):
    def test_comparison(self):
        test = [("true", "true"),
                ("(false)", "false"),
                ("true == true", "true"),
                ("true == false", "false"),
                ("4/2 == 1+1", "true"),
                ]

        for e in range(len(test)):
            with self.subTest(e=e):
                self.assertEqual(str(ext_eval_global(test[e][0])), str(test[e][1]))


if __name__ == '__main__':
    unittest.main()
