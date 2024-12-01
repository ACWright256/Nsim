import yaml
import os

from neuron_components.neuron_base import NeuronBase
from neuron_components.receptor import Receptor
from neuron_components.transmitter import Transmitter
from neuron_components.junction import NeuronJunction
from constants import USERGENDIR
from neuron_components.neurotransmitters import NeuroTransmitter, NT_dict

def load_generation_file(file_name:str):
    full_path = os.path.join(USERGENDIR,file_name)
    with open(full_path, 'r') as file:
        neuron_file = yaml.safe_load(file)
    return neuron_file

def create_net_from_file(neuron_dict:dict):
    object_dict:{}
    id_list_full=neuron_dict.keys()
    id_list_numeric=[ int(uid[3:]) for uid in id_list_full]
    #Phase 1: Generate all the constants
    for idx, uid in enumerate(id_list_full):
        uid_key=id_list_full['idx']
        cur_neuron=neuron_dict['uid_key']
        sensitivity=cur_neuron['sensitivity']
        input_cnt=cur_neuron['input_cnt']
        output_cnt=cur_neuron['output_cnt']
        parent_uids=cur_neuron['parent_uids']
        child_uids=cur_neuron['child_uids']
        initial_state=cur_neuron['initial_state']
        tx_off_period=cur_neuron['tx_off_period']
        tx_on_period=cur_neuron['tx_on_period']

        receptors_dict={}
        transmitters_dict={}

        cur_receptors_list = cur_neuron['receptors']
        cur_transmitters_list=cur_neuron["transmitters"]
        receptors_names = cur_receptors_list.keys()
        transmitter_names = cur_transmitters_list.keys()

        #generate receptors
        for recep in receptors_names:
            cur_recep=cur_receptors_list[recep]
            response_type=cur_recep['response_type']
            input_sensitivity=cur_recep['input_sensitivity']
            max_response_strength=cur_recep['input_sensitivity']
            receptors_dict[recep]=Receptor(ntransmit=NT_dict[recep],
                                            response_type=response_type,
                                            input_sensitivity=input_sensitivity,
                                            max_response_strength=max_response_strength)
        #generate Transmitters
        for tx in transmitter_names:
            cur_tx=cur_transmitters_list[tx]
            regeneration_constant=cur_tx['regeneration_constant']
            transmission_strength=cur_tx['transmission_strength']
            transmission_strength_stdev=cur_tx['transmission_strength_stdev']
            initial_stores=cur_tx["initial_stores"]
            transmitters_dict[tx]=Transmitter(ntransmit=NT_dict[tx],
                                            transmission_strength=transmission_strength,
                                            transmission_strength_stdev=transmission_strength_stdev,
                                            regeneration_constant=regeneration_constant,
                                            stores=0)
        #junction stuff
        input_junc=NeuronJunction(_junction_stores=cur_neuron["initial_junc_stores"])
        object_dict[uid]=NeuronBase(uid=uid,
                                    input_cnt=input_cnt,
                                    output_cnt=output_cnt,
                                    parent_uids=parent_uids,
                                    child_uids=child_uids,
                                    receive_sensitivity=sensitivity,
                                    receptors=receptors_dict,
                                    transmitters=transmitters_dict,
                                    input_junction=input_junc,
                                    output_junctions=[],
                                    neuron_state=initial_state,
                                    is_rx_met=False,
                                    tx_off_period=tx_off_period,
                                    tx_off_cnt=0,
                                    tx_on_period=tx_on_period,
                                    tx_on_cnt=0)
    #Phase 2: Add the junctions
    for idx, uid in enumerate(object_dict.keys()):
        cur_neuron = object_dict[uid]
        for child_uid in cur_neuron.child_uids:
            cur_neuron.output_junctions.append(object_dict[child_uid].input_junction)
    return object_dict