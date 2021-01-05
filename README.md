[![codecov](https://img.shields.io/codecov/c/github/neburnodrog/silabizador)](https://codecov.io/gh/neburnodrog/silabizador)

# silabizador
#### A syllabification algorithm for the Spanish language written in Python

- It separates every syllable in words and sentences. It counts the syllables as it's done in the spanish language poetry tradition.


---

# silabizador: algoritmo silabeador de la lengua española.
#### Un algoritmo silabeador para versos en español.

#### [silabizar](https://dle.rae.es/silabizar)
```
Del lat. mediev. syllabizare.
1. desus. silabear.
```
#### [silabear](https://dle.rae.es/silabear)
```
1. Ir pronunciando separadamente cada sílaba.
```


### Descripcion
- El silabizador separa palabras y frases en sílabas. Cuenta las sílabas a la manera de la tradición poética en lengua española. 
Es decir: tiene en cuenta sinalefas y finales de verso. Según la acentuación de la última palabra del verso se dan varios casos:
  1. Si la última palabra tiene una acetuación aguda u oxítona, la perceptión prosódica del verso impone que se le sume una sílaba al número de sílabas ortográficas del verso.
  2. Si es llana o paroxítona se deja como está: ni se le resta ni se le suman sílabas al verso.
  3. Si la última palabra del verso es esdrújula o proparoxítona se le resta una sílaba al verso.
  4. Si es superproparoxítona o sobresdrújula se le restan dos sílabas al verso.

