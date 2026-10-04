import re
from dataclasses import dataclass
from typing import List, Tuple

from pyverse.vars import (
    accented_vowels,
    strong_vowels,
    trans_accented_vowels,
    vowels,
)

#  Quilis, Métrica española: a final unstressed 'i' is read as 'e' and a final
#  unstressed 'u' as 'o', so that 'Venus' rhymes with 'cielo'.
loose_final_vowels = {"i": "e", "u": "o"}


@dataclass(frozen=True)
class Rhyme:
    """The rhymes of a word, counted from its last stressed vowel.

    Lowercase, with accents stripped: neither carries rhyming information,
    and both would otherwise duplicate entries for the same rhyme.
    Ex: '-al-ga-ra-bí-a' -> consonant 'ia', assonant 'ia'
    """

    consonant: str
    consonant_yeismo: str
    assonant: str
    assonant_strict: str


def rhyme(syllabified: str, accentuation: int) -> Rhyme:
    """syllabified is a hyphen-separated word ('-por-que').
    accentuation counts syllables from the end, 1 being oxytone."""

    syllabified = syllabified.lower()
    stressed_syllable, rest = _chop(_rhyme_block(syllabified, accentuation))
    from_stressed_vowel = _from_last_stressed_vowel(stressed_syllable, rest)
    consonant = from_stressed_vowel.translate(trans_accented_vowels) + rest
    loose, strict = _assonant(consonant)

    return Rhyme(
        consonant=consonant,
        consonant_yeismo=consonant.replace("ll", "y"),
        assonant=loose,
        assonant_strict=strict,
    )


def _rhyme_block(syllabified: str, accentuation: int) -> str:
    """The ending of the word from the start of its last stressed syllable."""

    block = syllabified
    while block.count("-") > accentuation:
        block = block[block.find("-", 1):]

    return block


def _chop(rhyme_block: str) -> Tuple[str, str]:
    """(last stressed syllable, the syllables after it), both without hyphens.
    Oxytone -> one syllable -> (stressed, ""). Paroxytone -> (stressed, rest)."""

    rhyme_block = rhyme_block.lstrip("-")

    cut_index = rhyme_block.find("-")
    if cut_index > 0:
        stressed_syllable = rhyme_block[:cut_index]
        rest_of_the_syllables = rhyme_block[cut_index + 1:].replace("-", "")

    else:
        stressed_syllable = rhyme_block
        rest_of_the_syllables = ""

    return stressed_syllable.replace("-", ""), rest_of_the_syllables


def _from_last_stressed_vowel(syllable: str, rest: str) -> str:
    if not rest:
        if re.search("[y]$", syllable):
            syllable = syllable.replace("y", "i")

    if match := re.search(f"[{accented_vowels}]", syllable):
        return match.group() + syllable[match.end():]

    if match := re.search(f"[{vowels}]+", syllable):
        return _stressed_vowel(match.group()) + syllable[match.end():]

    return syllable


def _stressed_vowel(vowel_group: str) -> str:
    """Can be a vowel, a diphthong or a triphthong. Hiatuses are already discarded."""

    if len(vowel_group) == 1:
        return vowel_group

    if strong_vowel := re.search(f"[{strong_vowels}]", vowel_group):
        #  This regex excludes triphthongs and diphthongs with strong vowels
        return strong_vowel.group() + vowel_group[strong_vowel.end():]

    #  only diphthongs with weak vowels left -> stress on the second one
    return vowel_group[-1]


def _assonant(consonant_rhyme: str) -> Tuple[str, str]:
    """(loose, strict): the stressed vowel followed by the last audible one.

    Vowels between the two drop out, as does the weak vowel of a diphthong,
    so 'lánguida' gives 'aa' and 'baile' gives 'ae'. A rhyme with a single
    audible vowel is one character long: 'rey' gives 'e'.
    """

    audible = _without_silent_u(consonant_rhyme)

    first = re.search(f"[{vowels}]", audible)
    if not first:
        return "", ""

    stressed = first.start()
    last = _nuclei(audible)[-1]

    if last == stressed:
        return audible[stressed], audible[stressed]

    strict = audible[last]
    return audible[stressed] + loose_final_vowels.get(strict, strict), (
        audible[stressed] + strict
    )


def _without_silent_u(text: str) -> str:
    """The 'u' of que/qui/gue/gui is not pronounced. 'ü' is, and stays."""

    return re.sub("([gq])u([eéií])", r"\1\2", text)


def _nuclei(text: str) -> List[int]:
    """The index of every vowel carrying a syllable of its own.

    The weak vowel of a diphthong carries none. Two strong vowels in a row are
    a hiatus, so both do. Accents are already stripped by the time this is
    asked, which costs nothing: a hiatus written with an accent on its weak
    vowel ('sabíamos') only ever holds the stressed vowel, and that one is
    located by its position rather than counted here.
    """

    found = []

    for group in re.finditer(f"[{vowels}]+", text):
        letters = group.group()

        if len(letters) == 1:
            found.append(group.start())
            continue

        strong = [i for i, letter in enumerate(letters) if letter in strong_vowels]
        if strong:
            found.extend(group.start() + i for i in strong)
        else:
            #  a diphthong of two weak vowels is stressed on the second
            found.append(group.end() - 1)

    return found
