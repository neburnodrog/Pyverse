import string
from typing import Union, Tuple, List
import re
from pyverse.vars import punctuation, vowels, strong_vowels, weak_accented_vowels, accented_vowels, unaccented_vowels, \
    trans_accented_vowels


class Word:
    def __init__(self, word: str) -> None:
        self.word_untrimmed = word
        self.word_text = self.stripped_word.lower()
        self.word_syllabified = self.syllabify_word()
        self.syllabified_w_punct = self.add_punctuation()
        self.syllable_count = self.syllable_counter()
        self.accentuation = self.accentuation_finder(self.word_syllabified)
        self.consonant_rhyme = self.consonant_rhyme_finder()
        self.assonant_rhyme = self.assonant_rhyme_finder()

    def __repr__(self):
        return f"<Word: '{self.word_syllabified}'>"

    @property
    def stripped_word(self) -> str:
        _stripped_word = self.word_untrimmed.strip(punctuation + " ")
        return _stripped_word

    def add_punctuation(self) -> str:
        return self.word_untrimmed.replace(self.stripped_word, self.word_syllabified)

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
            syllabified_word = syllabified_word.replace(vowel_group, self.check_if_separation(vowel_group))


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

        word = self.stripped_word

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
        print(vowel_group)
        # return vowel_group
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

        if word.count("-") == 1:
            return 1

        accent = re.search(f"[{accented_vowels}]", word)
        if accent:
            remaining = word[accent.end():].count("-")
            if remaining > 2:
                if word.endswith("-men-te"):
                    return 2
                else:
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

    def syllable_counter(self):
        return self.word_syllabified.count("-")

    def consonant_rhyme_finder(self) -> str:
        """If the word is atonic, then it has no rhyme -> None
        return the word from its last stressed vowel.
        Also remove any posible accents as they don't provide any info:
        would just duplicate entries in the DB for the same rhyme.
        Ex: '-al-ga-ra-bí-a' -> 'ia'"""

        stressed_syll, rest_of_sylls = self.rhyme_block_getter()
        from_last_stressed_vowel = self.last_stressed_vowel_finder(
            stressed_syll, rest_of_sylls
        )

        from_last_stressed_vowel = from_last_stressed_vowel.translate(
            trans_accented_vowels
        )
        return from_last_stressed_vowel + rest_of_sylls

    def rhyme_block_getter(self) -> Tuple[str, str]:
        """ Gets the ending of self.word_text from the beginning of the last stressed syllable. """

        rhyme_block = self.word_syllabified
        hyphens_left_in_block = self.accentuation

        while rhyme_block.count("-") > hyphens_left_in_block:
            rhyme_block = rhyme_block[rhyme_block.find("-", 1):]

        return self.rhyme_block_chopper(rhyme_block)

    @staticmethod
    def rhyme_block_chopper(rhyme_block: str) -> Tuple[str, str]:
        """Returns a tuple -> (last_stressed_syllable, rest_of_the_syllables)
        where all of them are stripped of the hyphens.
        If word is oxytone -> one syllable -> (stressed_one, "")
        if paroxytone -> two syllables -> (stressed_one, rest)"""

        rhyme_block = rhyme_block.lstrip("-")

        cut_index = rhyme_block.find("-")
        if cut_index > 0:
            stressed_syllable = rhyme_block[:cut_index]
            rest_of_the_syllables = rhyme_block[cut_index + 1:].replace("-", "")

        else:
            stressed_syllable = rhyme_block
            rest_of_the_syllables = ""

        return stressed_syllable.replace("-", ""), rest_of_the_syllables

    def last_stressed_vowel_finder(self, syllable: str, rest: str) -> str:
        if not rest:
            if re.search("[y]$", syllable):
                syllable = syllable.replace("y", "i")

        if match := re.search(f"[{accented_vowels}]", syllable):
            last_stressed_vowel: str = match.group()
            rest_of_syll: str = syllable[match.end():]  # Can be empty string
            return last_stressed_vowel + rest_of_syll

        if match := re.search(f"[{vowels}]+", syllable):
            last_stressed_vowel = self.find_stressed_vowel(match.group())
            rest_of_syll = syllable[match.end():]
            return last_stressed_vowel + rest_of_syll

        return syllable

    @staticmethod
    def find_stressed_vowel(vowel_group: str) -> str:
        """Can be a vowel or a diphthong or a tripthong.
        Hiatuses are already discarded."""

        if len(vowel_group) == 1:
            return vowel_group

        if strong_vowel := re.search(f"[{strong_vowels}]", vowel_group):
            #  This regex excludes triphthongs and diphthongs with strong vowels
            return strong_vowel.group() + vowel_group[strong_vowel.end():]

        return vowel_group[
            -1
        ]  # only diphthons with weak vowels left -> stress on the second one

    def assonant_rhyme_finder(self) -> str:
        consonant_rhyme = self.consonant_rhyme

        if match := re.search("[gq]u[éeíi]", consonant_rhyme):
            sub = match.group().replace("u", "")
            consonant_rhyme = consonant_rhyme.replace(match.group(), sub)

        assonant_rhyme = []
        for letter in consonant_rhyme:
            if letter in vowels:
                assonant_rhyme.append(letter)

        return "".join(assonant_rhyme)
