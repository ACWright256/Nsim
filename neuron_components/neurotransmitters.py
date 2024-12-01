##### Contains "static" data classes for neurotransmitters
from dataclasses import dataclass

@dataclass
class NeuroTransmitter:
    name: str
    uptake_coef: float
    degradation_coef: float
    bioavailability: float

@dataclass
class WumbusNT(NeuroTransmitter):
    name:str = "WumbusNT"
    uptake_coef:float = 0.025
    degradation_coef:float = 0.05
    bioavailability:float=0.6

@dataclass
class BadLongNameNT(NeuroTransmitter):
    name:str = "BadLongNameNT"
    uptake_coef:float = 0.01
    degradation_coef:float = 0.09
    bioavailability:float=0.7

@dataclass
class DiabolicalDastardlyNT(NeuroTransmitter):
    name:str = "DiabolicalDastardlyNT"
    uptake_coef:float = 0
    degradation_coef=0.25
    bioavailability:float=0.4

@dataclass
class Greg(NeuroTransmitter):
    name:str = "Greg"
    uptake_coef:float = 0.001
    degradation_coef=0.001
    bioavailability:float=0.9

@dataclass
class SillyGooseNT(NeuroTransmitter):
    name:str = "SillyGooseNT"
    uptake_coef:float = 0.001
    degradation_coef=0.001
    bioavailability:float=0.9

@dataclass
class SomberSwanNT(NeuroTransmitter):
    name:str = "SomberSwanNT"
    uptake_coef:float = 0.001
    degradation_coef=0.001
    bioavailability:float=0.9


NT_dict={
    "WumbusNT": WumbusNT,
    "BadLongNameNT":BadLongNameNT,
    "DiabolicalDastardlyNT":DiabolicalDastardlyNT,
    "Greg":Greg,
    "SillyGooseNT": SillyGooseNT,
    "SomberSwanNT": SomberSwanNT
}