"""
pyverse - Spanish syllabification algorithm

Usage:
------
pyverse as a command line tool returns 3 things:

- The syllabified verse or word specified in the TEXT argument.
- The count of the syllables.
- The assonant and consonant rhymes.

Contact:
--------
- neburnodrog@gmail.com
More information is available at:
- https://pypi.org/project/pyverse/
- https://github.com/neburnodrog/Pyverse
"""

import click
from .silabeador import Pyverse


@click.command()
@click.argument("text")
def silabify(text):
    """pyverse as a command line tool returns 3 things:

    \t1. The syllabified verse or word specified in the TEXT argument.\n
    \t2. The count of the syllables.\n
    \t3. The assonant and consonant rhymes."""

    verso = Pyverse(text)
    click.echo(
        f"""
        Syllabified Text | {verso.syllables}
        Count            | {verso.count}
        Consonant Rhyme  | {verso.consonant_rhyme}
        Assonant Rhyme   | {verso.assonant_rhyme}
        """
    )


if __name__ == "__main__":
    silabify()
