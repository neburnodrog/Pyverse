import string

__all__ = [
    "punctuation",
    "letters",
    "vowels",
    "vowels_with_h",
    "consonants",
    "weak_vowels",
    "weak_accented_vowels",
    "strong_vowels",
    "accented_vowels",
    "unaccented_vowels",
    "atonic_monosyll",
    "atonic_words",
    "trans_accented_vowels",
]

# VARIABLES
punctuation = string.punctuation + r'¡¿—«”»'

# Letters
spanish_uppercase = "ÑÁÉÍÓÚÜ"
spanish_lowercase = "ñáéíóúü"
letters = string.ascii_letters + spanish_lowercase + spanish_uppercase

# Vowels
vowels = "aeiou" + "áéíóú" + "AEIOU" + "ÁÉÍÓÚ" + "üÜ"
vowels_with_h = vowels + "hH"
weak_vowels = "UIuiü"
weak_accented_vowels = "ÚÍúí"
strong_vowels = "AEOaeoÁÉÓáéó"
accented_vowels = "áéíóúÁÉÍÓÚ"
unaccented_vowels = "aeiouAEIOU"

# Consonants
trans_vowels_into_nothing = str.maketrans({letter: "" for letter in vowels})
consonants = string.ascii_letters.translate(trans_vowels_into_nothing) + "ñÑ"

# Translation Table for accented vowels
trans_accented_vowels = str.maketrans(
    {k: v for k, v in zip(accented_vowels, unaccented_vowels)}
)

# Atonic monosyllables -> If the vowels are accented they are tonic -> "tú" vs "tu"
pron_ind = [
    'me', 'te', 'se', 'lo', 'los', 'la', 'las', 'le', 'les', 'nos', 'os'
]
art = ['el', 'la', 'lo', 'los', 'las']
poss = ["mi", "tu", "su"]
rel = ['que', 'quien']
conj = [
    'y', 'e', 'ni', 'o', 'u', 'mas', 'ya', 'pues', 'si'
]
prep = ["a", "con", "de", "en", "por"]

non_monosyll_atonic = [
    'donde', 'como', 'cuando', 'cuanto',
    'aunque', 'sino', 'sea', 'ora',
    'porque', 'mientras', 'apenas'
]

atonic_monosyll = (
    pron_ind + art + poss + rel + conj + prep
)

atonic_words = atonic_monosyll + non_monosyll_atonic
