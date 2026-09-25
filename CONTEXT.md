# Context

Pyverse syllabifies Spanish verse and counts its syllables the way the
Spanish poetic tradition does, which is not the way the RAE counts them.

## Glossary

**Verse** - one line of poetry, the unit the package takes in and answers about.
Modelled by `Pyverse`. A verse knows its syllable count, its rhymes and whether
it opens or closes a sentence. Not a "line" or a "sentence".

**Sentence** - the ordered words of a verse plus the positions where a
synalepha joins a word to the one before it. Modelled by `Sentence`. Named for
the class that exists; the concept is really "the words of one verse, joined".

**Word** - one whitespace-delimited token of a verse, carrying its punctuation.
Modelled by `Word`. A word knows its syllabification, its accentuation and its
rhyme.

**Syllable** - one beat of a word. Carried as a string in the `syllables`
tuple of a `Syllabification`.

**Syllabification** - a word's syllable division as a value. Modelled by
`Syllabification` in `pyverse/syllabification.py`, a frozen dataclass holding
the syllables plus the punctuation written before and after them. It renders
itself back to the hyphen form (`"-por-que"`), with or without the leading
hyphen, which is the hyphen a synalepha removes. Its `parse` is the one place
the hyphen form is decoded; the syllabifier still produces that form.

**Accentuation** - which syllable from the end carries the stress, as an
integer. 1 is **oxytone** (stress on the last syllable, *bergantín*), 2 is
**paroxytone** (*velero*), 3 is **proparoxytone** (*esdrújula*), 4 is
**superproparoxytone** (*propóngamelo*). The verse's syllable count is adjusted
by `2 - accentuation` of its last word.

**Synalepha** - two adjacent words pronounced as one syllable, because the
first ends in a vowel and the second begins with one. *el arma antigua* counts
as five syllables, not six. Blocked when the second word begins with an
accented vowel (*el viento ártico*), blocked for two-syllable paroxytones
(*el arma antes*), and blocked by punctuation on either side of the join
(*el arma, antigua*, *el arma ¿antigua?*). A verse's syllable count is the
syllables of its words minus its synalephas; it is not read back out of the
syllabified string.

**Atonic monosyllable** - a one-syllable word that carries no stress of its own
(*de*, *la*, *y*, *que*). A verse ending in one that formed a synalepha is
counted as if it ended in a paroxytone.

**Rhyme** - the ending of a word from its last stressed vowel, with accents
stripped. Modelled by `Rhyme` in `pyverse/rhyme.py`, which is the single place
this is derived. It has two forms:

- **Consonant rhyme** - every letter from the last stressed vowel onward.
  *algarabía* rhymes in `ia`, *porque* in `orque`.
- **Assonant rhyme** - only the vowels of the consonant rhyme. *porque* rhymes
  in `oe`, because the `u` of *que/qui/gue/gui* is silent. A `ü` is pronounced
  and stays: *averigüe* rhymes in `iüe`.

A verse's rhyme is its last word's rhyme. There is no second derivation.
