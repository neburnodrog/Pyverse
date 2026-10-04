"""The Verses the characterization snapshot is recorded over.

Four sources: the literals the test suite already pins, a set built to put
punctuation in every position, a generated set with a fixed seed, and a set
covering the rhyme rules of 3.0.0.

The four are concatenated in that order and the snapshot keeps it, so a source
is only ever extended at its own end. Inserting a Verse in the middle would
renumber the whole file and cost the diff its value as a review artifact.
"""

import random
from typing import List

FROM_THE_SUITE = [
    "Que haya Ariadnas nada cambia.",
    "el augusta ánima canta y baila antes de cada alimaña en el camino",
    "la muerte estaba murmurándome bien.",
    "Las cornisas de la brisa se inventaron el asco de Carlos",
    "Estamos en el mundo y",
    "Las manzanas y los arbustos porque...",
    "Los mentecatos comían manzanas todos juntos",
    "Eran los monjes esdrújulos con",
    "El ánima atraviesa mi",
    "El caballo nos sigue",
    "No sé qué averigüe",
    "Las mñnas son de miedo",
    "asdf",
    "1234",
    "mil 1000",
    "El arma azul",
    "El alma aire",
    "Que la muerte y",
    "La hiena hiede",
    "Las musas se despiertan.",
    "Los ahíncos del aire albo, alzaban el vuelo.",
    "Las cornisas de la brisa se inventaron el asco de Carlos.",
    "El gozne de la puerta aliena la tuerca del frigorífico",
    "un velero bergantín;",
    "Las manzanas y los arbustos porque",
    "¡.,+'onomatopeya...!",
    "¡.,+'hierático...!",
    "¡.,+'melopea...!",
    "¡.,+'alcohol...!",
    "¡.,+'esternohioideo...!",
    "¡.,+'radioautografía...!",
    "¡.,+'glacioeustatismo...!",
    "hierático.",
    "huida",
    "y",
]

VOCABULARY = [
    "el", "la", "los", "las", "un", "una", "de", "del", "en", "con", "por",
    "para", "sin", "sobre", "entre", "y", "e", "o", "u", "ni", "que", "quien",
    "como", "cuando", "donde", "aunque", "porque", "mientras", "apenas",
    "alma", "arma", "aire", "agua", "ala", "árbol", "ámbar", "ánima", "ángel",
    "áspid", "astro", "antes", "alto", "azul", "amor", "año", "arena",
    "bruma", "beso", "bosque", "brisa", "barco", "bergantín", "blanco",
    "caballo", "campo", "canta", "casa", "cielo", "ciudad", "corazón", "cruz",
    "cuerpo", "cumbre", "dolor", "duerme", "día", "dientes", "espejo",
    "estrella", "eco", "elegía", "escarcha", "espuma", "fuego", "flor",
    "frío", "fuente", "guerra", "golondrina", "grito", "hiedra", "hielo",
    "hierba", "hombre", "hoja", "huida", "húmedo", "isla", "invierno",
    "jardín", "joven", "labio", "lágrima", "luna", "luz", "llanto", "lluvia",
    "mano", "mar", "muerte", "montaña", "música", "murmullo", "noche",
    "nube", "nieve", "niño", "ojo", "olvido", "ola", "oro", "otoño", "pájaro",
    "palabra", "piedra", "puerta", "pecho", "polvo", "quimera", "río",
    "rosa", "ruiseñor", "reloj", "sangre", "sombra", "sueño", "sol", "silencio",
    "tiempo", "tierra", "torre", "trigo", "umbral", "viento", "verano",
    "vuelo", "voz", "ventana", "yedra", "zarza", "zorro", "áureo", "océano",
    "país", "poeta", "teoría", "sonríe", "búho", "ahínco", "cohete",
    "veinte", "treinta", "cuatro", "seis", "diez", "mil", "cien",
    "murmurándome", "propóngamelo", "rápidamente", "fácilmente", "esdrújulo",
    "atraviesa", "despiertan", "inventaron", "alzaban", "comían", "averigüe",
    "sigue", "vergüenza", "pingüino", "cigüeña",
]

PUNCTUATION_MARKS = [
    ("¿", "?"),
    ("¡", "!"),
    ('"', '"'),
    ("«", "»"),
    ("(", ")"),
    ("—", "—"),
    ("'", "'"),
]

TRAILING_ONLY = [",", ";", ":", "...", ".", "?", "!"]

PUNCTUATION_FRAMES = [
    "el arma {} antigua",
    "el alma {} eterna",
    "canta {} y baila",
    "la casa {} alta",
    "el viento {} ártico",
    "{} antigua",
    "el arma {}",
]

PUNCTUATED_WORDS = ["antigua", "eterna", "azul", "ánima", "y", "alma", "hiedra"]

#  The marks 3.0.0 teaches the package to read, and the words whose rhymes or
#  accentuation it changes. Kept apart from the sources above so that the
#  Verses they produce keep the positions they already hold in the snapshot.
LATE_PUNCTUATION_MARKS = [("“", "”"), ("‘", "’"), ("–", "–")]

LATE_TRAILING_MARKS = ["…", "–", "”", "’"]

REMAPPED_WORDS = [
    "lánguida", "antigua", "lirio", "lluvia", "baile", "reina", "rey",
    "averigüe", "Venus", "fácil", "lápiz", "tío", "playa", "falla",
    "cortésmente", "comúnmente", "rápidamente", "CORAZÓN", "Ávila", "aquí",
    "sabíamos", "línea", "tribu", "seis", "aunque",
]


def _punctuation_verses() -> List[str]:
    verses = []

    for opening, closing in PUNCTUATION_MARKS:
        for word in PUNCTUATED_WORDS:
            for frame in PUNCTUATION_FRAMES:
                verses.append(frame.format(opening + word))
                verses.append(frame.format(word + closing))
                verses.append(frame.format(opening + word + closing))
            verses.append("el arma " + opening + " " + word)

    for mark in TRAILING_ONLY:
        for word in PUNCTUATED_WORDS:
            verses.append("el arma " + word + mark + " antigua")
            verses.append("el arma " + mark + " " + word)

    return verses


def _rhyme_rule_verses() -> List[str]:
    """The cases the 3.0.0 rhyme and punctuation changes are aimed at."""

    verses = list(REMAPPED_WORDS)
    verses += ["la luna " + word for word in REMAPPED_WORDS]

    for opening, closing in LATE_PUNCTUATION_MARKS:
        for word in PUNCTUATED_WORDS:
            for frame in PUNCTUATION_FRAMES:
                verses.append(frame.format(opening + word))
                verses.append(frame.format(word + closing))
                verses.append(frame.format(opening + word + closing))
            verses.append("el arma " + opening + " " + word)

    for mark in TRAILING_ONLY + LATE_TRAILING_MARKS:
        for word in PUNCTUATED_WORDS:
            #  a Verse ending in a token that is punctuation and nothing else
            verses.append("el arma " + word + " " + mark)
            verses.append("la luna" + mark)

    return verses


def _generated_verses(count: int = 300, seed: int = 20260925) -> List[str]:
    rng = random.Random(seed)
    return [
        " ".join(rng.choice(VOCABULARY) for _ in range(rng.randint(2, 9)))
        for _ in range(count)
    ]


def verses() -> List[str]:
    """Every Verse in the snapshot, in a stable order."""

    seen = {}
    sources = (
        FROM_THE_SUITE
        + _punctuation_verses()
        + _generated_verses()
        + _rhyme_rule_verses()
    )

    for verse in sources:
        seen.setdefault(verse, None)
    return list(seen)
