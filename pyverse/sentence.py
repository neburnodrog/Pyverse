from typing import List

from pyverse.vars import unaccented_vowels, accented_vowels, consonants, punctuation
from pyverse.word import Word


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
            if word.syllable_count == 2 and word.accentuation == 2:
                # Paroxytone, 2 syllables -> "alto"
                return False

        return True

    def append_synalepha(self, first_word, second_word) -> None:
        first_word_text = first_word.word_untrimmed
        second_word_text = second_word.word_untrimmed
        self.synalephas.append(first_word_text + " " + second_word_text)
