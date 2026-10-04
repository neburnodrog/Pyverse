import pytest
from click.testing import CliRunner

from pyverse import PyverseError
from pyverse.__main__ import silabify


@pytest.fixture
def run():
    runner = CliRunner()

    def _run(*args):
        return runner.invoke(silabify, list(args))

    return _run


class TestCli:
    def test_reports_all_four_fields(self, run):
        result = run("un velero bergantín;")
        assert result.exit_code == 0
        assert "Syllabified Text | -un -ve-le-ro -ber-gan-tín;" in result.output
        assert "Count            | 8" in result.output
        assert "Consonant Rhyme  | in" in result.output
        assert "Assonant Rhyme   | i" in result.output

    def test_silent_u_reaches_the_output(self, run):
        """The 'u' of 'que' is silent -> 'oe', not 'oue'."""
        assert "Assonant Rhyme   | oe" in run("Las manzanas y los arbustos porque").output

    def test_dieresis_u_reaches_the_output(self, run):
        assert "Assonant Rhyme   | ie" in run("No sé qué averigüe").output

    def test_expands_digits(self, run):
        assert "-mil -dos-cien-tos -trein-ta y -cua-tro" in run("1234").output

    def test_rejects_mixed_letters_and_digits(self, run):
        result = run("123asd")
        assert result.exit_code != 0
        assert isinstance(result.exception, PyverseError)

    def test_requires_the_text_argument(self, run):
        assert run().exit_code != 0

    def test_does_not_write_anything_else_to_stdout(self, run):
        """The syllabifier must not leak its workings into the report."""
        result = run("un velero bergantín;")
        body = [line for line in result.output.splitlines() if line.strip()]
        assert len(body) == 4

    def test_a_triphthong_does_not_leak_into_the_report(self, run):
        result = run("esternohioideo")
        body = [line for line in result.output.splitlines() if line.strip()]
        assert len(body) == 4
        assert "-es-ter-no-hioi-de-o" in result.output
