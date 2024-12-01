import os
from datetime import datetime
from constants import OUTPUTDIR
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sim_helper.generate_neurons import load_generation_file, create_net_from_file

def main():
    date_str=f'{datetime.now():%Y-%m-%d %H-%M-%S%z}'
    output_directory_folder=os.path.join(OUTPUTDIR,date_str)
    if not os.path.exists(output_directory_folder):
        os.makedirs(output_directory_folder)

    total_df=pd.DataFrame()
    gen_file_name="test.yaml"
    neuron_dict=load_generation_file(file_name=gen_file_name)
    neuron_obj_dict= create_net_from_file(neuron_dict=neuron_dict)
    iterations=10
    for i in range(iterations):
        iteration_df_list=[]
        for uid in neuron_obj_dict.keys():
            cur_neuron=neuron_obj_dict[uid]

            cur_neuron.update()
            iteration_df_list.append(pd.DataFrame(data=cur_neuron.get_state(),columns=[f"UID_{uid}"]))
        iteration_df=pd.concat(iteration_df_list,axis=1)
        timestep_dataframe=pd.DataFrame(columns=["timestamp"], data=i*np.ones(len(iteration_df)), index=iteration_df.index)
        iteration_df=pd.concat([timestep_dataframe,iteration_df],axis=1)
        #print("\n")
        #print(iteration_df)
        total_df=pd.concat([total_df,iteration_df], axis=0)
        total_df.to_csv(os.path.join(output_directory_folder,"output_file.csv"))
    print(total_df)
    print(total_df.loc[["Transmitter_WumbusNT"]])
    print(total_df.loc[["neuron_state"]])
    print(total_df.loc[["Junction_WumbusNT"]])
    #plt.figure()
    

if __name__ == '__main__':
    main()