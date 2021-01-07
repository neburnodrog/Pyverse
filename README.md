[![codecov](https://img.shields.io/codecov/c/github/neburnodrog/silabizador)](https://codecov.io/gh/neburnodrog/silabizador)

# Pyverse
#### A automatic syllabification algorithm for Spanish verses written in Python

<<<<<<< HEAD
Pyverse comes from Python & Verso.
Verso beeing verse in Spanish.

=======
>>>>>>> b6c26b835e85222557c8cfc4777db1b55a37d8fb
- It separates every syllable of words and verses. It counts the syllables of verses as it's done in the spanish language poetry tradition.

### Description
  **silabizador** syllabifies words and verses taking into account [synalephas](https://en.wikipedia.org/wiki/Synalepha) and the [accentuation](https://en.wikipedia.org/wiki/Metre_(poetry)#Spanish) of the final word in the verse. 

  - The [prosodic](https://en.wikipedia.org/wiki/Prosody_(linguistics)) metre of a verse in Spanish poetry differs from the rules of syllabification specified by the [RAE](https://en.wikipedia.org/wiki/Royal_Spanish_Academy) for the counting of syllables. Depending on the accentuation of the last word of the verse we encounter different cases:

    1. If the last word is [oxytone](https://en.wikipedia.org/wiki/Oxytone), the prosodic perception will impose the addition of an extra syllable to the syllable count of the verse.
    2. If it's [paroxytone](https://en.wikipedia.org/wiki/Paroxytone) we leave as it is: we neither add nor substract a syllable to the counting.
    3. If it's [proparoxytone](https://en.wikipedia.org/wiki/Proparoxytone) we substract one syllable.
    4. If it's **superproparoxytone** we substract two.  

### Instalation
```
pip install pyverse
```
### Use
You can either use Pyverse in the command line:
```
pyverso "un velero bergantín;"

        Syllabified Text | -un -ve-le-ro -ber-ga-tín;
        Count            | 8
        Consonant Rhyme  | atin
        Assonant Rhyme   | ai
```
or as a python package
```
>>> from pyverse import Pyverse
>>> verse = Pyverse("un velero bergantín;")
>>> print(verse.get_syllables())
'-un -ve-le-ro -ber-gan-tín;'
>>> print(verse.count)
8
```
---

# Pyverse en Español
#### Un algoritmo silabeador de versos en español escrito en Python.
```
[silabear](https://dle.rae.es/silabear)
1. Ir pronunciando separadamente cada sílaba.
```

### Descripcion
Pyverse silabea palabras y versos en Español. Cuenta las sílabas a la manera de la tradición poética en lengua española. 
Es decir: tiene en cuenta sinalefas y finales de verso. 

- Según la [acentuación fonética](https://es.wikipedia.org/wiki/Acentuaci%C3%B3n_del_idioma_espa%C3%B1ol#Reglas_generales_de_acentuaci%C3%B3n) de la última palabra del verso se dan varios casos:

  1. Si la última palabra tiene una acetuación **aguda** u **oxítona**, la perceptión prosódica del verso impone que se le sume una sílaba al número de sílabas ortográficas del verso.  
  2. Si es **llana** o **paroxítona** se deja como está: ni se le resta ni se le suman sílabas al verso.
  3. Si la última palabra del verso es **esdrújula** o *proparoxítona* se le resta una sílaba al verso.
  4. Si es **superproparoxítona** o **sobresdrújula** se le restan dos sílabas al verso.
  
- [Sinalefas](https://es.wikipedia.org/wiki/Sinalefa)

  - La sinalefa es un fenómeno prosódico mediante el cual se juntan en una sola sílaba fonética la última sílaba de una palabra y la primera de la siguiente en caso de ser las dos vocales.
  
    ```
    -el -ar-ma_an-ti-gua
    -el -vien-to_a-zul
    ```
  - No se produce sinalefa si la segunda palabra empieza con vocal acentuada:
  
    ```
    -el -ar-la -á-ri-da
    -el -vien-to -ár-ti-co
    ```
- Rimas

  - El silabizador proporciona las rimas [asonante](https://es.wikipedia.org/wiki/Rima_asonante) y [consonantes](https://es.wikipedia.org/wiki/Rima_consonante) tanto de palabras como de versos

### Instalación
```
pip install Pyverse
```

### Uso
puedes usar Pyverse desde el terminal:
```
pyverso "un velero bergantín;"

        Syllabified Text | -un -ve-le-ro -ber-ga-tín;
        Count            | 8
        Consonant Rhyme  | atin
        Assonant Rhyme   | ai
```
o como una librería de Python
```
>>> from pyverse import Pyverse
>>> verse = Pyverse("un velero bergantín;")
>>> print(verse.get_syllables())
'-un -ve-le-ro -ber-gan-tín;'
>>> print(verse.count)
8
```
