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
import argparse
from silabizador import silabizar


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = input("Enter word/verse to syllabify: ")

    sil = silabizar.Silabizador(text)
    print(sil.sentence.syllabified_sentence)


if __name__ == "__main__":
    main()
