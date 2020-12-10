from typing import Optional, List, Tuple
import string

__all__ = [
    "last_word_finder",
    "consonant_rhyme_finder",
    "assonant_rhyme_finder",
    "type_verse",
    "agu_lla_esdr",
    "counter",
    "punctuation",
    "uppercase",
    "vowels",
    "vowels_with_h",
    "consonants",
    "weak_vowels",
    "weak_accented_vowels",
    "strong_vowels",
    "accented_vowels",
    "g_and_q",
]

# VARIABLES
punctuation = string.punctuation + r'¡¿—«”»'
uppercase = string.ascii_uppercase + "ÑÁÉÍÓÚ"
vowels = "aeiou" + "áéíóú" + "AEIOU" + "ÁÉÍÓÚ" + "üÜ"
vowels_with_h = vowels + "hH"
translation_table = str.maketrans({letter: "" for letter in vowels})
consonants = string.ascii_letters.translate(translation_table) + "ñÑ"
weak_vowels = "UIuiü"
weak_accented_vowels = "ÚÍúí"
strong_vowels = "AEOaeoÁÉÓáéó"
accented_vowels = "áéíóúÁÉÍÓÚ"
g_and_q = "gGqQ"


def counter(sentence: str, last_word_type: int) -> Tuple[int]:
    return sentence.count("-") + last_word_type


def agu_lla_esdr(word: str) -> int:
    """     Returns -1 if the word is proparoxytone; 0 if paroxytone; 1 if oxytone
            oxytone: word with stress/accent on the last syllable.
            paroxytone: word with stress/accent on the penultimate syllable.
            proparoxytone: word with stress/accent on the antepenultimate syllable.
    """

    if not word.startswith("-"):
        word = "-" + word

    if word.count("-") == 1:
        return 1

    for i, letter in enumerate(word):
        if letter in accented_vowels:
            remaining = word.count("-", i)
            if remaining == 3:
                if word.endswith("-men-te"):
                    #  This case is the very seldom superproparoxytone words like
                    return -2

            if remaining == 2:
                #  proparoxytone
                return -1
            elif remaining == 1:
                #  paroxytone
                return 0
            #  oxytone
            return 1

    if (word[-1] in vowels + "y"
            or word[-1] in "ns"
            or (word[-1] == "y" and word[-2] == " ")):
        return 0

    return 1


def consonant_rhyme_finder(last_word, agullaes):
    if not last_word.startswith("-"):
        last_word = "-" + last_word
    if agullaes == -1:
        # esdrújula
        while last_word.count("-") > 3:
            last_word = last_word[last_word.find("-", 1):]
    elif agullaes == 0:
        # llana
        while last_word.count("-") > 2:
            last_word = last_word[last_word.find("-", 1):]
    else:
        # aguda
        while last_word.count("-") > 1:
            last_word = last_word[last_word.find("-", 1):]

    block_clean = "".join([letter for letter in last_word if letter != "-"])

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


def assonant_rhyme_finder(consonant_rhyme):
    assonant_rhyme = "".join([letter for letter in consonant_rhyme if (letter in vowels or letter == "-")])

    replacements = [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]
    for replacement in replacements:
        assonant_rhyme = assonant_rhyme.replace(replacement[0], replacement[1])

    return assonant_rhyme


def type_verse(sentence):
    is_beg = True if sentence.strip(punctuation)[0] in uppercase else False

    if ((sentence.endswith("...") or not sentence.endswith("."))
            and sentence.strip(punctuation)[0] not in uppercase):
        is_int = True
    else:
        is_int = False

    if sentence.endswith(".") and not sentence.endswith("..."):
        is_end = True
    else:
        is_end = False

    return is_beg, is_int, is_end


def last_word_finder(sentence: str) -> str:
    """ sentece is already punctuation stripped
        It should return only the last word in lowercase"""

    if sentence.count(" ") != 0:
        last_word = sentence[sentence.rfind(" "):].strip(punctuation + " ")
        return decapitalize(last_word)

    return decapitalize(sentence).strip(punctuation + " ")


def decapitalize(word: str) -> str:
    return word[0].lower() + word[1:]
