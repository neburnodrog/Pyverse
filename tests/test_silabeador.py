import pytest

from pyverse.silabeador import (
    Word,
    Sentence,
    Pyverse,
)


#  TESTING Word-Class
class TestVowelBlockSeparator:
    def test_vowel_block_separator(self):
        """ ins-tru-men-to -> CCC(rl)V -> CC-C(rl)V """
        assert Word.vowel_block_separator("nstru") == "ns-tru"

    def test_vowel_block_separator2(self):
        """ des-tro-zar -> CC(rl)V -> C-C(rl)V """
        assert Word.vowel_block_separator("stro") == "s-tro"

    def test_vowel_block_separator3(self):
        """ o-pro-bio -> C(rl)V -> -C(rl)V """
        assert Word.vowel_block_separator("pro") == "-pro"

    def test_vowel_block_separator3_1(self):
        """ is-ra-el -> (sn)(rl)V -> C-CV """
        assert Word.vowel_block_separator("sra") == "s-ra"

    def test_vowel_block_separator3_2(self):
        """ is-la -> (sn)(rl)V -> C-CV """
        assert Word.vowel_block_separator("sla") == "s-la"

    def test_vowel_block_separator3_3(self):
        """ in-ri -> (sn)(rl)V -> C-CV """
        assert Word.vowel_block_separator("nri") == "n-ri"

    def test_vowel_block_separator3_4(self):
        """ an-le-ga-do -> (sn)(rl)V -> C-CV """
        assert Word.vowel_block_separator("nle") == "n-le"

    def test_vowel_block_separator3_5(self):
        """ car-los  -> (r)(l)V -> C-CV """
        assert Word.vowel_block_separator("rlo") == "r-lo"

    def test_vowel_block_separator4(self):
        """ gangs-ter -> CCCCV -> CCC-CV """
        assert Word.vowel_block_separator("ngste") == "ngs-te"

    def test_vowel_block_separator5(self):
        """ ist-mo -> CCCV -> CC-CV """
        assert Word.vowel_block_separator("stmo") == "st-mo"

    def test_vowel_block_separator6(self):
        """ as-ca-zo -> CCV -> C-CV """
        assert Word.vowel_block_separator("sca") == "s-ca"

    def test_vowel_block_separator7(self):
        """ ahínco """
        assert Word.vowel_block_separator("hí") == "-hí"

    def test_vowel_block_separator8(self):
        """ ahínco """
        assert Word.vowel_block_separator("í") == "-í"

    def test_vowel_block_separator9(self):
        """ special case -> achicoria """
        assert Word.vowel_block_separator("chi") == "-chi"


class TestDiphthongsFinder:
    def test_diphthongs_finder1(self):
        """ weak/strong -> especias """
        assert Word.diphthong_finder("i-a") == "ia"

    def test_diphthongs_finder2(self):
        """ weak_special/strong -> agüero """
        assert Word.diphthong_finder("ü-e") == "üe"

    def test_diphthongs_finder3(self):
        """ weak/weak -> ciudad """
        assert Word.diphthong_finder("i-u") == "iu"

    def test_diphthongs_finder4(self):
        """ weak/weak_accented -> muerciélago """
        assert Word.diphthong_finder("i-é") == "ié"

    def test_diphthongs_finder5(self):
        """ weak/aitch/weak -> prohibir """
        assert Word.diphthong_finder("o-hi") == "ohi"

    def test_diphthongs_finder6(self):
        """ strong/weak -> aire """
        assert Word.diphthong_finder("a-i") == "ai"

    def test_diphthongs_finder7(self):
        """ strong_accented/weak -> náutico """
        assert Word.diphthong_finder("á-u") == "áu"

    def test_diphthongs_finder8(self):
        """ same -> leer, chiita, zoológico """
        assert Word.diphthong_finder("e-e") == "e-e"
        assert Word.diphthong_finder("i-i") == "i-i"
        assert Word.diphthong_finder("A-ha") == "A-ha"
        assert Word.diphthong_finder("o-ho") == "o-ho"

    def test_diphthongs_finder9(self):
        """ strong/strong -> fea """
        assert Word.diphthong_finder("e-a") == "e-a"
        assert Word.diphthong_finder("e-o") == "e-o"
        assert Word.diphthong_finder("e-a") == "e-a"
        assert Word.diphthong_finder("o-ó") == "o-ó"

    def test_diphthongs_finder10(self):
        """ strong/weak_accented -> país """
        assert Word.diphthong_finder("a-í") == "a-í"
        assert Word.diphthong_finder("a-ú") == "a-ú"

    def test_diphthongs_finder11(self):
        """ weak_accented/strong -> sonríe """
        assert Word.diphthong_finder("í-e") == "í-e"
        assert Word.diphthong_finder("ú-a") == "ú-a"

    # def test_diphthongs_finde12(self):
    #     """ tripthongs """



class TestPreSyllabify:
    def test_pre_syllabify1(self):
        """Hiatus with 'h' inbetween vowels"""
        word = Word("ahínco")
        assert word.pre_syllabify() == "-a-hín-co"

    def test_pre_syllabify2(self):
        """Diphthongs still omited """
        word = Word("áureo")
        assert word.pre_syllabify() == "-á-u-re-o"

    def test_pre_syllabify3(self):
        word = Word("muerte")
        assert word.pre_syllabify() == "-mu-er-te"

    def test_pre_syllabify4(self):
        word = Word("melopea")
        assert word.pre_syllabify() == "-me-lo-pe-a"


class TestFurtherScans:
    def test_further_scans_1(self):
        word = Word("ahínco")
        assert word.syllabify_word() == "-a-hín-co"

    def test_further_scans_2(self):
        word = Word("molestias")
        assert word.syllabify_word() == "-mo-les-tias"


class TestAccentuationFinder:
    def test_accentuation_finder1(self):
        assert Word.accentuation_finder("-al-bo") == 2

    def test_accentuation_finder2(self):
        assert Word.accentuation_finder("-com-pro-me-ti-do") == 2

    def test_accentuation_finder3(self):
        assert Word.accentuation_finder("-lla-no") == 2

    def test_accentuation_finder4(self):
        assert Word.accentuation_finder("-lá-piz") == 2

    def test_accentuation_finder5(self):
        assert Word.accentuation_finder("-pa-ran") == 2

    def test_accentuation_finder6(self):
        assert Word.accentuation_finder("-ca-sas") == 2

    def test_accentuation_finder7(self):
        assert Word.accentuation_finder("-don-de") == 2

    def test_accentuation_finder8(self):
        assert Word.accentuation_finder("-es-tu-pen-dí-si-ma-men-te") == 2

    def test_accentuation_finder9(self):
        assert Word.accentuation_finder("-pro-pón-ga-me-lo") == 4

    def test_accentuation_finder10(self):
        assert Word.accentuation_finder("es-drú-ju-la") == 3

    def test_accentuation_finder11(self):
        assert Word.accentuation_finder("-ta-piz") == 1

    def test_accentuation_finder12(self):
        assert Word.accentuation_finder("-ma-ná") == 1


class TestFindStressedVowel:
    def test_find_stressed_vowel1(self):
        word = Word("huida")
        assert word.consonant_rhyme == "ida"


class TestWord:
    def test_init1(self):
        word = Word("¡.,+'onomatopeya...!")
        assert word.word_syllabified == "-o-no-ma-to-pe-ya"

    def test_init2(self):
        word = Word("¡.,+'hierático...!")
        assert word.word_syllabified == "-hie-rá-ti-co"

    def test_init3(self):
        word = Word("¡.,+'melopea...!")
        assert word.word_syllabified == "-me-lo-pe-a"

    def test_init4(self):
        word = Word("¡.,+'alcohol...!")
        assert word.word_syllabified == "-al-co-hol"

    def test_init5(self):
        word = Word("y")
        assert word.word_syllabified == "-y"

    def test_init6(self):
        word = Word("¡.,+'esternohioideo...!")
        assert word.word_syllabified == "-es-ter-no-hioi-de-o"

    def test_init7(self):
        word = Word("¡.,+'radioautografía...!")
        assert word.word_syllabified == "-ra-dioau-to-gra-fí-a"

    def test_init8(self):
        word = Word("¡.,+'glacioeustatismo...!")
        assert word.word_syllabified == "-gla-cioeus-ta-tis-mo"

    def test_repr(self):
        word = Word("hierático.")
        assert word.__repr__() == "<Word: '-hie-rá-ti-co'>"


# TESTING Sentence-Class
class TestStripHyphen:
    """Only a word after a word that ends in vowel become input to this method"""

    def test_strip_hyphen(self):
        sentence = Sentence("El arma azul")
        assert sentence.syllabified_words_punctuation == ["-El", "-ar-ma", "-a-zul"]
        assert sentence.strip_hyphen(sentence.word_objects[2]) == 1

    def test_strip_hyphen2(self):
        sentence = Sentence("El alma aire")
        assert sentence.syllabified_words_punctuation == ["-El", "-al-ma", "-ai-re"]
        assert sentence.strip_hyphen(sentence.word_objects[2]) == 0

    def test_strip_hyphen3(self):
        sentence = Sentence("Que la muerte y")
        assert sentence.syllabified_words_punctuation == [
            "-Que",
            "-la",
            "-muer-te",
            "-y",
        ]
        assert sentence.strip_hyphen(sentence.word_objects[3]) == 1
        assert sentence.syllabified_sentence == "-Que -la -muer-te y"

    def test_strip_hyphen4(self):
        sentence = Sentence("La hiena hiede")
        assert sentence.syllabified_words_punctuation == ["-La", "-hie-na", "-hie-de"]
        assert sentence.strip_hyphen(sentence.word_objects[2]) == 0
        assert sentence.syllabified_sentence == "-La -hie-na -hie-de"

    def test_strip_hyphen5(self):
        sentence = Sentence("Que haya Ariadnas nada cambia.")
        assert sentence.syllabified_words_punctuation == [
            "-Que",
            "-ha-ya",
            "-A-riad-nas",
            "-na-da",
            "-cam-bia.",
        ]
        assert sentence.strip_hyphen(sentence.word_objects[2]) == 1
        assert (
            sentence.syllabified_sentence == "-Que -ha-ya A-riad-nas -na-da -cam-bia."
        )


class TestSentence:
    sentence3 = Sentence(
        "El augusta ánima canta y baila antes de cada alimaña en el camino"
    )

    def test_words_punctuation(self):
        result = [
            "-El",
            "-au-gus-ta",
            "-á-ni-ma",
            "-can-ta",
            "-y",
            "-bai-la",
            "-an-tes",
            "-de",
            "-ca-da",
            "-a-li-ma-ña",
            "-en",
            "-el",
            "-ca-mi-no",
        ]
        assert self.sentence3.syllabified_words_punctuation == result

    def test_sentence1(self):
        sentence = Sentence("Las musas se despiertan.")
        assert sentence.syllabified_words_punctuation == [
            "-Las",
            "-mu-sas",
            "-se",
            "-des-pier-tan.",
        ]
        assert sentence.syllabified_sentence == "-Las -mu-sas -se -des-pier-tan."

    def test_sentence3(self):
        sentence = Sentence("Los ahíncos del aire albo, alzaban el vuelo.")
        assert sentence.syllabified_words_punctuation == [
            "-Los",
            "-a-hín-cos",
            "-del",
            "-ai-re",
            "-al-bo,",
            "-al-za-ban",
            "-el",
            "-vue-lo.",
        ]

    def test_sentence4(self):
        sentence = Sentence("Los ahíncos del aire albo, alzaban el vuelo.")
        assert (
            sentence.syllabified_sentence == "-Los -a-hín-cos -del "
                                             "-ai-re -al-bo, "
                                             "-al-za-ban -el -vue-lo."
        )

    def test_sentence5(self):
        text = "Las cornisas de la brisa se inventaron el asco de Carlos."

        resultado = "-Las -cor-ni-sas -de -la -bri-sa -se " \
                    "in-ven-ta-ron -el -as-co -de -Car-los."

        sentence = Sentence(text)
        assert sentence.syllabified_sentence == resultado

    def test_repr(self):
        assert (
            self.sentence3.__repr__() == "<Sentence: "
                                         "El augusta ánima canta y baila "
                                         "antes de cada alimaña [...]>"
        )

    def test_repr2(self):
        sentence = Sentence("El gozne de la puerta aliena la tuerca del frigorífico")
        assert (
            sentence.__repr__() == "<Sentence: "
                                   "El gozne de la puerta aliena "
                                   "la tuerca del frigorífico>"
        )


# TESTING Class-Silabizador
class TestSilabizador:
    verse = Pyverse("Que haya Ariadnas nada cambia.")
    verse2 = Pyverse(
        "el augusta ánima canta y baila antes de cada alimaña en el camino"
    )
    verse3 = Pyverse("la muerte estaba murmurándome bien.")
    verse4 = Pyverse("Las cornisas de la brisa se inventaron el asco de Carlos")
    verse5 = Pyverse("Estamos en el mundo y")
    verse6 = Pyverse("Las manzanas y los arbustos porque...")

    def test_counter1(self):
        assert self.verse.counter() == 9

    def test_counter2(self):
        assert self.verse2.counter() == 23

    def test_counter3(self):
        assert self.verse3.counter() == 12

    def test_counter4(self):
        assert self.verse5.counter() == 7

    def test_repr(self):
        assert (
            self.verse.__repr__() == "<Verse: "
                                     "'-Que -ha-ya A-riad-nas -na-da -cam-bia.', "
                                     "Syllables: 9>"
        )

    def test_repr2(self):
        assert (
            self.verse4.__repr__() == "<Verse: "
                                      "'-Las -cor-ni-sas -de -la -bri-sa "
                                      "-se in-ven-ta-ron [...]', "
                                      "Syllables: 18>"
        )

    def test_repr3(self):
        assert (
            self.verse3.__repr__() == "<Verse: "
                                      "'-la -muer-te es-ta-ba -mur-mu-rán-do-me -bien.', "
                                      "Syllables: 12>"
        )

    def test_repr4(self):
        verse = Pyverse("Los mentecatos comían manzanas todos juntos")
        assert (
            verse.__repr__() == "<Verse: "
                                "'-Los -men-te-ca-tos -co-mí-an "
                                "-man-za-nas -to-dos -jun-tos', "
                                "Syllables: 15>"
        )

    def test_verse_type(self):
        assert self.verse.type_verse() == {
            "is_beg": True,
            "is_int": False,
            "is_end": True,
        }

    def test_verse_type2(self):
        assert self.verse2.type_verse() == {
            "is_beg": False,
            "is_int": True,
            "is_end": False,
        }

    def test_verse_type3(self):
        assert self.verse3.type_verse() == {
            "is_beg": False,
            "is_int": False,
            "is_end": True,
        }

    def test_verse_type4(self):
        assert self.verse4.type_verse() == {
            "is_beg": True,
            "is_int": False,
            "is_end": False,
        }

    def test_verse_type5(self):
        assert self.verse6.type_verse() == {
            "is_beg": True,
            "is_int": False,
            "is_end": False,
        }

    def test_verse_consonant_rhyme_finder1(self):
        # 'cambia'
        assert self.verse.verse_consonant_rhyme_finder() == "ambia"

    def test_verse_consonant_rhyme_finder2(self):
        # 'camino'
        assert self.verse2.verse_consonant_rhyme_finder() == "ino"

    def test_verse_consonant_rhyme_finder3(self):
        # 'bien'
        assert self.verse3.verse_consonant_rhyme_finder() == "en"

    def test_verse_consonant_rhyme_finder4(self):
        # 'mundo y'
        assert self.verse5.verse_consonant_rhyme_finder() == "i"

    def test_verse_consonant_rhyme_finder5(self):
        # 'porque'
        assert self.verse6.verse_consonant_rhyme_finder() == "orque"

    def test_verse_consonant_rhyme_finder6(self):
        verse = Pyverse("Eran los monjes esdrújulos con")
        assert verse.verse_consonant_rhyme_finder() == "on"

    def test_verse_consonant_rhyme_finder7(self):
        verse = Pyverse("El ánima atraviesa mi")
        assert verse.verse_consonant_rhyme_finder() == "i"


class TestOther:
    def test_1(self):
        sil = Pyverse("Las mñnas son de miedo")
        assert sil.syllables == "-Las -mñ-nas -son -de -mie-do"

    def test_2(self):
        sil = Pyverse("asdf")
        assert(sil.syllables == "-asdf")

    def test_3(self):
        sil = Pyverse("1234")
        assert(sil.syllables == '-mil -dos-cien-tos -trein-ta y -cua-tro')

    def test_4(self):
        sil = Pyverse("mil 1000")
        assert(sil.syllables == "-mil -mil")

    def test_5(self):
        with pytest.raises(Exception):
            Pyverse(1234)

    def test_6(self):
        with pytest.raises(Exception):
            Pyverse("123asd")
