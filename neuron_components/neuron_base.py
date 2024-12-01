from dataclasses import dataclass
from .receptor import Receptor
from.transmitter import Transmitter
from .minimal_classes import ReceptionToken, TransmissionToken
from .junction import NeuronJunction
from enum import Enum
import pandas as pd

class NeuronState(Enum):
    OFF=0
    ON=1


@dataclass
class NeuronBase:
    #book keeping
    uid: int #unique identifier
    input_cnt:int
    output_cnt:int
    parent_uids:list[int]=[]
    child_uids:list[int]=[]

    receive_sensitivity: int #Threshold required to be overcome to generate an action potential
    receptors: dict[str, Receptor] #nt names and receptor type
    transmitters: dict[str,Transmitter]

    input_junction: NeuronJunction = None
    output_junctions: list[NeuronJunction] = {} #every other neuron connected to
    neuron_state: NeuronState

    is_rx_met: bool #whether or not the neuron is currently currently firing for the current cycle
    tx_off_period:int
    tx_off_cnt:int=0
    tx_on_period: int
    tx_on_cnt: int=0

    def post_init(junction_list:list[NeuronJunction], input_junction:NeuronJunction, parent_ids:list[int], child_ids:list[int]):
        #Done after the creation of the neurons, to help get the conntions right
        self.input_junction=input_junction
        self.output_junctions=junction_list
        self.parent_ids=parent_ids
        self.child_ids=child_ids

    def update(self):
        """"""
        if self.tx_off_cnt==self.tx_off_period and self.is_rx_met == True:
            #Is now possible to go to the ON state
            #self.tx_off_cnt=0
            self.neuron_state = NeuronState.ON
        elif self.tx_on_cnt == self.tx_on_period:
            #must return to the off state, regardless if rx is met
            #self.tx_on_cnt=0
            #self.tx_off_cnt=0
            self.neuron_state = NeuronState.OFF

        self._update_junctions_tx()
        self._update_rx()
        self._maintenance_update()
        #self._reuptake()

        if self.neuron_state == NeuronState.ON:
            self.tx_off_cnt=0
            self.tx_on_cnt = (self.tx_on_cnt+1)% (self.tx_off_period+1)
        else:
            self.tx_on_cnt=0
            self.tx_off_cnt = (self.tx_off_cnt+1)%(self.tx_off_period+1)

    def _update_nt_stores(self, transmitter_dict:dict[str,int]):
        """Update transmitter stores"""
        for nt_name in transmitter_dict.keys():
            self.transmitters[nt_name].update_stores(transmitter_dict[nt_name])

    def _update_rx(self):
        """Sum across all receptors. If threshold is met, is possible to transmit"""
        potential_count=0
        for nt_name in self.receptors.keys():
            nt_count_junc = self.input_junction.get_junction_store(nt_name)
            potential_count =  potential_count + self.receptors[nt_name].receive(nt_count_junc)
        if potential_count >= receive_sensitivity:
            self.is_rx_met=True
        else:
            self.is_rx_met=False

    def _update_junctions_tx(self):
        """
        Adds neurotransmitters to the junction from the tranmitter, if transmission is occurring
        """
        if self.neuron_state==NeuronState.ON:
            for tx_key in self.transmitters.keys():
                tx=self.transmitters[tx_key]
                tx_count = tx.transmit()
                tx_per_junc = tx_count//len(self.output_junctions)
                for junction in self.output_junctions:
                    junction.update_stores(tx_key,tx_per_junc)

    def _maintenance_update(self):
        """Handles junction updates, and transmitter regeneration"""
        for junc in self.output_junctions:
            reuptake_dict=junc.reuptake_update()
            junc.degradation_update()
            self._update_nt_stores(transmitter_dict=reuptake_dict)
        for tx_key in self.transmitters:
            self.transmitters[tx_key].regenerate()

    def _reuptake(self):
        """remove neurotransmitters from the junction, add them to appropriate tx stores"""
        for junc in self.output_junctions:
            reuptake_dict=junc.reuptake_update()
            self._update_nt_stores(transmitter_dict=reuptake_dict)
    def get_state(self):
        """Puts all the nice state information into a dataframe :)"""
        base_array=[self.is_rx_met, self.tx_off_period, self.tx_off_cnt, self.tx_on_period, self.tx_on_cnt, self.neuron_state]
        base_array_index=["is_rx_met", "tx_off_period", "tx_off_cnt", "tx_on_period", "tx_on_cnt", "neuron_state"]
        base_series=pd.Series(data=base_array, index=base_array_index)
        junction_series = self.input_junction.get_state()
        tx_array_vals=[]
        tx_array_index=[]
        for tx_key in self.transmitters.keys():
            tx_array_index.append(f"Transmitter_{tx_key}")
            tx_array_vals.append(self.transmitters[tx_key].stores)
        tx_series=pd.Series(data=tx_array_vals, index=tx_array_index)
        state_series=pd.concat([base_series, junction_series, tx_series])
        return state_series
