
# coding: utf-8

# In[ ]:

from multiprocessing import Process
from multiprocessing import JoinableQueue as Queue
import os
from Queue import Empty
import random
import sys
import time
import traceback
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

num_workers = 4
per_rewire = 5
steps = 300
Ns = [250]
Ks = [7]
Ds = [2]
rs = [float(x) / 6.0 for x in range(7)]
keep = [1.0]
samples = [0]

methods = [
    "conform", "best",
    "loc_conform", "loc_best",
#    "loc_conform_unstruct", "loc_best_unstruct",
    "loc_cons"
]

uid = str(int(time.time()))

exp_name = "nk_rewire"
try:
    job_id = os.environ["PBS_ARRAYID"]
    exp_name = exp_name
except KeyError:
    job_id = 0
exp = logbook.Experiment(exp_name, suffix=str(job_id))
log = exp.get_logger()


# In[ ]:

def values_to_efficiency(values):
    start = values[0]
    halfmax = (max(values) - start) / 2.0 + start
    return 1.0 / float(len([v for v in values if v <= halfmax]))


# In[ ]:

def simulate(N, K, D, rewire, keep, steps=50, sample=3):
    start_time = time.time()
    run_data = {"N": N, "K":K, "D":D, "rewire":rewire, "keep":keep, "steps":steps, "sample":sample}
    values = {}
    model = elpnk.NK(N, K)
    # Generate network from NK structure
    edges_node_loc, nodes = net.nk_to_affiliation(model, D)
    if rewire > 0:
        net.rewire_affiliation(model, edges_node_loc, rewire)
    edges = net.affiliation_to_node(edges_node_loc)
    if keep < 1.0:
        edges = net.sample_edges(edges, keep)
        
    # Create strategies
    if "best" in methods:
        best_ind_strat = strategy.BestNeighborIndividual(model, nodes, edges, sample)
    if "conform" in methods:
        conform_ind_strat = strategy.ConformityIndividual(model, nodes, edges, sample)
    if "loc_conform" in methods:
        loc_conform_ind_strat = strategy.LocalConformityIndividual(model, nodes, edges_node_loc, sample)
    if "loc_best" in methods:
        loc_best_ind_strat = strategy.LocalBestNeighborIndividual(model, nodes, edges_node_loc, sample)
    if "loc_conform_unstruct" in methods:
        loc_conform_unstructured = strategy.LocalConformityIndividual(model, nodes, edges_node_loc, sample, False)
    if "loc_best_unstruct" in methods:
        loc_best_unstructured = strategy.LocalBestNeighborIndividual(model, nodes, edges_node_loc, sample, False)
    if "loc_cons" in methods:
        loc_cons = strategy.LocalIndividualConsensus(model, nodes, edges_node_loc, sample)
    
    # Simulate strategies
    if "best" in methods:
        sim = simulator.Simulator(model, nodes, edges, best_ind_strat)
        sim.run(steps)
        run_data["best_perf"] = sim.values[-1]
        run_data["best_eff"] = values_to_efficiency(sim.values)
        values["best"] = sim.values
    
    if "conform" in methods:
        sim = simulator.Simulator(model, nodes, edges, conform_ind_strat)
        sim.run(steps)
        run_data["conform_perf"] = sim.values[-1]
        run_data["conform_eff"] = values_to_efficiency(sim.values)
        values["conform"] = sim.values
    
    if "loc_conform" in methods:
        sim = simulator.Simulator(model, nodes, edges, loc_conform_ind_strat)
        sim.run(steps)
        run_data["loc_conform_perf"] = sim.values[-1]
        run_data["loc_conform_eff"] = values_to_efficiency(sim.values)
        values["loc_conform"] = sim.values
    
    if "loc_best" in methods:
        sim = simulator.Simulator(model, nodes, edges, loc_best_ind_strat)
        sim.run(steps)
        run_data["loc_best_perf"] = sim.values[-1]
        run_data["loc_best_eff"] = values_to_efficiency(sim.values)
        values["loc_best"] = sim.values
    
    if "loc_conform_unstruct" in methods:
        sim = simulator.Simulator(model, nodes, edges, loc_conform_unstructured)
        sim.run(steps)
        run_data["loc_conform_unstruct_perf"] = sim.values[-1]
        run_data["loc_conform_unstruct_eff"] = values_to_efficiency(sim.values)
        values["loc_conform_unstruct"] = sim.values
    
    if "loc_best_unstruct" in methods:
        sim = simulator.Simulator(model, nodes, edges, loc_best_unstructured)
        sim.run(steps)
        run_data["loc_best_unstruct_perf"] = sim.values[-1]
        run_data["loc_best_unstruct_eff"] = values_to_efficiency(sim.values)
        values["loc_best_unstruct"] = sim.values
    
    if "loc_cons" in methods:
        sim = simulator.Simulator(model, nodes, edges, loc_cons)
        sim.run(steps)
        run_data["loc_cons_perf"] = sim.values[-1]
        run_data["loc_cons_eff"] = values_to_efficiency(sim.values)
        values["loc_cons"] = sim.values
    
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
    run_data["meanpath"] = float(total_path) / float(path_count)
    run_data["diameter"] = next_diameter
    nodes = edges.keys()
    run_data["degree"] = sum([len(edges[n]) for n in nodes]) / float(len(nodes))
    run_data["duration"] = time.time() - start_time
    # Return the stats for this iteration
    return (run_data, values)


# In[ ]:

def worker(task_queue, result_queue):
    try:
        while True:
            N, K, D, r, k, steps, sample = task_queue.get_nowait()
            try:
                result_queue.put(simulate(N, K, D, r, k, steps, sample))
            except IndexError:
                print N, K, D, r, k, steps, sample
            except KeyError:
                print N, K, D, r, k, steps, sample
            task_queue.task_done()
    except Empty:
        return


# In[ ]:

start_time = time.time()

task_queue = Queue()
result_queue = Queue()

total_tasks = 0

for i in range(per_rewire):
    for N in Ns:
        for K in Ks:
            for D in Ds:
                for sample in samples:
                    for r in rs:
                        for k in keep:
                            if num_workers > 1:
                                task_queue.put( (N, K, D, r, k, steps,sample) )
                            else:
                                result_queue.put(simulate(N, K, D, r, k, steps,sample))
                            total_tasks += 1
if num_workers > 1:
    workers = []
    for i in range(num_workers):
        p = Process(target=worker, args=(task_queue, result_queue))
        workers.append(p)
        p.start()

conform_values = {}
best_values = {}
loc_conform_values = {}
loc_best_values = {}
loc_conform_unstruct_values = {}
loc_best_unstruct_values = {}
loc_cons_values = {}

f_runs = open(exp.get_filename("runs.csv"), "wb")
f_values = open(exp.get_filename("values.csv"), "wb")
runs_written = 0
values_written = 0
values_columns = ["rewire", "keep", "strategy", "trial", "step", "value", "sample"]

tasks_complete = 0
while tasks_complete < total_tasks:
    try:
        run_data, values = result_queue.get()
        rewire = run_data["rewire"]
        runs_columns = list(run_data.keys())
        run_id = uid + "-" + str(job_id) + "-" + str(runs_written)
        if runs_written == 0:
            # Write index
            f_runs.write(",")
            f_values.write(",")
            # Write column headers
            f_runs.write(",".join(runs_columns) + "\n")
            f_values.write(",".join(values_columns) + "\n")
        # Write values data
        for k in methods:
            for step, value in enumerate(values[k]):
                d = [
                    run_id + '-' + str(values_written),
                    repr(run_data["rewire"]),
                    repr(run_data["keep"]),
                    k,
                    run_id,
                    repr(step),
                    repr(value),
                    repr(run_data["sample"])]
                f_values.write(",".join(d) + "\n")
                values_written += 1
        # Write run data
        runs_v = [repr(run_data[k]) for k in runs_columns]
        f_runs.write(run_id + ",")
        f_runs.write(",".join(runs_v) + "\n")
        f_runs.flush()
        f_values.flush()
        runs_written += 1
        tasks_complete += 1
        log.info("%d of %d complete" % (tasks_complete, total_tasks))
    except Empty:
        break
    except:
        traceback.print_exc()
        break
f_runs.close()
f_values.close()

print "Completed in %s seconds" % repr(time.time() - start_time)


# In[ ]:



