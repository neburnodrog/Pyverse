from unittest import TestCase
from silabizador.silabizador import Word


class TestWordVowelBlockSeparator(TestCase):
    def test_vowel_block_separator(self):
        self.assertEqual(Word.vowel_block_separator("nstru"), "ns-tru")


class TestVowelSeparator(TestCase):
    def test_vowel_separator1(self):
        self.assertEqual(Word.vowel_separator("ue"), "ue")

    def test_vowel_separator2(self):
        self.assertEqual(Word.vowel_separator("aí"), "a-í")

    def test_vowel_separator3(self):
        self.assertEqual(Word.vowel_separator("ahí"), "a-hí")
