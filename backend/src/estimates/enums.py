from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class ActivityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ImpactType(str, Enum):
    forehand = "forehand"
    backhand = "backhand"
    serve = "serve"
    volley = "volley"
    smash = "smash"
