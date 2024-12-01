from dataclasses import dataclass
from .neurotransmitters import NeuroTransmitter
from .minimal_classes import TransmissionToken
import numpy as np

@dataclass
class Transmitter:
    #TODO maybe the strings can be made into some sort of class or something
    ntransmit: NeuroTransmitter #the name of the neurotransmitter
    transmission_strength: int #strength of transmission. This count will be divided up by all receiving neurons
    transmission_strength_stdev: int #standard deviation of strengths
    regeneration_constant:int #how much per delta time the stores regenerate
    stores: int #how much "juice" the parent neuron has for this particular associated NT
    name:str = ntransmit.name #name of receptor is name of ntransmitter

    def transmit(self):
        """
        Returns a transmission Token. This token is used by the neuron to
        transmit nts to the junction, divided by number of output synapse.
        Transmission will not occur if stores are depleted
        """
        current_tx_strength = np.random.normal(loc=self.transmission_strength, scale=self.transmission_strength_stdev)
        tx_val = max(current_tx_strength,stores)
        self.update_stores(-1*tx_val)
        return tx_val
        #if self.transmission_str > stores:
        #    
        #    return 0
        #    #return TransmissionToken(relative_strength=0, ntransmit=self.ntransmit)
        #else:
        #    self.update_stores(-1*self.transmission_str)
        #    return self.transmission_str
        #    #return TransmissionToken(relative_strength=self.transmission_str, ntransmit=self.ntransmit)
    
    def regenerate(self):
        self.update_stores(self.regeneration_constant)

    def update_stores(self, delta_stores):
        """will be used to update stores based on reuptake and transmission"""
        self.stores=self.stores + delta_stores
