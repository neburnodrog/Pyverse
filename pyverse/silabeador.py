import re
from typing import List, Dict
from pyverse.errors import PyverseError
from pyverse.sentence import Sentence
from pyverse.vars import atonic_monosyll, punctuation
from nlt import numlet as nl
from pyverse.word import Word


class Pyverse:
    def __init__(self, verse: str):
        self.original_verse = verse

        if not isinstance(verse, str):
            raise PyverseError(
                "Pyverse reads a verse from a string. "
                f"Got: {type(verse).__name__}."
            )
        if re.search(r"\d", verse):
            self.verse_text = self.numbers_to_words(verse)
        else:
            self.verse_text = self.original_verse

        self.sentence: Sentence = Sentence(self.verse_text)
        self.word_list: List[Word] = self.sentence.word_objects
        self.last_word_index: int = self.last_word_with_letters()
        self.last_word: Word = self.word_list[self.last_word_index]
        self.syllables = self.sentence.syllabified_sentence
        self.synalephas = self.sentence.synalephas
        self.count = self.counter()
        self.consonant_rhyme = self.last_word.rhyme.consonant
        self.consonant_rhyme_yeismo = self.last_word.rhyme.consonant_yeismo
        self.assonant_rhyme = self.last_word.rhyme.assonant
        self.assonant_rhyme_strict = self.last_word.rhyme.assonant_strict
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

    def last_word_with_letters(self) -> int:
        """The verse rhymes on its last word, which is the last token holding
        letters: the dash of 'la luna, —' is punctuation, not a word."""

        for index in reversed(range(len(self.word_list))):
            if self.word_list[index].syllable_count:
                return index

        raise PyverseError(
            f"{self.original_verse!r} holds no word to read: a verse needs "
            "at least one letter."
        )

    def counter(self) -> int:
        """Counts the number of syllables:

        1. if the last word is oxytone we add 1 syllable to the verse meter.
        2. if it is paroxytone (the most common case in spanish) we leave it as it is.
        3. if it is proparoxytone we sustract 1 syllable from the counting.

        """

        words = [word for word in self.word_list if word.syllable_count]

        if len(words) == 1 and self.last_word.syllable_count == 1:
            return 1

        verse_final_accent = self.last_word.accentuation

        if (
            self.last_word.word_text in atonic_monosyll
            and self.last_word_index in self.sentence.synalepha_positions
        ):
            verse_final_accent = 2

        syllable_addition = 2 - verse_final_accent
        syllables = sum(word.syllable_count for word in words)

        return syllables - len(self.sentence.synalepha_positions) + syllable_addition

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
                raise PyverseError(
                    f"{word!r} mixes letters and digits, so Pyverse cannot "
                    "tell how it is read."
                )

        return " ".join(new_words)
