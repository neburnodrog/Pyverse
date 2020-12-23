import string

__all__ = [
    "punctuation",
    "uppercase",
    "vowels",
    "vowels_with_h",
    "consonants",
    "weak_vowels",
    "weak_accented_vowels",
    "strong_vowels",
    "accented_vowels",
    "unaccented_vowels",
    "atonic_monosyllabic",
    "monosyllabic_words",
    "trans_accented_vowels",
]

# VARIABLES
punctuation = string.punctuation + r'¡¿—«”»'

# Letters
uppercase = string.ascii_uppercase + "ÑÁÉÍÓÚ"

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
trans_accented_vowels = str.maketrans({k: v for k, v in zip(accented_vowels, unaccented_vowels)})

# Atonic monosyllables -> If the vowels are accented they are tonic -> "tú" vs "tu"
personal_pronouns_indirect = ['me', 'te', 'se', 'lo', 'los', 'la', 'las', 'le', 'les', 'nos', 'os']
articles = ['el', 'la', 'lo', 'los', 'las']
possessivs = ["mi", "tu", "su"]
relatives = ['que', 'quien', 'como']
conjunctions = [
    'y', 'e', 'ni', 'o', 'u', 'mas', 'ya', 'pues', 'si'
]

non_monosyllabic_atonic_words = [
    'donde', 'como', 'cuando', 'cuanto',
    'aunque', 'sino', 'sea', 'ora',
    'porque', 'mientras', 'apenas'
]

atonic_monosyllabic = personal_pronouns_indirect + articles + possessivs + relatives + conjunctions

monosyllabic_words = atonic_monosyllabic + non_monosyllabic_atonic_words
