from enum import Enum
from dataclasses import dataclass
from .neurotransmitters import NeuroTransmitter

class ReceptorResponse(Enum):
    EXCITORY= "EXCITORY"
    INHIBITORY= "INHIBITORY"
    MODULATORY= "MODULATORY"
    
    #def __eq__(self,other):
    #    return self==other

