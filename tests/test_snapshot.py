import snapshot


class TestSnapshot:
    def test_every_verse_answers_what_it_did(self):
        recorded = {entry["verse"]: entry for entry in snapshot.load()}
        current = {entry["verse"]: entry for entry in snapshot.record()}

        assert current.keys() == recorded.keys()

        moved = {
            verse: (recorded[verse], entry)
            for verse, entry in current.items()
            if entry != recorded[verse]
        }
        assert not moved
