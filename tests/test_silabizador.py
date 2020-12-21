from silabizador.silabizador import (
    Word,
    Sentence,
    Silabizador,
)
from silabizador.vars import *


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
        assert (word.pre_syllabified_word == "-a-hín-co")

    def test_pre_syllabify2(self):
        """Diphthongs still omited """
        word = Word("áureo")
        assert (word.pre_syllabified_word == "-á-u-re-o")

    def test_pre_syllabify3(self):
        word = Word("muerte")
        assert (word.pre_syllabified_word == "-mu-er-te")

    def test_pre_syllabify4(self):
        word = Word("melopea")
        assert (word.pre_syllabified_word == "-me-lo-pe-a")


class TestFurtherScans:
    def test_further_scans_1(self):
        word = Word("ahínco")
        assert (word.pre_syllabified_word == "-a-hín-co")
        assert (word.further_scans("-a-hín-co") == "-a-hín-co")

    def test_further_scans_2(self):
        word = Word("molestias")
        assert (word.pre_syllabified_word == "-mo-les-ti-as")
        assert (word.further_scans(word.pre_syllabified_word) == "-mo-les-tias")


class TestAccentuationFinder:
    def test_accentuation_finder1(self):
        assert (Word.accentuation_finder("-al-bo") == 0)

    def test_accentuation_finder2(self):
        assert (Word.accentuation_finder("-com-pro-me-ti-do") == 0)

    def test_accentuation_finder3(self):
        assert (Word.accentuation_finder("-lla-no") == 0)

    def test_accentuation_finder4(self):
        assert (Word.accentuation_finder("-lá-piz") == 0)

    def test_accentuation_finder5(self):
        assert (Word.accentuation_finder("-pa-ran") == 0)

    def test_accentuation_finder6(self):
        assert (Word.accentuation_finder("-ca-sas") == 0)

    def test_accentuation_finder7(self):
        assert (Word.accentuation_finder("-don-de") == None)

    def test_accentuation_finder8(self):
        assert (Word.accentuation_finder("-es-tu-pen-dí-si-ma-men-te") == 0)

    def test_accentuation_finder9(self):
        assert (Word.accentuation_finder("-pro-pón-ga-me-lo") == -2)

    def test_accentuation_finder10(self):
        assert (Word.accentuation_finder("es-drú-ju-la") == -1)

    def test_accentuation_finder11(self):
        assert (Word.accentuation_finder("-ta-piz") == 1)

    def test_accentuation_finder12(self):
        assert (Word.accentuation_finder("-ma-ná") == 1)


class TestWord:
    def test_init1(self):
        word = Word("¡.,+'onomatopeya...!")
        assert (word.syllabified_word == "-o-no-ma-to-pe-ya")

    def test_init2(self):
        word = Word("¡.,+'hierático...!")
        assert (word.syllabified_word == "-hie-rá-ti-co")

    def test_init3(self):
        word = Word("¡.,+'melopea...!")
        assert (word.syllabified_word == "-me-lo-pe-a")

    def test_init4(self):
        word = Word("¡.,+'alcohol...!")
        assert (word.syllabified_word == "-al-co-hol")

    def test_init5(self):
        word = Word("y")
        assert (word.syllabified_word == "-y")

    def test_repr(self):
        word = Word("hierático.")
        assert (word.__repr__() == "<Word: '-hie-rá-ti-co'>")


# TESTING Sentence-Class
class TestStripHyphen:
    """Only a word after a word that ends in vowel become input to this method"""

    def test_strip_hyphen(self):
        sentence = Sentence("El arma azul")
        assert (sentence.syllabified_words_punctuation == ["-El", "-ar-ma", "-a-zul"])
        assert (sentence.strip_hyphen(sentence.word_objects[2], "a") == True)

    def test_strip_hyphen2(self):
        sentence = Sentence("El alma aire")
        assert (sentence.syllabified_words_punctuation == ["-El", "-al-ma", "-ai-re"])
        assert (sentence.strip_hyphen(sentence.word_objects[2], "a") == False)

    def test_strip_hyphen3(self):
        sentence = Sentence("Que la muerte y")
        assert (sentence.syllabified_words_punctuation == ["-Que", "-la", "-muer-te", "-y"])
        assert (sentence.strip_hyphen(sentence.word_objects[3], "e") == True)
        assert (sentence.syllabified_sentence == "-Que -la -muer-te y")

    def test_strip_hyphen4(self):
        sentence = Sentence("La hiena hiede")
        assert (sentence.syllabified_words_punctuation == ["-La", "-hie-na", "-hie-de"])
        assert (sentence.strip_hyphen(sentence.word_objects[2], "a") == False)
        assert (sentence.syllabified_sentence == "-La -hie-na -hie-de")

    def test_strip_hyphen5(self):
        sentence = Sentence("Que haya Ariadnas nada cambia.")
        assert(sentence.syllabified_words_punctuation == ["-Que", "-ha-ya", "-A-riad-nas", "-na-da", "-cam-bia."])
        assert (sentence.strip_hyphen(sentence.word_objects[2], "a") == True)
        assert (sentence.syllabified_sentence == "-Que -ha-ya A-riad-nas -na-da -cam-bia.")


class TestSentence:
    sentence = Sentence("Las musas se despiertan.")
    sentence2 = Sentence("Los ahíncos del aire albo, alzaban el vuelo.")
    sentence3 = Sentence("El augusta ánima canta y baila antes de cada alimaña en el camino")

    def test_words_punctuation(self):
        result = [
            "-El", "-au-gus-ta", "-á-ni-ma", "-can-ta",
            "-y", "-bai-la", "-an-tes", "-de", "-ca-da",
            "-a-li-ma-ña", "-en", "-el", "-ca-mi-no"
        ]
        assert (self.sentence3.syllabified_words_punctuation == result)

    def test_sentence1(self):
        assert (self.sentence.syllabified_words_punctuation == ["-Las", "-mu-sas", "-se", "-des-pier-tan."])

    def test_sentence2(self):
        assert (self.sentence.syllabified_sentence == "-Las -mu-sas -se -des-pier-tan.")

    def test_sentence3(self):
        assert (self.sentence2.syllabified_words_punctuation == ["-Los", "-a-hín-cos", "-del", "-ai-re", "-al-bo,",
                                                                 "-al-za-ban", "-el", "-vue-lo."])

    def test_sentence4(self):
        assert (self.sentence2.syllabified_sentence == "-Los -a-hín-cos -del -ai-re -al-bo, -al-za-ban -el -vue-lo.")


# TESTING Class-Silabizador
    verse = Silabizador("Que haya Ariadnas nada cambia.")
    verse2 = Silabizador("El augusta ánima canta y baila antes de cada alimaña en el camino")
    verse3 = Silabizador("La muerte estaba murmurándome bien.")

    def test_counter1(self):
        assert(self.verse.counter() == 8)

    def test_counter2(self):
        assert(self.verse2.counter() == 23)

    def test_counter3(self):
        assert(self.verse3.counter() == 12)

