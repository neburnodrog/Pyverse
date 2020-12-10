import string
from typing import List
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
        self.word_badly_syllabified = self.syllabify(self.word_text)
        self.word_syllabified = self.second_scan(self.word_badly_syllabified)

    def syllabify(self, word: str) -> str:
        block = ""
        syllabified_word = ""

        for i, letter in enumerate(word):
            block += letter
            if letter == " " or letter in string.punctuation:
                syllabified_word += block
                block = ""

            elif letter in vowels:
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
            7. Cons/Cons/Cons/Cons/Vow, 8. Cons/Cons/Cons/(L|R|H)/Vow"""

        block_length = len(block)

        if block_length < 3:
            return "-" + block  # Cases 1 and 2

        if block_length >= 3:
            if block[-2] in "rlhRLH":
                return block[:-3] + "-" + block[-3:]  # Cases 4, 6 and 8
            else:
                return block[:-2] + "-" + block[-2:]  # Cases 3, 5 and 7

    def second_scan(self, word: str) -> str:
        """Re-cut the word in syllables to account for special cases (see Hiatus & Diphthongs, etc)"""
        syllabified_word = word.split("-")[1:]
        diphthonged_word = []
        new_syllabified_word = []

        for syllable in diphthonged_word:
            new_syllable = self.diphthongs_maker(syllable)
            new_syllabified_word.append(new_syllable)

        return "".join(new_syllabified_word)

    def diphthongs_maker(self, syllable: str) -> str:
        """Account for diphthongs"""
        if len(syllable) == 1:
            return syllable
        #  Possible to have blocks of more than 3 letters?
        #  Look for a big input syllabify all words and regex if there some long ones

        new_syllable = ""

        for i, letter in enumerate(syllable):
            if letter not in vowels:
                new_syllable += letter

        return "-" + new_syllable

    @staticmethod
    def vowel_separator(vowel_block: str) -> str:
        """     Groups of 2 or 3 letters (VV / VHV / VVV)
                Vowel: V, Letter H: H
        """

        if "h" in vowel_block:
            vowel_one = vowel_block[0]
            vowel_two = vowel_block[2]
            if vowel_two in strong_vowels or vowel_block[1] in weak_accented_vowels:
                if vowel_one in strong_vowels or vowel_one in weak_accented_vowels:
                    return vowel_one + "-" + "h" + vowel_two
                else:
                    return vowel_block
            else:
                return vowel_block

        else:
            if vowel_block[1] in strong_vowels or vowel_block[1] in weak_accented_vowels:
                if vowel_block[0] in strong_vowels or vowel_block[0] in weak_accented_vowels:
                    return vowel_block[0] + "-" + vowel_block[1]
                return vowel_block
            return vowel_block


def main():
    sentence = input("Enter word/sentence to syllabify: ")
    syllabifier = Syllabifier(sentence)
    print(syllabifier)


if __name__ == "__main__":
    main()
