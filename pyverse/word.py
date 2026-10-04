import string
from functools import cached_property
from typing import Union
import re
from pyverse.rhyme import Rhyme, rhyme
from pyverse.syllabification import Syllabification
from pyverse.vars import (
    accented_vowels,
    punctuation,
    strong_vowels,
    unaccented_vowels,
    vowels,
    weak_accented_vowels,
)


class Word:
    def __init__(self, word: str) -> None:
        self.word_untrimmed = word
        self.word_text = self.stripped_word.lower()
        self.syllabification = Syllabification.parse(
            self.as_written(self.syllabify_word()), word
        )
        self.word_syllabified = self.syllabification.render(with_punctuation=False)
        self.syllabified_w_punct = self.syllabification.render()
        self.syllable_count = len(self.syllabification)
        self.accentuation = self.accentuation_finder(self.word_syllabified)

    def __repr__(self):
        return f"<Word: '{self.word_syllabified}'>"

    @property
    def stripped_word(self) -> str:
        _stripped_word = self.word_untrimmed.strip(punctuation + " ")
        return _stripped_word

    def as_written(self, division: str) -> str:
        """The division laid back over the letters as the verse writes them.

        The syllabifier reads lower case throughout, down to the 'h' of 'ch'
        and the 'r' of a 'br' cluster, so it is asked about the lower-cased
        word and answers about it. The verse keeps its capitals.
        """

        letters = list(self.stripped_word)

        if len(letters) != len(division.replace("-", "")):
            #  '.lower()' is not length-preserving for every alphabet
            return division

        return "".join(
            "-" if character == "-" else letters.pop(0) for character in division
        )

    def syllabify_word(self) -> str:
        """Find all vowel groupings in the pre_syllabified_word
        and pass them to diphthong_finder to see if any diphthongs slipped through."""
        syllabified_word = self.pre_syllabify()

        vowel_groupings = re.findall(f"[{vowels}]-h?[{vowels}]+", syllabified_word)
        for hiatus in vowel_groupings:
            diphthong = self.diphthong_finder(hiatus)
            if diphthong:
                syllabified_word = syllabified_word.replace(hiatus, diphthong)

        vowel_groupings_two = re.findall(f"[{vowels}]-h?[{vowels}]+", syllabified_word)
        if vowel_groupings_two:
            for hiatus in vowel_groupings_two:
                diphthong = self.diphthong_finder(hiatus)
                if diphthong:
                    syllabified_word = syllabified_word.replace(hiatus, diphthong)

        vowel_groupings_three = re.findall(f"[h{vowels}]+", syllabified_word)
        longer_than_3 = filter(lambda x: len(x) > 3, vowel_groupings_three)
        for vowel_group in longer_than_3:
            syllabified_word = syllabified_word.replace(
                vowel_group, self.check_if_separation(vowel_group)
            )

        if not syllabified_word.startswith("-"):
            syllabified_word = "-" + syllabified_word

        return syllabified_word

    @staticmethod
    def check_if_separation(vowel_groups_longer_than_3: string):
        result = ''

        for vowel in vowel_groups_longer_than_3:
            if vowel == 'h':
                result += '-h'
            else:
                result += vowel

        return result

    def pre_syllabify(self) -> str:
        """Basic logic of the syllabifier"""

        word = self.word_text

        if len(word) == 1:
            return "-" + word

        block = ""
        _pre_syllabified_word = ""

        for i, letter in enumerate(word):
            block += letter

            if letter in vowels:
                _pre_syllabified_word += self.vowel_block_separator(block)
                block = ""

            elif i == len(word) - 1:
                if block == letter:
                    _pre_syllabified_word += letter
                else:
                    _pre_syllabified_word += block

        return _pre_syllabified_word

    @staticmethod
    def vowel_block_separator(block: str) -> str:
        """When a block ends with a vowel, it checks where to separate.
        There are 8 possibilities in the spanish language.
        1. Vow,
        2. Cons/Vow,
        3. Cons/Cons/Vow, 4. Cons/(L|R|H)/Vow,
        5. Cons/Cons/Cons/Vow, 6. Cons/Cons/(L|R|H)/Vow
        7. Cons/Cons/Cons/Cons/Vow, 8. Cons/Cons/Cons/(L|R|H)/Vow"""

        block_length = len(block)

        if block_length < 3:
            return "-" + block  # Cases 1 and 2

        if block_length == 3:
            if block[1] in "rl":
                if block[1] == "l" and block[0] == "r":
                    # rlo -> r-lo -> -Car-los (Ex: Ar-lan-za, far-lo-pa)
                    return block[0] + "-" + block[1:]

                if block[0] in "sSmMnN":
                    # nri -> n-ri -> In-ri (Ex: Israel, islote)
                    return block[0] + "-" + block[1:]

                else:
                    # bri -> -bri -> hí-bri-do (Ex: a-cri-tud, a-cli-ma-tar-se)
                    return "-" + block

            elif block[1] in "h" and block[0] in "Cc":
                # Letter 'ch' -> -cho-ri-zo (Ex: cha-mi-zo)
                return "-" + block

            else:
                # xqu -> x-qu -> ex-qui-si-to
                return block[0] + "-" + block[1:]

        else:
            if block[-2] in "rl":
                return block[:-3] + "-" + block[-3:]  # Cases 4, 6 and 8
            else:
                return block[:-2] + "-" + block[-2:]  # Cases 3, 5 and 7

    @staticmethod
    def diphthong_finder(vowel_block: str) -> Union[str, None]:
        """Vowels are already separated.
        Now we have to check if they are diphthongs instead of hiatus.
        Possible inputs:

        -Must be a string consisting of two vowels and one hyphen in between them ('h' possible).
        -Possibilities -> weak-strong | strong-weak | strong-strong | weak-weak.
        -Strong = 'aeoáéó'
        -Weak = 'iuü'
        -Weak accented = 'íú'"""
        clean_block = vowel_block.replace("-", "")
        clean_without_hache = clean_block.replace("h", "")

        if len(clean_without_hache) > 2:
            return Word.tripthong_parser(vowel_block)

        first_vowel, second_vowel = list(clean_without_hache)

        hiatus_conditions = [
            first_vowel.lower() == second_vowel.lower(),
            first_vowel in strong_vowels and second_vowel in strong_vowels,
            first_vowel in weak_accented_vowels and second_vowel in strong_vowels,
            first_vowel in strong_vowels and second_vowel in weak_accented_vowels,
        ]

        if any(hiatus_conditions):
            return vowel_block

        else:
            return vowel_block.replace("-", "")

    @staticmethod
    def tripthong_parser(vowel_group):
        return vowel_group.replace('-', '')

    @staticmethod
    def accentuation_finder(word: str) -> int:
        """oxytone: word stressed on the ultima -> 1
        paroxytone: word with stressed on the penult -> return 2
        proparoxytone: word with stressed on the antepenult -> 3
        and so on...

        See: https://en.wikipedia.org/wiki/Oxytone
        See: https://en.wikipedia.org/wiki/Ultima_(linguistics)
        """

        word = word.lower()

        if word.count("-") <= 1:
            return 1

        if word.endswith("-men-te"):
            #  An adverb in -mente keeps the stress of its adjective as a
            #  secondary one, but is read as a paroxytone whatever that
            #  adjective's written accent says: 'cortésmente', 'rápidamente'.
            return 2

        accent = re.search(f"[{accented_vowels}]", word)
        if accent:
            remaining = word[accent.end():].count("-")
            if remaining > 2:
                #  This case is the very seldom superproparoxytone word_list
                return 4

            if remaining == 2:
                #  proparoxytone
                return 3

            if remaining == 1:
                #  paroxytone
                return 2

            #  oxytone
            return 1

        if word[-1] in "ns" + unaccented_vowels:
            return 2

        return 1

    @cached_property
    def rhyme(self) -> Rhyme:
        return rhyme(self.word_syllabified, self.accentuation)
