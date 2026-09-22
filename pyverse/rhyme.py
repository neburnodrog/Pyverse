import re
from dataclasses import dataclass
from typing import Tuple

from pyverse.vars import (
    accented_vowels,
    strong_vowels,
    trans_accented_vowels,
    vowels,
)


@dataclass(frozen=True)
class Rhyme:
    """The rhymes of a word, counted from its last stressed vowel.

    Accents are stripped: they carry no rhyming information and would
    otherwise duplicate entries for the same rhyme.
    Ex: '-al-ga-ra-bí-a' -> consonant 'ia', assonant 'ia'
    """

    consonant: str
    assonant: str


def rhyme(syllabified: str, accentuation: int) -> Rhyme:
    """syllabified is a hyphen-separated word ('-por-que').
    accentuation counts syllables from the end, 1 being oxytone."""

    stressed_syllable, rest = _chop(_rhyme_block(syllabified, accentuation))
    from_stressed_vowel = _from_last_stressed_vowel(stressed_syllable, rest)
    consonant = from_stressed_vowel.translate(trans_accented_vowels) + rest
    return Rhyme(consonant=consonant, assonant=_assonant(consonant))


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


def _assonant(consonant_rhyme: str) -> str:
    if match := re.search("[gq]u[éeíi]", consonant_rhyme):
        #  The 'u' of que/qui/gue/gui is silent. 'ü' is not, and does not match here.
        sub = match.group().replace("u", "")
        consonant_rhyme = consonant_rhyme.replace(match.group(), sub)

    return "".join(letter for letter in consonant_rhyme if letter in vowels)
