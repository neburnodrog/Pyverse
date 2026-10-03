from dataclasses import dataclass
from typing import Tuple

from pyverse.vars import punctuation


@dataclass(frozen=True)
class Syllabification:
    """A word's syllable division, with the punctuation it was written with
    held apart from the syllables.

    '¿antigua?' -> syllables ('an', 'ti', 'gua'), prefix '¿', suffix '?'
    """

    syllables: Tuple[str, ...]
    prefix: str = ""
    suffix: str = ""

    def __len__(self) -> int:
        return len(self.syllables)

    def render(self, leading_hyphen: bool = True, with_punctuation: bool = True) -> str:
        """The hyphen form. The leading hyphen is what a synalepha removes."""

        body = "-".join(self.syllables)

        if body and leading_hyphen:
            body = "-" + body

        if not with_punctuation:
            return body

        return self.prefix + body + self.suffix

    @classmethod
    def parse(cls, syllabified: str, token: str) -> "Syllabification":
        """syllabified is the hyphen form of the token's letters ('-por-que').
        token is the word as it was written, punctuation included."""

        letters = token.strip(punctuation + " ")

        if not letters:
            return cls(syllables=(), prefix=token)

        start = token.index(letters)

        return cls(
            syllables=tuple(syllabified.lstrip("-").split("-")),
            prefix=token[:start],
            suffix=token[start + len(letters):],
        )
