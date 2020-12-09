import string
from poems.help_funcs import (last_word_finder,
                              block_separator,
                              consonant_rhyme_finder,
                              assonant_rhyme_finder,
                              type_verse,
                              counter)

vowels = "aeiouáéíóúAEIOUÁÉÍÓÚ"
vowels_h = vowels + "h"
consonants = ("".join((letter for letter in string.ascii_letters if letter not in vowels)) + "ñÑ")
debiles = "UIui"
debiles_tonicas = "ÚÍúí"
fuertes = "AEOaeo"
fuertes_tildadas = "ÁÉÓáéó"
vowels_tildadas = "áéíóúÁÉÍÓÚ"
punct = "¡!\"#$%&'()*+,./:;<=>¿?@[\\]^_—{|}~-«”»"


class Syllabifier:
    def __init__(self, sentence):
        self.sentence = sentence.strip(".,¿?¡!«'—»();:\"-* ")
        self.last_word = last_word_finder(sentence)
        self.syllabified_sentence = self.syllabify(self.sentence)
        self.syllables, self.agullaes = counter(self.syllabified_sentence)
        self.consonant_rhyme, self.assonant_rhyme = self.rhymer(self.syllabified_sentence)
        self.beg, self.int, self.end = type_verse(sentence)

    def syllabify(self, sentence):
        block = ""
        syllabified_sentence = ""

        for i, letter in enumerate(sentence):
            block += letter
            if letter == " ":
                syllabified_sentence += block
                block = ""

            elif len(block) == 1 and letter in string.punctuation:
                syllabified_sentence += block
                block = ""

            elif letter in vowels:
                if len(block) == 1:
                    try:
                        if syllabified_sentence.strip()[-1] in vowels:
                            if (syllabified_sentence.strip()[-1] in debiles
                                    and block in debiles
                                    and sentence[i + 1] not in "ns"
                            ):
                                syllabified_sentence += "-" + block
                                block = ""
                            else:
                                syllabified_sentence += block
                                block = ""
                        else:
                            syllabified_sentence += "-" + block
                            block = ""
                    except IndexError:
                        syllabified_sentence += "-" + block
                        block = ""

                elif len(block) == 2:
                    try:
                        if (
                                block[0] in "hH"
                                and syllabified_sentence.strip()[-1] in vowels
                                and (not sentence[i + 1] in fuertes or sentence[i + 1] in debiles_tonicas)
                        ):
                            syllabified_sentence += block
                            block = ""
                        else:
                            syllabified_sentence += "-" + block
                            block = ""
                    except IndexError:
                        syllabified_sentence += "-" + block
                        block = ""

                elif len(block) == 3:
                    if block[-2] in "rlhRLH":
                        syllabified_sentence += "-" + block
                        block = ""
                    else:
                        syllabified_sentence += block[0] + "-" + block[1:]
                        block = ""

                elif len(block) == 4:
                    if block[-2] in "rlhRLH":
                        syllabified_sentence += block[0] + "-" + block[1:]
                        block = ""
                    else:
                        syllabified_sentence += block[0:2] + "-" + block[2:]
                        block = ""

                elif len(block) == 5:
                    if block[-2] in "rlhRLH":
                        syllabified_sentence += block[0:2] + "-" + block[2:]
                        block = ""
                    else:
                        syllabified_sentence += block[0:3] + "-" + block[3:]
                        block = ""

            elif i == len(sentence) - 1 and (
                    letter in consonants or letter in string.punctuation
            ):
                syllabified_sentence += letter

        return self.second_scan(syllabified_sentence.strip(".,!?¡¿:;"))

    def second_scan(self, sentence):
        separated_sentence = ""

        while sentence:
            try:
                cut_point = sentence.index("-", sentence.index("-") + 1)
                block = sentence[0:cut_point]
                sentence = sentence[cut_point:]
            except ValueError:
                block = sentence
                sentence = ""

            new_block = block_separator(block)
            separated_sentence += new_block

        return separated_sentence

    def rhymer(self, verso):
        last_word = last_word_finder(verso)
        consonant_rhyme = consonant_rhyme_finder(last_word, self.agullaes)
        assonant_rhyme = assonant_rhyme_finder(consonant_rhyme)
        consonant_rhyme = consonant_rhyme.replace("ll", "i").replace("y", "i")
        return consonant_rhyme, assonant_rhyme


def main():
    sentence = input("Enter word/sentence to syllabify: ")
    syllabifier = Syllabifier(sentence)
    print("[+] Sentence:", syllabifier.sentence)
    print("[+] Syllabified sentence:", syllabifier.syllabified_sentence)
    print("[+] Syllables:", syllabifier.syllables)
    print("[+] Last word:", syllabifier.last_word)
    print("[+] Aguda, llana o esdrújula?:", syllabifier.agullaes)
    print("[+] Bloque consonante a rimar:", syllabifier.consonant_rhyme)
    print("[+] Bloque asonante a rimar:", syllabifier.assonant_rhyme)
    print("[+] beg: {}, int: {}, end: {}".format(syllabifier.beg, syllabifier.int, syllabifier.end))


if __name__ == "__main__":
    main()
