from typing import Optional, List, Tuple
import string

__all__ = ["last_word_finder",
           "block_separator",
           "consonant_rhyme_finder",
           "assonant_rhyme_finder",
           "type_verse",
           "counter",
           "punctuation",
           "uppercase",
           "vowels",
           "vowels_with_h",
           "consonants",
           "weak_vowels",
           "weak_accented_vowels",
           "strong_vowels",
           "accented_vowels",]


# VARIABLES
punctuation = string.punctuation + r'¡¿—«”»'
uppercase = string.ascii_uppercase + "ÑÁÉÍÓÚ"
vowels = "aeiou" + "áéíóú" + "AEIOU" + "ÁÉÍÓÚ" + "üÜ"
vowels_with_h = vowels + "hH"
translation_table = str.maketrans({letter: "" for letter in vowels})
consonants = string.ascii_letters.translate(translation_table) + "ñÑ"
weak_vowels = "UIui"
weak_accented_vowels = "ÚÍúí"
strong_vowels = "AEOaeo"
accented_vowels = "áéíóúÁÉÍÓÚ"


def counter(sentence: str) -> Tuple[int, int]:
    sil_count = sentence.count("-")
    last_word = last_word_finder(sentence)
    type_word = agu_lla_esdr(last_word)
    return sil_count + type_word, type_word


def block_separator(block: str) -> str:
    separated_block = ""

    block = block.strip("-")

    i = 0
    while True:
        try:
            letter = block[i]

            if letter not in vowels:
                separated_block += letter
                i += 1

            elif letter in vowels:
                try:
                    if block[i + 1] not in vowels_with_h:
                        separated_block += letter
                        i += 1

                    elif block[i + 1] == "h":
                        try:
                            if block[i + 2] in vowels:
                                vowel_block = vowel_separator(block[i:i + 3])
                                separated_block += vowel_block
                                i += 3
                            else:
                                separated_block += block[i:i + 3]
                                i += 3
                        except IndexError:
                            separated_block += letter
                            i += 1

                    else:
                        vowel_block = vowel_separator(block[i:i + 2])
                        separated_block += vowel_block
                        i += 2
                except IndexError:
                    separated_block += letter
                    i += 1

        except IndexError:
            break

    return "-" + separated_block


def vowel_separator(vowel_block: str) -> str:
    """     Groups of 2 or 3 letters (VV / VHV / VVV)
            Vowel: V, Letter H: H
    """

    if "h" in vowel_block:
        vocal_uno = vowel_block[0]
        vocal_dos = vowel_block[2]
        if vocal_dos in strong_vowels or vowel_block[1] in weak_accented_vowels:
            if vocal_uno in strong_vowels or vocal_uno in weak_accented_vowels:
                return vocal_uno + "-" + "h" + vocal_dos
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
    sentence = sentence.strip(punctuation + " ")

    if sentence.count(" ") != 0:
        last_word = sentence[sentence.rfind(" "):]

        if last_word == "y":
            last_word = sentence
            while last_word.count(" ") > 1:
                last_word = last_word[last_word.find(" "):].strip()

            if all([letter.isdigit() for letter in last_word]):
                int_to_str(last_word)

            return decapitalize(last_word)

        return decapitalize(last_word)

    return decapitalize(sentence)


def decapitalize(word: str, strict: Optional[bool] = True):
    if strict:
        return word.lower()
    return word[0].lower() + word[1:]
