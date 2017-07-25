
# coding: utf-8

# In[ ]:


get_ipython().magic(u'pylab inline')
from multiprocessing import Process
from multiprocessing import JoinableQueue as Queue
from Queue import Empty
import sys
import time
import numpy as np
import pandas as pd
import scipy.stats as spstats
import elp_networks.algorithms as elpalg
import elp_nkmodel as elpnk
import logbook
import net
import simulator
import strategy


# In[ ]:


def values_to_efficiency(values):
    start = values[0]
    halfmax = (max(values) - start) / 2.0 + start
    return 1.0 / float(len([v for v in values if v <= halfmax]))


# In[ ]:


def simulate(N, K, D, rewire, steps=50, sample=3):
    start_time = time.time()
    run_data = {"N": N, "K":K, "D":D, "rewire":rewire, "steps":steps, "sample":sample}
    values = {}
    model = elpnk.NK(N, K)
    # Generate network from NK structure
    edges_node_loc = net.nk_to_affiliation(model, D)
    if rewire > 0:
        net.rewire_affiliation(model, edges_node_loc, rewire)
    edges = net.affiliation_to_node(edges_node_loc)
    # Create strategies
    best_ind_strat = strategy.BestNeighborIndividual(model, edges, sample)
    conform_ind_strat = strategy.ConformityIndividual(model, edges, sample)
    loc_conform_ind_strat = strategy.LocalConformityIndividual(model, edges_node_loc, sample)
    loc_best_ind_strat = strategy.LocalConformityIndividual(model, edges_node_loc, sample)
    loc_conform_unstructured = strategy.LocalConformityIndividual(model, edges_node_loc, sample, False)
    loc_best_unstructured = strategy.LocalConformityIndividual(model, edges_node_loc, sample, False)
    #loc_ind_cons_strat = strategy.LocalIndividualConsensus(model, edges_node_loc)
    # Simulate strategies
    sim = simulator.Simulator(model, edges, best_ind_strat)
    sim.run(steps)
    run_data["best_perf"] = [sim.values[-1]]
    run_data["best_eff"] = values_to_efficiency(sim.values)
    values["best_values"] = sim.values
    sim = simulator.Simulator(model, edges, conform_ind_strat)
    sim.run(steps)
    run_data["conform_perf"] = [sim.values[-1]]
    run_data["conform_eff"] = values_to_efficiency(sim.values)
    values["conform_values"] = sim.values
    sim = simulator.Simulator(model, edges, loc_conform_ind_strat)
    sim.run(steps)
    run_data["loc_conform_perf"] = [sim.values[-1]]
    run_data["loc_conform_eff"] = values_to_efficiency(sim.values)
    values["loc_conform_values"] = sim.values
    sim = simulator.Simulator(model, edges, loc_best_ind_strat)
    sim.run(steps)
    run_data["loc_best_perf"] = [sim.values[-1]]
    run_data["loc_best_eff"] = values_to_efficiency(sim.values)
    values["loc_best_values"] = sim.values
    sim = simulator.Simulator(model, edges, loc_conform_unstructured)
    sim.run(steps)
    run_data["loc_conform_unstruct_perf"] = [sim.values[-1]]
    run_data["loc_conform_unstruct_eff"] = values_to_efficiency(sim.values)
    values["loc_conform_unstruct_values"] = sim.values
    sim = simulator.Simulator(model, edges, loc_best_unstructured)
    sim.run(steps)
    run_data["loc_best_unstruct_perf"] = [sim.values[-1]]
    run_data["loc_best_unstruct_eff"] = values_to_efficiency(sim.values)
    values["loc_best_unstruct_values"] = sim.values
#    sim = simulator.Simulator(model, edges, loc_ind_cons_strat)
#    sim.run(steps)
#    run_data["loc_cons_perf"] = [sim.values[-1]]
#    values["loc_cons_values"] = sim.values
    # Find diameter and mean path length
    next_diameter = 0
    total_path = 0
    path_count = 0
    for n in edges.keys():
        distances = elpalg.get_distances_bfs(edges, n)
        d = max(distances.values())
        total_path += sum(distances.values())
        path_count += len(distances.values()) - 1 # Don't count self
        if d > next_diameter:
            next_diameter = d
    run_data["meanpath"] = [float(total_path) / float(path_count)]
    run_data["diameter"] = [next_diameter]
    nodes = edges.keys()
    run_data["degree"] = [sum([len(edges[n]) for n in nodes]) / float(len(nodes))]
    run_data["duration"] = time.time() - start_time
    # Return the stats for this iteration
    return (pd.DataFrame(run_data), values)


# In[ ]:


def worker(task_queue, result_queue):
    try:
        while True:
            N, K, D, r, steps, sample = task_queue.get_nowait()
            result_queue.put(simulate(N, K, D, r, steps, sample))
            print "Put results for %d %d %d %f" % (N, K, D, r)
            task_queue.task_done()
    except Empty:
        return


# In[ ]:


num_workers = 12
per_rewire = 25
steps = 75
Ns = [500]
Ks = [4]
Ds = [2]
rs = [0.0, 0.33, 0.67, 1.0]
samples = [3]

exp = logbook.Experiment("nk_rewire")

task_queue = Queue()
result_queue = Queue()

for N in Ns:
    for K in Ks:
        for D in Ds:
            for r in rs:
                for sample in samples:
                    for i in range(per_rewire):
                        task_queue.put( (N, K, D, r, steps, sample) )
workers = []
for i in range(num_workers):
    p = Process(target=worker, args=(task_queue, result_queue))
    workers.append(p)
    p.start()
task_queue.join()

df_runs = pd.DataFrame()
conform_values = {}
best_values = {}
loc_conform_values = {}
loc_best_values = {}
loc_conform_unstruct_values = {}
loc_best_unstruct_values = {}
loc_cons_values = {}

try:
    while True:
        run_data, values = result_queue.get_nowait()
        df_runs = df_runs.append(run_data)
        rewire = run_data["rewire"][0]
        try:
            conform_values[rewire].append(values["conform_values"])
            best_values[rewire].append(values["best_values"])
            loc_conform_values[rewire].append(values["loc_conform_values"])
            loc_best_values[rewire].append(values["loc_best_values"])
            loc_conform_unstruct_values[rewire].append(values["loc_conform_unstruct_values"])
            loc_best_unstruct_values[rewire].append(values["loc_best_unstruct_values"])
#            loc_cons_values[rewire].append(values["loc_cons_values"])
        except KeyError:
            conform_values[rewire] = [values["conform_values"]]
            best_values[rewire] = [values["best_values"]]
            loc_conform_values[rewire] = [values["loc_conform_values"]]
            loc_best_values[rewire] = [values["loc_best_values"]]
            loc_conform_unstruct_values[rewire] = [values["loc_conform_unstruct_values"]]
            loc_best_unstruct_values[rewire] = [values["loc_best_unstruct_values"]]
#            loc_cons_values[rewire] = [values["loc_cons_values"]]
except Empty:
    pass


# In[ ]:


df_runs


# In[ ]:


df_runs.to_csv(exp.get_filename("runs.csv"))


# In[ ]:


value_data = {
    "rewire": [],
    "strategy": [],
    "trial": [],
    "step": [],
    "value": [],
}
trial_n = 0
for r, trials in conform_values.iteritems():
    for trial_data in trials:
        for step, value in enumerate(trial_data):
            value_data["rewire"].append(r)
            value_data["strategy"].append("conform")
            value_data["trial"].append(trial_n)
            value_data["step"].append(step)
            value_data["value"].append(value)
        trial_n += 1
for r, trials in best_values.iteritems():
    for trial_data in trials:
        for step, value in enumerate(trial_data):
            value_data["rewire"].append(r)
            value_data["strategy"].append("best")
            value_data["trial"].append(trial_n)
            value_data["step"].append(step)
            value_data["value"].append(value)
        trial_n += 1
for r, trials in loc_conform_values.iteritems():
    for trial_data in trials:
        for step, value in enumerate(trial_data):
            value_data["rewire"].append(r)
            value_data["strategy"].append("loc_conform")
            value_data["trial"].append(trial_n)
            value_data["step"].append(step)
            value_data["value"].append(value)
        trial_n += 1
for r, trials in loc_best_values.iteritems():
    for trial_data in trials:
        for step, value in enumerate(trial_data):
            value_data["rewire"].append(r)
            value_data["strategy"].append("loc_best")
            value_data["trial"].append(trial_n)
            value_data["step"].append(step)
            value_data["value"].append(value)
        trial_n += 1
for r, trials in loc_conform_unstruct_values.iteritems():
    for trial_data in trials:
        for step, value in enumerate(trial_data):
            value_data["rewire"].append(r)
            value_data["strategy"].append("loc_conform_unstruct")
            value_data["trial"].append(trial_n)
            value_data["step"].append(step)
            value_data["value"].append(value)
        trial_n += 1
for r, trials in loc_best_unstruct_values.iteritems():
    for trial_data in trials:
        for step, value in enumerate(trial_data):
            value_data["rewire"].append(r)
            value_data["strategy"].append("loc_best_unstruct")
            value_data["trial"].append(trial_n)
            value_data["step"].append(step)
            value_data["value"].append(value)
        trial_n += 1
df_values = pd.DataFrame(value_data)


# In[ ]:


df_values.to_csv(exp.get_filename("values.csv"))


# In[ ]:




