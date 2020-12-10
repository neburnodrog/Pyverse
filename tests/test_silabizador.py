from silabizador.silabizador import (
    Word
)


#  TESTING Word-Class
class TestVowelBlockSeparator:
    def test_vowel_block_separator(self):
        """ ins-tru-men-to -> CCC(rl)V -> CC-C(rl)V """
        assert (Word.vowel_block_separator("nstru") == "ns-tru")

    def test_vowel_block_separator2(self):
        """ des-tro-zar -> CC(rl)V -> C-C(rl)V """
        assert (Word.vowel_block_separator("stro") == "s-tro")

    def test_vowel_block_separator3(self):
        """ o-pro-bio -> C(rl)V -> -C(rl)V """
        assert (Word.vowel_block_separator("pro") == "-pro")

    def test_vowel_block_separator4(self):
        """ gangs-ter -> CCCCV -> CCC-CV """
        assert (Word.vowel_block_separator("ngste") == "ngs-te")

    def test_vowel_block_separator5(self):
        """ ist-mo -> CCCV -> CC-CV """
        assert (Word.vowel_block_separator("stmo") == "st-mo")

    def test_vowel_block_separator6(self):
        """ is-ra-el -> CCV -> C-CV """
        assert (Word.vowel_block_separator("sra") == "s-ra")

    def test_vowel_block_separator7(self):
        """ ahínco """
        assert (Word.vowel_block_separator("hí") == "-hí")

    def test_vowel_block_separator8(self):
        """ ahínco """
        assert (Word.vowel_block_separator("í") == "-í")

    def test_vowel_block_separator9(self):
        """ special case -> achicoria """
        assert (Word.vowel_block_separator("chi") == "-chi")


class TestDiphthongsFinder:
    def test_diphthongs_finder1(self):
        """ weak/strong -> especias """
        assert (Word.diphthong_finder("i-a") == "ia")

    def test_diphthongs_finder2(self):
        """ weak_special/strong -> agüero """
        assert (Word.diphthong_finder("ü-e") == "üe")

    def test_diphthongs_finder3(self):
        """ weak/weak -> ciudad """
        assert (Word.diphthong_finder("i-u") == "iu")

    def test_diphthongs_finder4(self):
        """ weak/weak_accented -> muerciélago """
        assert (Word.diphthong_finder("i-é") == "ié")

    def test_diphthongs_finder5(self):
        """ weak/aitch/weak -> prohibir """
        assert (Word.diphthong_finder("o-hi") == "ohi")

    def test_diphthongs_finder6(self):
        """ strong/weak -> aire """
        assert (Word.diphthong_finder("a-i") == "ai")

    def test_diphthongs_finder7(self):
        """ strong_accented/weak -> náutico """
        assert (Word.diphthong_finder("á-u") == "áu")

    def test_diphthongs_finder8(self):
        """ same -> leer, chiita, zoológico """
        assert (Word.diphthong_finder("e-e") == "e-e")
        assert (Word.diphthong_finder("i-i") == "i-i")
        assert (Word.diphthong_finder("A-ha") == "A-ha")
        assert (Word.diphthong_finder("o-ho") == "o-ho")

    def test_diphthongs_finder9(self):
        """ strong/strong -> fea """
        assert (Word.diphthong_finder("e-a") == "e-a")
        assert (Word.diphthong_finder("e-o") == "e-o")
        assert (Word.diphthong_finder("e-a") == "e-a")
        assert (Word.diphthong_finder("o-ó") == "o-ó")

    def test_diphthongs_finder10(self):
        """ strong/weak_accented -> país """
        assert (Word.diphthong_finder("a-í") == "a-í")
        assert (Word.diphthong_finder("a-ú") == "a-ú")

    def test_diphthongs_finder11(self):
        """ weak_accented/strong -> sonríe """
        assert (Word.diphthong_finder("í-e") == "í-e")
        assert (Word.diphthong_finder("ú-a") == "ú-a")


class TestPreSyllabify:
    def test_pre_syllabify1(self):
        """Hiatus with 'h' inbetween vowels"""
        word = Word("ahínco")
        assert (word.pre_syllabify(word.word_text) == "-a-hín-co")

    def test_pre_syllabify2(self):
        """Diphthongs still omited """
        word = Word("áureo")
        assert (word.pre_syllabify(word.word_text) == "-á-u-re-o")

    def test_pre_syllabify3(self):
        word = Word("muerte")
        assert (word.pre_syllabify(word.word_text) == "-mu-er-te")

    def test_pre_syllabify4(self):
        word = Word("melopea")
        assert (word.pre_syllabify(word.word_text) == "-me-lo-pe-a")


class TestFurtherScans:
    def test_further_scans_1(self):
        word = Word("ahínco")
        assert (word.pre_syllabified_word == "-a-hín-co")
        assert (word.further_scans("-a-hín-co") == "-a-hín-co")

    def test_further_scans_2(self):
        word = Word("molestias")
        assert (word.pre_syllabified_word == "-mo-les-ti-as")
        assert (word.further_scans(word.pre_syllabified_word) == "-mo-les-tias")


class TestWord:
    def test_init1(self):
        """ Normal word """
        word = Word("¡  .,+'onomatopeya...!")
        assert (word.syllabified_word == "-o-no-ma-to-pe-ya")

    def test_init2(self):
        """ Normal word """
        word = Word("¡  .,+'hierático...!")
        assert (word.syllabified_word == "-hie-rá-ti-co")

    def test_init3(self):
        """ Normal word """
        word = Word("¡  .,+'melopea...!")
        assert (word.syllabified_word == "-me-lo-pe-a")

    def test_init4(self):
        """ Normal word """
        word = Word("¡  .,+'alcohol...!")
        assert (word.syllabified_word == "-al-co-hol")


# TESTING Sentence-Class
# TODO
