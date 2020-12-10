import re
from typing import List, Union
from .helper_funcs import *


class Syllabifier:
    def __init__(self, sentence):
        self.sentence = sentence
        self.stripped_sentence = sentence.strip(punctuation)
        self.last_word = last_word_finder(self.stripped_sentence)
        self.syllabified_sentence = Sentence(self.stripped_sentence).syllabified_sentence
        self.agu_lla_esdr = agu_lla_esdr(self.last_word)
        self.number_of_syllables = counter(self.syllabified_sentence.syllabified_sentence, self.agu_lla_esdr)
        self.consonant_rhyme, self.assonant_rhyme = self.rhymer(self.syllabified_sentence)
        self.beginning_verse, self.intermediate_verse, self.ending_verse = type_verse(sentence)

    def __str__(self):
        return f"""{self.sentence}:

    \t stripped sentence                     : {self.stripped_sentence}
    \t last word                             : {self.last_word}
    \t syllabified sentence                  : {self.syllabified_sentence}
    \t aguda (1), llana (0) o esdrujula (-1) : {self.agu_lla_esdr}
    \t numero de silabas                     : {self.number_of_syllables}
    \t rima consonantemente con palabras en  : {self.consonant_rhyme}
    \t rima asonantemente con palabras en    : {self.assonant_rhyme}
    \t comienzo? {self.beginning_verse}, intermedio? {self.intermediate_verse}, final? {self.ending_verse}
                """

    def rhymer(self, verso):
        last_word = last_word_finder(verso)
        consonant_rhyme = consonant_rhyme_finder(last_word, self.agu_lla_esdr)
        assonant_rhyme = assonant_rhyme_finder(consonant_rhyme)
        consonant_rhyme = consonant_rhyme.replace("ll", "i").replace("y", "i")
        return consonant_rhyme, assonant_rhyme


class Sentence:
    def __init__(self, sentence):
        self.sentence_text = sentence.strip(punctuation + " ")
        self.words = [Word(word_string) for word_string in sentence.split()]
        self.words_text = [word_instance.word_text for word_instance in self.words]
        self.syllabified_sentence = self.sentence_syllabifier(self.words_text)

    def sentence_syllabifier(self, words: List) -> str:
        sentence = "".join(words)  # Care about punctuation

        '''if syllabified_sentence.strip()[-1] in vowels:
            if (
                    syllabified_sentence.strip()[-1] in weak_vowels
                    and block in weak_vowels
                    and word[i + 1] not in "ns"
            ):
                syllabified_sentence += "-" + block
                block = ""
            else:
                syllabified_sentence += block
                block = ""
        else:
            syllabified_sentence += "-" + block
            block = ""'''

        '''if (
                block[0] in "hH"
                and syllabified_sentence.strip()[-1] in vowels
                and not block[1] in strong_vowels + weak_accented_vowels
        ):
            syllabified_sentence += block
            block = ""
        else:
            syllabified_sentence += "-" + block
            block = ""'''


class Word:
    def __init__(self, word: str) -> None:
        self.word_text = word.strip(punctuation + " ")
        self.pre_syllabified_word = self.pre_syllabify(self.word_text)
        self.syllabified_word = self.further_scans(self.pre_syllabified_word)

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


def main():
    sentence = input("Enter word/sentence to syllabify: ")
    syllabifier = Syllabifier(sentence)
    print(syllabifier)


if __name__ == "__main__":
    main()
