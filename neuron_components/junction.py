import pandas as pd
#from .neuron_base import NeuronBase
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
        if nt_name in self._junction_stores.keys():
            return self._junction_stores[nt_name]
        return 0

    def update_stores(self, nt:str, delta):
        if nt in self._junction_stores.keys():
            print(f"UPDATING STORES BY {delta}")
            self._junction_stores[nt]=self._junction_stores[nt]+delta

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
    def get_state(self):
        stores_list=list([f"Junction_{junc}" for junc in self._junction_stores.keys()])
        pd_series = pd.Series(data=list(self._junction_stores.values()), index= stores_list)
        return pd_series
