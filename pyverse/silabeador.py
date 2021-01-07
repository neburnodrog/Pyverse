import re
from typing import List, Union, Dict, Tuple
from pyverse.vars import *
from nlt import numlet as nl


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

        1. if the the last word is oxytone we add 1 syllable to the verse meter.
        2. if it is paroxytone (the most common case in spanish) we leave it as it is.
        3. if it is proparoxytone we sustract 1 syllable from the counting.

        """

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


class Sentence:
    def __init__(self, sentence: str) -> None:
        self.sentence_text = sentence
        self.word_objects = [Word(word) for word in self.sentence_text.split()]
        self.last_word = self.word_objects[-1]
        self.synalephas: List[str] = []
        self.syllabified_sentence = self.sentence_syllabifier()

    def __repr__(self):
        sentence = self.sentence_text
        if len(sentence) > 50:
            try:
                cut_index = sentence.index(" ", 50)
                sentence = sentence[:cut_index] + " [...]"
            except ValueError:
                pass

        return f"<Sentence: {sentence}>"

    @property
    def syllabified_words_punctuation(self) -> List[str]:
        """For tests"""
        sentence = [word.syllabified_w_punct for word in self.word_objects]
        return sentence

    def sentence_syllabifier(self) -> str:
        words: List[Word] = self.word_objects
        syllabified_sentence = []
        last_letter = "z"
        last_word = words[-1]

        for i, word in enumerate(words):
            if last_letter in unaccented_vowels:
                if self.strip_hyphen(word):
                    syllabified_sentence.append(word.syllabified_w_punct.lstrip("-"))
                    self.append_synalepha(last_word, word)

                else:
                    syllabified_sentence.append(word.syllabified_w_punct)

            else:
                syllabified_sentence.append(word.syllabified_w_punct)

            last_letter = word.syllabified_w_punct[-1]
            last_word = word

        return " ".join(syllabified_sentence)

    @staticmethod
    def strip_hyphen(word) -> bool:
        word_text = word.syllabified_w_punct.lstrip("-hH")

        if word_text.rstrip(punctuation) == "y":
            # 'y' count as vowel in this situation
            return True

        if word_text[0] in consonants:
            # No synalepha here
            return False

        if word_text[0] in accented_vowels:
            """
            'el arma ártica' -> False -> '-el -ar-ma -ár-ti-ca'
            'el blanco áspid' -> False -> '-el -blan-co -ás-pid'
            """
            return False

        if word_text[0] in unaccented_vowels:
            """\tif it an unaccented vowel return False if word has 2 syllable and is paroxytone:
            'el arma antigua' -> True -> '-el -ar-ma an-ti-gua'
            'el arma antes' -> False -> '-el -ar-ma -an-tes'
            'el arma azul' -> True -> '-el -ar-ma -a-zul'"""
            if word.number_of_syllables == 2 and word.accentuation == 2:
                # Paroxytone, 2 syllables -> "alto"
                return False

        return True

    def append_synalepha(self, first_word, second_word) -> None:
        first_word_text = first_word.word_untrimmed
        second_word_text = second_word.word_untrimmed
        self.synalephas.append(first_word_text + " " + second_word_text)


class Word:
    def __init__(self, word: str) -> None:
        self.word_untrimmed = word
        self.word_text = self.stripped_word.lower()
        self.word_syllabified = self.syllabify_word()
        self.syllabified_w_punct = self.add_punctuation()
        self.number_of_syllables = self.syllable_counter()
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

        if vowel_groupings := re.findall(f"[{vowels}]-h?[{vowels}]+", syllabified_word):
            for hiatus in vowel_groupings:
                diphthong = self.diphthong_finder(hiatus)
                if diphthong:
                    syllabified_word = syllabified_word.replace(hiatus, diphthong)

        if not syllabified_word.startswith("-"):
            syllabified_word = "-" + syllabified_word

        return syllabified_word

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
        """When a block ends with a vowel, it check where to separate.
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
        clean_block = vowel_block.replace("-", "").replace("h", "")
        first_vowel, second_vowel = tuple(clean_block)

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
