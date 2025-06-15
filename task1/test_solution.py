import unittest
from task1.solution import strict


class TestFirstTask(unittest.TestCase):
    """Тест декоратора из первого задания."""

    def test_on_correct_types(self):
        @strict
        def multiply_three(a: int, b: int, c: int):
            return a * b * c

        self.assertEqual(multiply_three(1, 2, 3), 6)
        self.assertEqual(multiply_three(2, -3, 4), -24)
        self.assertEqual(multiply_three(0, 25678, 33654), 0)

    def test_on_incorrect_types(self):
        @strict
        def concat_strings(a: str, b: str, c: str ='abcde'):
            return a + b + c

        with self.assertRaises(TypeError):
            concat_strings([1, 2], 123)
            concat_strings('abc', 'def', (123, 456))
            concat_strings({1: 123, 2: 234}, 12345, (123, 456))


if __name__ == '__main__':
    unittest.main()
