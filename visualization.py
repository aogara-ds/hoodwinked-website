import time
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Load CSV from Results directory
save_dir = 'results'
file_name = '3'
full_path = save_dir + '/' + file_name + '.csv'

print(full_path)
eval_df = pd.read_csv(full_path, index_col=0)

setups = ["all_random", "all_gpt", "gpt_killer_remaining_random"]


# Calculate metrics for evaluation
total_killers = np.array([eval_df.loc[(
    eval_df['Setup'] == setup), 'killer'].sum() for setup in setups])
total_agents = np.array(
    [len(eval_df[eval_df["Setup"] == setup]) for setup in setups])
total_innocent = np.subtract(total_agents, total_killers)

# Sanity Check that calculations are correct
# print(total_killers)
# print(total_innocents)


# INNOCENTS SUMMARY
total_innocent_escaped = np.array([len(
    eval_df[(eval_df['killer'] == False) & (eval_df['escaped'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

total_banished_killer = np.array([len(
    eval_df[(eval_df['killer'] == True) & (eval_df['banished'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

total_innocent_killed = np.array([len(
    eval_df[(eval_df['killer'] == False) & (eval_df['killed'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

total_innocent_banished = np.array([len(
    eval_df[(eval_df['killer'] == False) & (eval_df['banished'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

# PLOTS
innocents_summary = pd.DataFrame(
    columns=["Setup", "Escaped (%)", "Banished Killer (%)", "Killed (%)", "Banished (%)"])
innocents_summary.set_index("Setup")
innocents_summary["Setup"] = setups
innocents_summary["Escaped (%)"] = total_innocent_escaped / \
    total_innocent * 100
innocents_summary["Banished Killer (%)"] = total_banished_killer / \
    total_innocent * 100
innocents_summary["Killed (%)"] = total_innocent_killed / total_innocent * 100
innocents_summary["Banished (%)"] = total_innocent_banished / \
    total_innocent * 100


print(innocents_summary)
labels = innocents_summary.columns

innocents_summary.plot(x=labels[0], y=labels[1:], kind="bar")
plt.xticks(rotation=0)
# innocents_summary.plot(x=innocents_summary.columns, y=innocents_summary)
plt.show()
