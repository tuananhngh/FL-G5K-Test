import pandas as pd
import os
strategy = 'fedadam'
nb_clients = 70

file_origin = f"/Users/Slaton/Documents/grenoble-code/fl-flower/energyfl/outputcifar10/30clients/fractionfit/{strategy}/labelskew/"
file_new = f"/Users/Slaton/Documents/grenoble-code/fl-flower/energyfl/outputcifar10/30clients/fractionfit2/{strategy}/labelskew"

exp_summary1 = pd.read_csv(os.path.join(file_origin, "experiment_summary.csv"))
exp_summary2 = pd.read_csv(os.path.join(file_new,"experiment_summary.csv"))

date = "2024-06-15_11-54-51"
filtered = exp_summary2.result_folder.apply(lambda x: x.split('/')[-1] == date)
new_exp = exp_summary2[filtered].reset_index(drop=True)
new_exp.to_csv(os.path.join(file_origin, "experiment_summary1.csv"), index=False)