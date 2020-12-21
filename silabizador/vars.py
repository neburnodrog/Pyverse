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
    "atonic_words",
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
translation_table = str.maketrans({letter: "" for letter in vowels})
consonants = string.ascii_letters.translate(translation_table) + "ñÑ"

# Atonic monosyllables -> If the vowels are accented they are tonic -> "tú" vs "tu"
personal_pronouns_indirect = ['me', 'te', 'se', 'lo', 'los', 'la', 'las', 'le', 'les', 'nos', 'os']
articles = ['el', 'la', 'lo', 'los', 'las']
possessivs = ["mi", "tu", "su"]
relatives = ['que', 'quien', 'donde', 'como', 'cuando', 'cuanto']
conjunctions = [
    'y', 'e', 'ni', 'o', 'u','pero',
    'aunque', 'mas', 'sino', 'bien',
    'ya', 'sea', 'ora', 'pues', 'porque',
    'si', 'mientras', 'apenas',
]

atonic_words = personal_pronouns_indirect + articles + possessivs + relatives + conjunctions
