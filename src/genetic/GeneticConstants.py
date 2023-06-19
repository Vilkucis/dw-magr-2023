from enum import Enum


class CrossoverType(Enum):
    SINGLE_POINT = "single_point"
    TWO_POINTS = "two_points"
    UNIFORM = "uniform"
    SCATTERED = "scattered"

class ParentSelectionType(Enum):
    SSS = "sss"
    RWS = "rws"
    SUS = "sus"
    RANK = "rank"
    RANDOM = "random"
    TOURNAMENT = "tournament"