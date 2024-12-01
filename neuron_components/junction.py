from .neuron_base import NeuronBase
from dataclasses import dataclass
from .neurotransmitters import NeuroTransmitter, NT_dict

@dataclass
class NeuronJunction:
    """
        Attached to a parent neuron. Associated with neuronal input.
        Contains references to neurons transmitting to parent neuron.
        Handles neurotransmitter degradation and reuptake
    """
    _junction_stores: dict[str,int] #how much of a given neurotransmitter is currently in the junction

    def get_junction_store(self, nt_name:str):
        return _junction_stores[nt_name]

    def update_stores(nt:str, delta):
        self.junction_stores[nt]=self.junction_stores[nt]+delta

    def reuptake_update(self):
        """
            Removes neurotransmitters from the junction based on reuptake.
            returns a dict containing the names of each neurotransmitter, and how much gets transferred to
            the calling neuron
        """
        reuptake_dict={}
        for nt in self._junction_stores.keys():
            nt_class=NT_dict[nt]
            removed=int(nt_class.degradation_coef*self._junction_stores[nt])
            self.update_stores(nt, -1*removed)
            reuptake_dict[nt]=removed
        return reuptake_dict

    def degradation_update(self):
        """
            Removes neurotransmitters from junction based on degradation. Nothing is returned
        """
        for nt in self._junction_stores.keys():
            nt_class=NT_dict[nt]
            removed=int(nt_class.degradation_coef*self._junction_stores[nt])
            self.update_stores(nt, -1*removed)
    #def update(self):