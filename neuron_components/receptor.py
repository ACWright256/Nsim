from dataclasses import dataclass
from .minimal_classes import ReceptorResponse
from .neurotransmitters import NeuroTransmitter, NT_dict


@dataclass
class Receptor:
    #TODO maybe the strings can be made into some sort of class or something
    ntransmit: NeuroTransmitter #the neurotransmitter
    response_type: ReceptorResponse #whether or not this receptor will inhibit, excite, or modulate
    input_sensitivity: float #how sensitive this receptor will be to incoming nts
    max_response_strength: int #maximum response to nt
    #name: str = self.ntransmit.name #name of receptor is name of ntransmitter

    def receive(self, nt_count):
        """
        Multipurpose handler for responding.
        Inputs:
            nt_count: how much juice neuron detected (summed across all input synapses)
        Outputs:
            response_token: datastructure containing information about whether or not to activate.
            this token is to be used by the neuron to determine whether or not activate (by
            taking into account all tokens and relative strengths). Response will be determined by
            neuron sensitivity.
        """

        if self.response_type==ReceptorResponse.EXCITORY.value:
            return self._excitory_reception(nt_count)
        elif self.response_type==ReceptorResponse.INHIBITORY.value:
            return self._inhibitory_reception(nt_count)
        elif self.response_type==ReceptorResponse.MODULATORY.value:
            return self._modulatory_reception(nt_count)
        else:
            raise Exception(f"Invalid receptor response type {self.response_type}")

    def _excitory_reception(self,nt_count):
        return int(min(self.max_response_strength, self.ntransmit.bioavailability*nt_count*self.input_sensitivity))

    def _inhibitory_reception(self,nt_count):
        return -1* int(min(self.max_response_strength, self.ntransmit.bioavailability*nt_count*self.input_sensitivity))

    def _modulatory_reception(self,nt_count):
        """TODO: idk what to do with this yet"""

