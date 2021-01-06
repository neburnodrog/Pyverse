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

import sys
import click
from .silabeador import Pyverso


@click.command()
@click.argument("text")
def silabify(text):
    """pyverso as a command line tool returns 3 things:

    \t1. The syllabified verse or word specified in the TEXT argument.\n
    \t2. The count of the syllables.\n
    \t3. The assonant and consonant rhymes."""

    silabiz = Pyverso(text)
    click.echo(
        f"""
        Syllabified Text | {silabiz.get_syllables()}
        Count            | {silabiz.count}
        Consonant Rhyme  | {silabiz.consonant_rhyme}
        Assonant Rhyme   | {silabiz.assonant_rhyme}
        """
    )
