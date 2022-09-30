from math import sqrt
from typing import Iterable


def moyenne(data: list) -> float:
    return float(sum(data)/len(data))


def get_incertitude_type_uniforme(composante: float) -> float:
    return composante/sqrt(3)


def get_somme_quadratique(data: Iterable[float]) -> float:
    return sqrt(sum([pow(d, 2) for d in data]))
