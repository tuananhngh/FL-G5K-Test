from typing import Dict, Tuple
from box import Box
import pandas as pd
import os
import sys
import cProfile
import io
import pstats
from collections import defaultdict

sys.path.append("/Users/Slaton/Documents/grenoble-code/fl-flower/jetson-tl/analysis/")
from utils.process_experiment import ProcessResults, EnergyResults, read_server
from utils.process_energy import (
    aggregate_round_stats,
    compute_energy_within_range,
    compute_strategy_exp_energy_perf,
    compute_host_energy
)
from utils.read_file_functions import load_client_data, load_server_data, server_log_file_to_csv
import time

start = time.time()

usr_homedir = "/Users/Slaton/Documents/grenoble-code/fl-flower"
strategies = ['fedadam', 'fedconstraints']
nb_clients = [10, 20, 30, 50, 70, 100]#20,30,50,70,100]

def read_multiclient_host(usr_homedir,parent_path, strategies, threshold=None):
    result_summary = EnergyResults(output_dir=parent_path,
                                usr_homedir=usr_homedir,
                                strategies=strategies,
                                condition=None,
                                threshold=threshold,
                                epoch_list=[1],
                                split='labelskew'
                                )
    exp_summaries = pd.DataFrame()#defaultdict(dict)
    energy_summaries = pd.DataFrame()#defaultdict(dict)
    perf_summaries = pd.DataFrame()#defaultdict(dict)
    results_acc = defaultdict(dict)
    for strategy in strategies:
        exp_summary = result_summary.get_experiment_summary(strategy,'epoch_1','exp_0')
        exp_summary = pd.DataFrame(exp_summary, index=[0])
        energy_summary,perf_summary = compute_strategy_exp_energy_perf(result_summary, strategy)
        exp_summary['strategy'] = [strategy]*len(exp_summary)
        energy_summary['strategy'] = [strategy]*len(energy_summary)
        perf_summary['strategy'] = [strategy]*len(perf_summary)
        exp_summaries = pd.concat([exp_summaries, exp_summary], axis=0)
        energy_summaries = pd.concat([energy_summaries, energy_summary], axis=0)
        perf_summaries = pd.concat([perf_summaries, perf_summary], axis=0)
        
        server_files = result_summary.get_server_results(strategy,'epoch_1','exp_0')
        
        results_acc[strategy] = server_files['results']
    return energy_summaries, perf_summaries, exp_summaries, results_acc


output_path = "/Users/Slaton/Documents/grenoble-code/fl-flower/energyfl/outputcifar10/"
save_path = "../files/"
def read_all_multiclients_host(output_path, save_path, usr_home_dir, nb_clients_list, strategies):
    energy_summaries = pd.DataFrame()
    perf_summaries = pd.DataFrame()
    exp_summaries = pd.DataFrame()
    for nb in nb_clients_list:
        print(f'Number of clients: {nb}')
        parent_path = os.path.join(output_path, f'{nb}clients', 'fractionfit')
        energy_summary, perf_summary, exp_summary, *tobedefine = read_multiclient_host(usr_home_dir, parent_path, strategies,threshold=0.75)
        energy_summary["nb_clients"] = [nb]*len(energy_summary)
        perf_summary["nb_clients"] = [nb]*len(perf_summary)
        
        #exp_summary = pd.DataFrame(exp_summary, index=[0])
        exp_summary["nb_clients"] = [nb]*len(exp_summary)
        energy_summaries = pd.concat([energy_summaries, energy_summary], axis=0)
        perf_summaries = pd.concat([perf_summaries, perf_summary], axis=0)
        exp_summaries = pd.concat([exp_summaries, exp_summary], axis=0)
        
        path_nb = os.path.join(save_path, f'{nb}clients')
        if not os.path.exists(path_nb):
            os.makedirs(path_nb)
        unpack = tobedefine[0]
        for key, res in unpack.items():
            res.to_csv(os.path.join(path_nb, f'{key}.csv'))
    return energy_summaries, perf_summaries, exp_summaries, tobedefine
        
energy_summary, perf_summary, exp_summary, tobedefine = read_all_multiclients_host(output_path, save_path, usr_homedir, nb_clients, strategies)


#tobedefine[0][0]['fedadam']['split_epoch']['epoch_1']['exp_0']['server']['results']
# energy_summary.to_parquet(os.path.join(save_path,"multiclients_energy_summary.parquet"))
# perf_summary.to_parquet(os.path.join(save_path,"multiclients_perf_summary.parquet"))
# exp_summary.to_parquet(os.path.join(save_path,"multiclients_exp_summary.parquet"))
