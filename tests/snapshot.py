"""Records what a Verse answers today, so that a change to how it is computed
shows up as a diff rather than as a silent movement."""

import contextlib
import io
import json
from pathlib import Path
from typing import Dict, List

from pyverse import Pyverse

from corpus import verses

SNAPSHOT_PATH = Path(__file__).with_name("snapshot.json")


def record() -> List[Dict[str, object]]:
    recorded = []

    for verse in verses():
        with contextlib.redirect_stdout(io.StringIO()):
            #  The triphthong handler writes to standard output.
            pyverse = Pyverse(verse)

        recorded.append(
            {
                "verse": verse,
                "syllables": pyverse.syllables,
                "count": pyverse.count,
                "synalephas": list(pyverse.synalephas),
                "consonant_rhyme": pyverse.consonant_rhyme,
                "assonant_rhyme": pyverse.assonant_rhyme,
            }
        )

    return recorded


def load() -> List[Dict[str, object]]:
    return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))


def write() -> None:
    SNAPSHOT_PATH.write_text(
        json.dumps(record(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    write()
