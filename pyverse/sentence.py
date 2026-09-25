from typing import List, Tuple

from pyverse.vars import unaccented_vowels, accented_vowels, consonants
from pyverse.word import Word


class Sentence:
    def __init__(self, sentence: str) -> None:
        self.sentence_text = sentence
        self.word_objects = [Word(word) for word in self.sentence_text.split()]
        self.last_word = self.word_objects[-1]
        self.joined_words = self.find_synalephas()
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

    @property
    def synalephas(self) -> List[str]:
        words = self.word_objects
        return [
            words[i - 1].word_untrimmed + " " + words[i].word_untrimmed
            for i in self.joined_words
        ]

    def find_synalephas(self) -> Tuple[int, ...]:
        """The positions of the words pronounced as one with the word before."""

        joined = []
        last_letter = "z"

        for i, word in enumerate(self.word_objects):
            if last_letter in unaccented_vowels and self.joins_previous_word(word):
                joined.append(i)

            last_letter = word.syllabified_w_punct[-1]

        return tuple(joined)

    def sentence_syllabifier(self) -> str:
        return " ".join(
            word.syllabification.render(leading_hyphen=i not in self.joined_words)
            for i, word in enumerate(self.word_objects)
        )

    @staticmethod
    def joins_previous_word(word: Word) -> bool:
        """Whether this word is pronounced as one with the word before it.
        Only asked of a word whose predecessor ends in an unaccented vowel."""

        if word.syllabification.prefix:
            """Punctuation before the word marks a pause, the same way
            punctuation after the previous word already does.
            'el arma ¿antigua?' -> False -> '-el -ar-ma ¿-an-ti-gua?'"""
            return False

        word_text = word.syllabification.render(
            leading_hyphen=False, with_punctuation=False
        ).lstrip("hH")
        first_letter = word_text[:1]

        if word_text == "y":
            # 'y' count as vowel in this situation
            return True

        if first_letter in consonants:
            # No synalepha here
            return False

        if first_letter in accented_vowels:
            """
            'el arma ártica' -> False -> '-el -ar-ma -ár-ti-ca'
            'el blanco áspid' -> False -> '-el -blan-co -ás-pid'
            """
            return False

        if first_letter in unaccented_vowels:
            """\tif it an unaccented vowel return False if word has 2 syllable and is paroxytone:
            'el arma antigua' -> True -> '-el -ar-ma an-ti-gua'
            'el arma antes' -> False -> '-el -ar-ma -an-tes'
            'el arma azul' -> True -> '-el -ar-ma -a-zul'"""
            if word.syllable_count == 2 and word.accentuation == 2:
                # Paroxytone, 2 syllables -> "alto"
                return False

        return True
