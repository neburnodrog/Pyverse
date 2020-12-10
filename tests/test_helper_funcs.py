import unittest
from silabizador.helper_funcs import *


class TestCounter(unittest.TestCase):
    def test_counter1(self):
        self.assertEqual(counter("-La -muer-te es-ta-ba -mur-mu-ran-do-me -bien", 1), 12)

    def test_counter2(self):
        self.assertEqual(counter("asdf---her--g        e-e-r2-3-4-f--g-", 13), 26)


class TestLastWordFinder(unittest.TestCase):
    def test_last_word1(self):
        self.assertEqual(last_word_finder("Hermoso el jardín de los águilas"), "águilas")

    def test_last_word2(self):
        self.assertEqual(last_word_finder("vamos a dárselo a Miguel"), "miguel")

    def test_last_word3(self):
        self.assertEqual(last_word_finder("La angustia me da,    ,-migrañas"), "migrañas")


if __name__ == "__main__":
    unittest.main()
