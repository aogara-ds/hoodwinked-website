import time
import pandas as pd
import os
import matplotlib.pyplot as plt

# Load CSV from Results directory
save_dir = 'results'
file_name = '0'
full_path = save_dir + '/' + file_name + '.csv'

print(full_path)
eval_df = pd.read_csv(full_path, index_col=0)

print(eval_df)


# Calculate metrics for evaluation
total_killers = eval_df['killer'].sum()
total_innocents = len(eval_df) - total_killers

# Sanity Check that calculations are correct
# print(total_killers)
# print(total_innocents)

total_innocent_escaped = len(
    eval_df[(eval_df['killer'] == False) & (eval_df['escaped'] == True)])

total_banished_killer = len(
    eval_df[(eval_df['killer'] == True) & (eval_df['banished'] == True)])

total_innocent_killed = len(
    eval_df[(eval_df['killer'] == False) & (eval_df['killed'] == True)])

total_innocent_banished = len(
    eval_df[(eval_df['killer'] == False) & (eval_df['banished'] == True)])

all_random_innocent = ["All Random", total_innocent_escaped, total_banished_killer,
                       total_innocent_killed, total_innocent_banished]

# Works
innocents_summary = pd.DataFrame(
    columns=["Setup", "Escaped (%)", "Banished Killer (%)", "Killed (%)", "Banished (%)"])
innocents_summary.set_index("Setup")
innocents_summary.loc[0] = all_random_innocent

print(innocents_summary)
labels = innocents_summary.columns

innocents_summary.plot(x=labels[0], y=labels[1:], kind="bar")

# innocents_summary.plot(x=innocents_summary.columns, y=innocents_summary)
plt.show()
