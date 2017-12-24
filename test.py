import unittest

from eval_int import eval_int
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
            print("Test ", test[e])
            with self.subTest(e=e):
                self.assertEqual(str(eval_int(parse(test[e][0]))), str(test[e][1]))


if __name__ == '__main__':
    unittest.main()
