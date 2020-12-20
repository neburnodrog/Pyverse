import re
from typing import List, Union, Tuple, Dict
from silabizador.vars import *


class Silabizador:
    def __init__(self, verse: str):
        self.sentence = Sentence(verse)
        self.number_of_syllables: int = self.counter()
        self.consonant_rhyme, self.assonant_rhyme = self.rhymer()
        self.type_of_verse = self.type_verse(verse)

    def counter(self) -> int:
        last_word_type = self.sentence.last_word.accentuation
        if last_word_type:
            return self.sentence.syllabified_sentence.count("-") + last_word_type
        else:
            return self.sentence.word_objects[-2].accentuation - 1

    def rhymer(self) -> Tuple[str, str]:
        last_word = self.sentence.last_word
        word_text = last_word.word_text
        word_accent = last_word.accentuation
        if word_accent is None:
            next_to_last_word = self.sentence.word_objects[-2]
            word_text = next_to_last_word.word_text + word_text
            word_accent = next_to_last_word.accentuation - 1

        rhyme_block = self.rhyme_block_finder(word_text, word_accent)

        consonant_rhyme = self.consonant_rhyme_finder(rhyme_block)
        assonant_rhyme = self.assonant_rhyme_finder(consonant_rhyme)
        consonant_rhyme = consonant_rhyme.replace("ll", "i").replace("y", "i")
        return consonant_rhyme, assonant_rhyme

    @staticmethod
    def rhyme_block_finder(word_text: str, word_accent: int) -> str:
        if word_accent == -2:
            # superproparoxytone
            while word_text.count("-") > 4:
                word_text = word_text[word_text.find("-", 1):]

        if word_accent == -1:
            # proparoxytone
            while word_text.count("-") > 3:
                word_text = word_text[word_text.find("-", 1):]

        elif word_accent == 0:
            # paroxytone
            while word_text.count("-") > 2:
                word_text = word_text[word_text.find("-", 1):]

        else:
            # oxytone
            while word_text.count("-") > 1:
                word_text = word_text[word_text.find("-", 1):]
        return word_text

    @staticmethod
    def consonant_rhyme_finder(rhyme_block: str) -> str:
        block_clean = rhyme_block.replace("-", "")

        if len(block_clean) > 1:
            while block_clean[0] not in vowels:
                if len(block_clean) > 2:
                    if block_clean[0].lower() in "qg" and (
                            block_clean[1].lower() == "u" and (
                            block_clean[2].lower() in "ieíé")):
                        block_clean = block_clean[2:]

                    else:
                        block_clean = block_clean[1:]
                else:
                    block_clean = block_clean[1:]

                if len(block_clean) == 1:
                    break

            if (len(block_clean) > 1
                    and block_clean[0] in weak_vowels
                    and block_clean[1] in vowels):
                block_clean = block_clean[1:]

        if " " in block_clean:
            block_clean = block_clean.replace(" ", "")

        return block_clean

    @staticmethod
    def assonant_rhyme_finder(consonant_rhyme):
        assonant_rhyme = "".join([letter for letter in consonant_rhyme if (letter in vowels or letter == "-")])

        replacements = [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]
        for replacement in replacements:
            assonant_rhyme = assonant_rhyme.replace(replacement[0], replacement[1])

        return assonant_rhyme

    @staticmethod
    def type_verse(sentence: str) -> Dict[str, bool]:
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


class Sentence:
    def __init__(self, sentence: str):
        self.sentence_text = sentence
        self.string_words = self.sentence_text.split()
        self.word_objects = [Word(word) for word in self.string_words]
        self.last_word = self.word_objects[-1]
        self.syllabified_words_punctuation = self.join_words_with_punctuation()
        self.syllabified_sentence = self.sentence_syllabifier(self.syllabified_words_punctuation)

    def join_words_with_punctuation(self):
        sentence = [word.word_text.replace(word.stripped_word, word.syllabified_word) for word in self.word_objects]
        return sentence

    def sentence_syllabifier(self, words: List) -> str:
        syllabified_sentence = []
        last_word_endswith_unaccented_vowel = None
        for i, word in enumerate(words):
            if last_word_endswith_unaccented_vowel:
                if self.strip_hyphen(word, i):
                    syllabified_sentence.append(word.lstrip("-"))

                else:
                    syllabified_sentence.append(word)

            else:
                syllabified_sentence.append(word)

            if word[-1] in unaccented_vowels:
                last_word_endswith_unaccented_vowel = True
            else:
                last_word_endswith_unaccented_vowel = False

        return " ".join(syllabified_sentence)

    def strip_hyphen(self, word_text, index):
        if word_text[0] in "hH":
            word_text = word_text.lstrip("hH")

        if word_text == "y":
            return True

        if word_text[0] in consonants:
            return False

        if word_text[0] in accented_vowels:
            return False

        word = self.word_objects[index]
        if word.number_of_syllables == 2 and word.accentuation == 0:
            # Paroxytone, 2 syllables -> "alto"
            return False

        else:
            return True


class Word:
    def __init__(self, word: str) -> None:
        self.word_text = word  # this variable holds each words with punctuation attached.
        self.stripped_word = word.strip(punctuation + " ")
        self._pre_syllabified_word = self.pre_syllabify(self.stripped_word)
        self.syllabified_word = self.further_scans(self._pre_syllabified_word)
        self.number_of_syllables = self.syllable_counter()
        self.accentuation = self.accentuation_finder(self.stripped_word)

    def pre_syllabify(self, word: str) -> str:
        block = ""
        syllabified_word = ""

        for i, letter in enumerate(word):
            block += letter

            if letter in vowels:
                syllabified_word += self.vowel_block_separator(block)
                block = ""

            elif i == len(word) - 1:
                syllabified_word += letter

        return syllabified_word

    @staticmethod
    def vowel_block_separator(block: str) -> str:
        """ When a block ends with a vowel, it check where to separate.
            There are 8 possibilities in the spanish language.
            1. Vow,
            2. Cons/Vow,
            3. Cons/Cons/Vow, 4. Cons/(L|R|H)/Vow,
            5. Cons/Cons/Cons/Vow, 6. Cons/Cons/(L|R|H)/Vow
            7. Cons/Cons/Cons/Cons/Vow, 8. Cons/Cons/Cons/(L|R|H)/Vow """

        block_length = len(block)

        if block_length < 3:
            return "-" + block  # Cases 1 and 2

        if block_length == 3:
            if block[1] in "rl":

                if block[0] in "sSmM":
                    return block[0] + "-" + block[1:]
                else:
                    return "-" + block

            elif block[1] in "h" and block[0] in "Cc":
                return "-" + block

            else:
                return block[0] + "-" + block[1:]

        if block_length > 3:
            if block[-2] in "rl":
                return block[:-3] + "-" + block[-3:]  # Cases 4, 6 and 8
            else:
                return block[:-2] + "-" + block[-2:]  # Cases 3, 5 and 7

    def further_scans(self, pre_syllabified_word: str) -> str:
        """ Find all vowel groupings in the pre_syllabified_word
            and pass them to diphthong_finder to see if any diphthongs slipped through. """

        vowel_groupings = re.findall(f"[{vowels}]-h?[{vowels}]", pre_syllabified_word)

        for hiatus in vowel_groupings:
            diphthong = self.diphthong_finder(hiatus)
            if diphthong:
                pre_syllabified_word = pre_syllabified_word.replace(hiatus, diphthong)

        return pre_syllabified_word

    @staticmethod
    def diphthong_finder(vowel_block: str) -> Union[str, None]:
        """ Vowels are already separated. Now we have to check if they are diphthongs instead of hiatus.
            Possible inputs:
                -Must be a string consisting of two vowels and one hyphen in between them (Aitch is possible).
                -Possibilities -> weak-strong | strong-weak | strong-strong | weak-weak.
                -Strong = 'aeoáéó'
                -Weak = 'iuü'
                -Weak accented = 'íú' """
        clean_block = vowel_block.replace("-", "").replace("h", "")
        first_vowel, second_vowel = tuple(clean_block)

        if (    # they fulfill one of the conditions for beeing an hiatus:
                (first_vowel.lower() == second_vowel.lower())
                or (first_vowel in strong_vowels and second_vowel in strong_vowels)
                or (first_vowel in weak_accented_vowels and second_vowel in strong_vowels)
                or (first_vowel in strong_vowels and second_vowel in weak_accented_vowels)
        ):
            return vowel_block

        else:
            return vowel_block.replace("-", "")

    @staticmethod
    def accentuation_finder(word: str) -> Union[None, int]:
        """     oxytone: word with stress/accent on the last syllable.
                paroxytone: word with stress/accent on the penultimate syllable.
                proparoxytone: word with stress/accent on the antepenultimate syllable.
        """

        if word.count("-") == 1:
            return None

        accent = re.search(f"[{accented_vowels}]", word)
        if accent:
            remaining = word[accent.end():].count("-")
            if remaining == 3:
                if word.endswith("-men-te"):
                    return 0
                else:
                    #  This case is the very seldom superproparoxytone words
                    return -2

            if remaining == 2:
                #  proparoxytone
                return -1

            elif remaining == 1:
                #  paroxytone
                return 0

            #  oxytone
            return 1

        if word[-1] in "ns":
            return 0

        return 1

    def syllable_counter(self):
        return self.syllabified_word.count("-")


if __name__ == "__main__":
    pass
