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
    "unaccented_vowels"
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
unaccented_vowels = "aeiouAEIOU2"

# Consonants
translation_table = str.maketrans({letter: "" for letter in vowels})
consonants = string.ascii_letters.translate(translation_table) + "ñÑ"
