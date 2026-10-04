"""Records what a Verse answers today, so that a change to how it is computed
shows up as a diff rather than as a silent movement."""

import json
from pathlib import Path
from typing import Dict, List

from pyverse import Pyverse

from tests.corpus import verses

SNAPSHOT_PATH = Path(__file__).with_name("snapshot.json")


def record() -> List[Dict[str, object]]:
    recorded = []

    for verse in verses():
        pyverse = Pyverse(verse)

        recorded.append(
            {
                "verse": verse,
                "syllables": pyverse.syllables,
                "count": pyverse.count,
                "synalephas": list(pyverse.synalephas),
                "consonant_rhyme": pyverse.consonant_rhyme,
                "consonant_rhyme_yeismo": pyverse.consonant_rhyme_yeismo,
                "assonant_rhyme": pyverse.assonant_rhyme,
                "assonant_rhyme_strict": pyverse.assonant_rhyme_strict,
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
    #  python -m tests.snapshot
    write()
