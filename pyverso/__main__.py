"""
pyverso - Spanish syllabification algorythm

Usage:
------
pyverso as a command line tool returns 3 things:

- The syllabified verse or word specified in the TEXT argument.
- The count of the syllables.
- The assonant and consonant rhymes.

Contact:
--------
- neburnodrog@gmail.com
More information is available at:
- https://pypi.org/project/silabizador/
- https://github.com/neburnodrog/silabizador

Version:
--------
- pyverso v1.0.0
"""

import click
from .silabeador import Pyverso


@click.command()
@click.argument("text")
def silabify(text):
    """pyverso as a command line tool returns 3 things:

    \t1. The syllabified verse or word specified in the TEXT argument.\n
    \t2. The count of the syllables.\n
    \t3. The assonant and consonant rhymes."""

    verso = Pyverso(text)
    click.echo(
        f"""
        Syllabified Text | {verso.syllables}
        Count            | {verso.count}
        Consonant Rhyme  | {verso.consonant_rhyme}
        Assonant Rhyme   | {verso.assonant_rhyme}
        """
    )
