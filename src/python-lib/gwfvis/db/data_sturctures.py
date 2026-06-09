# %% data structures
from dataclasses import dataclass
from typing import Dict, Sequence

@dataclass
class Info:
    key: str
    value: str = None
    label: str = None

    def __hash__(self):
        return id(self)


@dataclass
class Location:
    id: int
    geometry: dict
    metadata: dict = None

    def __hash__(self):
        return id(self)


@dataclass
class Dimension:
    id: int
    name: str
    size: int
    description: str = None
    value_labels: Sequence[str] = None

    def __hash__(self):
        return id(self)


@dataclass
class Variable:
    id: int
    name: str
    dimensions: Sequence[Dimension]
    unit: str = None
    description: str = None

    def __hash__(self):
        return id(self)


@dataclass
class Value:
    location: Location
    variable: Variable
    value: float
    dimension_dict: Dict[Dimension, int] = None

    def __hash__(self):
        return id(self)


@dataclass
class Options:
    info: Sequence[Info]
    locations: Sequence[Location]
    dimensions: Sequence[Dimension]
    variables: Sequence[Variable]
    values: Sequence[Value]

    def __hash__(self):
        return id(self)
