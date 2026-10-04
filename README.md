[![codecov](https://img.shields.io/codecov/c/github/neburnodrog/Pyverse)](https://codecov.io/gh/neburnodrog/Pyverse)

# Pyverse
#### A automatic syllabification algorithm for Spanish verses written in Python

Python + Verse = Pyverse.

=======

- It separates every syllable of words and verses. It counts the syllables of verses as it's done in the spanish language poetry tradition.

### Description
  **silabizador** syllabifies words and verses taking into account [synalephas](https://en.wikipedia.org/wiki/Synalepha) and the [accentuation](https://en.wikipedia.org/wiki/Metre_(poetry)#Spanish) of the final word in the verse.

  - A synalepha joins two adjacent words into one syllable when the first ends in a vowel and the second begins with one. It is blocked when the second word begins with an accented vowel, when the second word is a two-syllable paroxytone, and when punctuation falls between the two words, whichever side of the join it sits on.


  - The [prosodic](https://en.wikipedia.org/wiki/Prosody_(linguistics)) metre of a verse in Spanish poetry differs from the rules of syllabification specified by the [RAE](https://en.wikipedia.org/wiki/Royal_Spanish_Academy) for the counting of syllables. Depending on the accentuation of the last word of the verse we encounter different cases:

    1. If the last word is [oxytone](https://en.wikipedia.org/wiki/Oxytone), the prosodic perception will impose the addition of an extra syllable to the syllable count of the verse.
    2. If it's [paroxytone](https://en.wikipedia.org/wiki/Paroxytone) we leave as it is: we neither add nor substract a syllable to the counting.
    3. If it's [proparoxytone](https://en.wikipedia.org/wiki/Proparoxytone) we substract one syllable.
    4. If it's **superproparoxytone** we substract two.  

  - A verse rhymes on its last word, counting from that word's last stressed
    vowel. Every rhyme is lowercase and carries no accents, so that two words
    that rhyme always give the same string.

    1. The **consonant rhyme** is every letter from the last stressed vowel
       onward: *algarabía* rhymes in `ia`, *porque* in `orque`.
    2. The **assonant rhyme** is the stressed vowel followed by the last
       vowel, and nothing in between: *lánguida* rhymes in `aa`, *baile* in
       `ae`, *rey* in `e`.
    3. Assonance comes in two readings. The default one is loose, where a
       final unstressed `i` is read as `e` and a final unstressed `u` as `o`
       (Quilis, *Métrica española*), so *Venus* rhymes in `eo` with *cielo*.
       The strict one takes the final vowel as written, so *Venus* rhymes in
       `eu`. The stressed vowel is never remapped.
    4. The **yeísmo** consonant rhyme reads `ll` as `y`, so *playa* and
       *falla* both rhyme in `aya`.

  - Input the package cannot read as a verse raises `PyverseError`, which
    subclasses `ValueError`.

### Installation
Requires Python 3.12 or newer.
```
pip install pyverse
```
### Use
You can either use Pyverse in the command line:
```
pyverse "un velero bergantín;"

        Syllabified Text | -un -ve-le-ro -ber-gan-tín;
        Count            | 8
        Consonant Rhyme  | in
        Assonant Rhyme   | i
```
or as a python package
```
>>> from pyverse import Pyverse
>>> verse = Pyverse("un velero bergantín;")
>>> verse.syllables
'-un -ve-le-ro -ber-gan-tín;'
>>> verse.count
8
>>> verse.consonant_rhyme, verse.assonant_rhyme
('in', 'i')
>>> venus = Pyverse("la luna Venus")
>>> venus.assonant_rhyme, venus.assonant_rhyme_strict
('eo', 'eu')
>>> Pyverse("la luna falla").consonant_rhyme_yeismo
'aya'
>>> Pyverse("el arma antigua").synalephas
['arma antigua']
>>> Pyverse("...")
Traceback (most recent call last):
pyverse.errors.PyverseError: '...' holds no word to read: a verse needs at least one letter.
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
  - Tampoco si hay un signo de puntuación entre las dos palabras, vaya delante o detrás de la cesura:
  
    ```
    -el -ar-ma, -an-ti-gua
    -el -ar-ma ¿-an-ti-gua?
    ```
- Rimas

  - El silabizador proporciona las rimas [asonante](https://es.wikipedia.org/wiki/Rima_asonante) y [consonantes](https://es.wikipedia.org/wiki/Rima_consonante) tanto de palabras como de versos. Todas las rimas van en minúsculas y sin tildes.

  - La rima consonante son todas las letras a partir de la última vocal tónica: *algarabía* rima en `ia`, *porque* en `orque`.

  - La rima asonante es la vocal tónica más la última vocal, sin lo que haya entre ellas: *lánguida* rima en `aa`, *baile* en `ae`, *rey* en `e`.

    - En la lectura **relajada**, que es la de por defecto, una `i` final átona se lee como `e` y una `u` final átona como `o` (Quilis, *Métrica española*): *Venus* rima en `eo` con *cielo*.
    - En la **estricta** la vocal final se toma tal cual se escribe: *Venus* rima en `eu`. La vocal tónica nunca cambia.

  - La rima consonante con **yeísmo** lee `ll` como `y`: *playa* y *falla* riman las dos en `aya`.

  - Lo que el paquete no puede leer como verso lanza `PyverseError`, que hereda de `ValueError`.

### Instalación
Requiere Python 3.12 o superior.
```
pip install pyverse
```

### Uso
puedes usar Pyverse desde el terminal:
```
$ pyverse "un velero bergantín;"

        Syllabified Text | -un -ve-le-ro -ber-gan-tín;
        Count            | 8
        Consonant Rhyme  | in
        Assonant Rhyme   | i
```
o como una librería de Python
```
>>> from pyverse import Pyverse
>>> verse = Pyverse("un velero bergantín;")
>>> verse.syllables
'-un -ve-le-ro -ber-gan-tín;'
>>> verse.count
8
>>> verse.consonant_rhyme, verse.assonant_rhyme
('in', 'i')
>>> venus = Pyverse("la luna Venus")
>>> venus.assonant_rhyme, venus.assonant_rhyme_strict
('eo', 'eu')
>>> Pyverse("la luna falla").consonant_rhyme_yeismo
'aya'
```
