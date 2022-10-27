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

num_games = total_killers  # Since there is one killer per game this is an easy fix

# INNOCENTS SUMMARY
total_innocent_escaped = np.array([len(
    eval_df[(eval_df['killer'] == False) & (eval_df['escaped'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

total_banished_killer = np.array([len(
    eval_df[(eval_df['killer'] == True) & (eval_df['banished'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

total_innocent_killed = np.array([len(
    eval_df[(eval_df['killer'] == False) & (eval_df['killed'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

total_innocent_banished = np.array([len(
    eval_df[(eval_df['killer'] == False) & (eval_df['banished'] == True) & (eval_df['Setup'] == setup)]) for setup in setups])

# INNOCENTS AVERAGES
avg_turns_before_escape = np.array([eval_df.loc[(eval_df['killer'] == False) & (eval_df['escaped'] == True) & (eval_df['Setup'] == setup), 'num_turns'].mean() for setup in setups])

avg_turns_before_killed = np.array([eval_df.loc[(eval_df['killer'] == False) & (eval_df['killed'] == True) & (eval_df['Setup'] == setup), 'num_turns'].mean() for setup in setups])

avg_turns_before_banished = np.array([eval_df.loc[(eval_df['killer'] == False) & (eval_df['banished'] == True) & (eval_df['Setup'] == setup), 'num_turns'].mean() for setup in setups])


# PLOTS

# INNOCENT SUMMARY
innocents_summary = pd.DataFrame(
    columns=["Setup", "Escaped (%)", "Banished Killer (%)", "Killed (%)", "Banished (%)"])
innocents_summary.set_index("Setup")
innocents_summary["Setup"] = setups
innocents_summary["Escaped (%)"] = total_innocent_escaped / \
    total_innocent * 100
innocents_summary["Banished Killer (%)"] = total_banished_killer / \
    num_games * 100
innocents_summary["Killed (%)"] = total_innocent_killed / total_innocent * 100
innocents_summary["Banished (%)"] = total_innocent_banished / \
    total_innocent * 100

# INNOCENT AVERAGE
# Average turns before:
innocents_avg = pd.DataFrame(
    columns=["Setup", "Escaped", "Banished", "Killed"])
innocents_avg.set_index("Setup")
innocents_avg["Setup"] = setups
innocents_avg["Escaped"] = avg_turns_before_escape
innocents_avg["Banished"] = avg_turns_before_banished
innocents_avg["Killed"] = avg_turns_before_killed


# KILLER
killer_summary = pd.DataFrame(columns=["Setup", "Banished Rate (%)"])
killer_summary["Setup"] = setups
killer_summary["Banished Rate (%)"] = total_banished_killer / \
    total_killers * 100

print(innocents_summary)
print(innocents_avg)
print(killer_summary)

killer_summary.plot(
    x=killer_summary.columns[0], y=killer_summary.columns[1], kind="bar")
plt.xticks(rotation=0)
plt.title("Killer Summary")

innocents_summary.plot(
    x=innocents_summary.columns[0], y=innocents_summary.columns[1:], kind="bar")
plt.xticks(rotation=0)
plt.title("Innocents Summary")

innocents_avg.plot(
    x=innocents_avg.columns[0], y=innocents_avg.columns[1:], kind="bar")
plt.xticks(rotation=0)
plt.title("Innocents Average Turns Before Being:")

plt.show()
