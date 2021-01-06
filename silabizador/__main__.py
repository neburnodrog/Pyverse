"""
silabizador - Spanish syllabification algorythm

Usage:
------


Contact:
--------
- neburnodrog@gmail.com
More information is available at:
- https://pypi.org/project/silabizador/
- https://github.com/neburnodrog/silabizador

Version:
--------
- silabizador v1.0.0
"""

import sys
import click
from .silabizar import Silabizador


@click.command()
@click.argument("text")
@click.option(
    "--v",
    default=0,
    help="0: Only get syllabified text\n1: Also Syllable Count\n2: Also Rhymes",
)
def silabify(text, v):
    """silabizador as a CLI is only capable of returning a syllabified spanish sentence or word.


    It has three possible"""

    try:
        verbosity = int(v)
    except ValueError:
        raise ValueError("Only digits allowed as parameters to the --v option")

    if verbosity == 0:
        silabiz = Silabizador(text)
        click.echo(silabiz.get_syllables())

    elif verbosity == 1:
        silabiz = Silabizador(text)
        click.echo(
            f"""{silabiz.get_syllables()}
            Count: {silabiz.count}
            """
        )

    elif verbosity == 2:
        silabiz = Silabizador(text)
        click.echo(
            f"""{silabiz.get_syllables()}
            Count: {silabiz.count}
            Consonant Rhyme: {silabiz.consonant_rhyme}
            Assonant Rhyme: {silabiz.assonant_rhyme}
            """
        )

    else:
        print("Only values 0, 1 or 2 allowed", file=sys.stderr)
