import pytest

from pyverse.syllabification import Syllabification


class TestParse:
    def test_splits_the_hyphen_form_into_syllables(self):
        assert Syllabification.parse("-por-que", "porque").syllables == ("por", "que")

    def test_holds_punctuation_apart_from_the_syllables(self):
        syllabification = Syllabification.parse("-an-ti-gua", "¿antigua?")
        assert syllabification.syllables == ("an", "ti", "gua")
        assert syllabification.prefix == "¿"
        assert syllabification.suffix == "?"

    def test_no_punctuation_leaves_both_sides_empty(self):
        syllabification = Syllabification.parse("-al-ma", "alma")
        assert syllabification.prefix == ""
        assert syllabification.suffix == ""

    def test_a_token_without_letters_has_no_syllables(self):
        syllabification = Syllabification.parse("-", "...")
        assert syllabification.syllables == ()
        assert syllabification.prefix == "..."

    def test_keeps_the_case_of_the_token(self):
        assert Syllabification.parse("-El", "El").syllables == ("El",)


class TestLength:
    def test_length_is_the_syllable_count(self):
        assert len(Syllabification.parse("-a-li-ma-ña", "alimaña")) == 4

    def test_a_monosyllable_is_one(self):
        assert len(Syllabification.parse("-y", "y")) == 1

    def test_a_token_without_letters_is_zero(self):
        assert len(Syllabification.parse("-", "¡")) == 0


class TestRender:
    def test_round_trips_the_hyphen_form(self):
        for syllabified, token in [
            ("-por-que", "porque"),
            ("-a-ve-ri-güe", "averigüe"),
            ("-y", "y"),
        ]:
            assert Syllabification.parse(syllabified, token).render() == syllabified

    def test_keeps_the_punctuation_where_it_was_written(self):
        for syllabified, token, rendered in [
            ("-an-ti-gua", "¿antigua?", "¿-an-ti-gua?"),
            ("-al-bo", "albo,", "-al-bo,"),
            ("-o-no-ma-to-pe-ya", "¡.,+'onomatopeya...!", "¡.,+'-o-no-ma-to-pe-ya...!"),
        ]:
            assert Syllabification.parse(syllabified, token).render() == rendered

    def test_without_the_leading_hyphen(self):
        syllabification = Syllabification.parse("-an-ti-gua", "antigua")
        assert syllabification.render(leading_hyphen=False) == "an-ti-gua"

    def test_drops_the_leading_hyphen_even_behind_punctuation(self):
        """The defect lstrip('-') could not fix: the hyphen is not leading."""
        syllabification = Syllabification.parse("-an-ti-gua", "¿antigua?")
        assert syllabification.render(leading_hyphen=False) == "¿an-ti-gua?"

    def test_without_punctuation(self):
        syllabification = Syllabification.parse("-an-ti-gua", "¿antigua?")
        assert syllabification.render(with_punctuation=False) == "-an-ti-gua"

    def test_a_token_without_letters_renders_as_itself(self):
        assert Syllabification.parse("-", "...").render() == "..."


class TestImmutability:
    def test_cannot_be_edited(self):
        syllabification = Syllabification.parse("-al-ma", "alma")
        with pytest.raises(Exception):
            syllabification.syllables = ("o",)
