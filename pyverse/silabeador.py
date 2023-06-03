import re
from typing import List, Dict
from pyverse.sentence import Sentence
from pyverse.vars import *
from nlt import numlet as nl
from pyverse.word import Word


class Pyverse:
    def __init__(self, verse: str):
        self.original_verse = verse

        if not isinstance(verse, str):
            raise ValueError("Pyverse can only handle strings.")
        if re.search(r"\d", verse):
            self.verse_text = self.numbers_to_words(verse)
        else:
            self.verse_text = self.original_verse

        self.sentence: Sentence = Sentence(self.verse_text)
        self.word_list: List[Word] = self.sentence.word_objects
        self.last_word: Word = self.word_list[-1]
        self.syllables = self.sentence.syllabified_sentence
        self.synalephas = self.sentence.synalephas
        self.count = self.counter()
        self.consonant_rhyme = self.verse_consonant_rhyme_finder()
        self.assonant_rhyme = self.verse_assonant_rhyme_finder()
        self.type_of_verse = self.type_verse()

    def __repr__(self):
        sentence = self.sentence.syllabified_sentence

        if len(sentence) > 50:
            try:
                cut_index = sentence.index(" ", 50)
                sentence = sentence[:cut_index] + " [...]"
            except ValueError:
                pass

        return "<Verse: '{}', Syllables: {}>".format(
            sentence,
            self.count,
        )

    def counter(self) -> int:
        """Counts the number of syllables:

        1. if the last word is oxytone we add 1 syllable to the verse meter.
        2. if it is paroxytone (the most common case in spanish) we leave it as it is.
        3. if it is proparoxytone we sustract 1 syllable from the counting.

        """

        if len(self.word_list) == 1 and str.count(self.syllables, '-') == 1:
            return 1

        verse_final_accent = self.last_word.accentuation

        if (
            self.last_word.word_text in atonic_monosyll
            and self.word_list[-2].word_untrimmed + " " + self.last_word.word_untrimmed
            in self.sentence.synalephas
        ):
            verse_final_accent = 2

        syllable_addition = 2 - verse_final_accent

        return self.sentence.syllabified_sentence.count("-") + syllable_addition

    def type_verse(self) -> Dict[str, bool]:
        sentence = self.original_verse
        type_of_verse = {}
        first_letter = sentence.strip(punctuation)[0]

        if first_letter == first_letter.upper():
            type_of_verse["is_beg"] = True
        else:
            type_of_verse["is_beg"] = False

        if sentence.endswith(".") and not sentence.endswith("..."):
            type_of_verse["is_end"] = True
        else:
            type_of_verse["is_end"] = False

        if not type_of_verse["is_beg"] and not type_of_verse["is_end"]:
            type_of_verse["is_int"] = True
        else:
            type_of_verse["is_int"] = False

        return type_of_verse

    def verse_consonant_rhyme_finder(self) -> str:
        return self.last_word.consonant_rhyme

    def verse_assonant_rhyme_finder(self) -> str:
        return "".join([letter for letter in self.consonant_rhyme if letter in vowels])

    @staticmethod
    def numbers_to_words(verse: str) -> str:
        words = verse.split()
        new_words = []
        for word in words:
            word_stripped = word.strip(punctuation)
            if word_stripped.isalpha():
                new_words.append(word)

            elif word_stripped.isdigit():
                number_to_letters = nl.Numero(word).a_letras.lower()
                new_word = word.replace(word_stripped, number_to_letters)
                new_words.append(new_word)

            else:
                raise ValueError("Invalid mixture of letters and digits")

        return " ".join(new_words)
