
# coding: utf-8

# In[ ]:


get_ipython().magic(u'pylab inline')
import sys
import numpy as np
import pandas as pd
import scipy.stats as spstats
import elp_networks.algorithms as elpalg
import elp_nkmodel as elpnk
import net
import simulator

import strategy


# In[ ]:


N = 2000
K = 3
D = 1
rewire_values = 5
per_rewire = 50

conform_perf = []
best_perf = []
loc_cons_perf = []
loc_conform_perf = []
diameter = []
meanpath = []
degree = []
rewire = []
best_values = []
conform_values = []
loc_cons_values = []
loc_conform_values = []

for r in range(rewire_values):
    r = float(r) / float(rewire_values - 1)
    for i in range(per_rewire):
        rewire.append(r)
        print "Rewire %f" % r
        m = elpnk.NK(N, K)
        # Generate network from NK structure
        edges_node_loc = net.nk_to_affiliation(m, D)
        if rewire > 0:
            net.rewire_affiliation(m, edges_node_loc, r)
        edges = net.affiliation_to_node(edges_node_loc)
        # Create strategies
        best_ind_strat = strategy.BestNeighborIndividual(m, edges, sample=3)
        conform_ind_strat = strategy.ConformityIndividual(m, edges, sample=3)
        loc_ind_cons_strat = strategy.LocalIndividualConsensus(m, edges_node_loc)
        loc_conform_ind_strat = strategy.LocalConformityIndividual(m, edges_node_loc, sample=3)
        sys.stdout.write("  Step %d: " % i)
        sys.stdout.write("best-neighbor... ")
        sys.stdout.flush()
        sim = simulator.Simulator(m, edges, best_ind_strat)
        sim.run(50)
        best_perf.append(sim.values[-1])
        best_values.append(sim.values)
        sys.stdout.write("conformity... ")
        sys.stdout.flush()
        sim = simulator.Simulator(m, edges, conform_ind_strat)
        sim.run(50)
        conform_perf.append(sim.values[-1])
        conform_values.append(sim.values)
        sys.stdout.write("loc-consensus... ")
        sys.stdout.flush()
        sim = simulator.Simulator(m, edges, loc_ind_cons_strat)
        sim.run(50)
        loc_cons_perf.append(sim.values[-1])
        loc_cons_values.append(sim.values)
        sys.stdout.write("loc-conformity... ")
        sys.stdout.flush()
        sim = simulator.Simulator(m, edges, loc_conform_ind_strat)
        sim.run(50)
        loc_conform_perf.append(sim.values[-1])
        loc_conform_values.append(sim.values)
        sys.stdout.write("diameter... ")
        sys.stdout.flush()
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
        meanpath.append(float(total_path) / float(path_count))
        diameter.append(next_diameter)
        nodes = edges.keys()
        degree.append(sum([len(edges[n]) for n in nodes]) / float(len(nodes)))
        sys.stdout.write("done\n")
        sys.stdout.flush()


# In[1]:


meanpath


# In[ ]:


df = pd.DataFrame({
    "rewire": rewire,
    "degree": degree,
    "mean_path": meanpath,
    "diameter": diameter,
    "conform_perf": conform_perf,
    "best_perf": best_perf,
    "loc_cons": loc_cons_perf,
    "loc_conform": loc_conform_perf
})
df.to_csv("local.csv")


# In[ ]:


print "Degree"
print [min(degree), np.mean(degree), max(degree)]
print np.std(degree)
print "Best-neighbor"
print [min(best_perf), np.mean(best_perf), max(best_perf)]
print np.std(best_perf)
print np.std(best_perf)/sqrt(float(len(best_perf)))
print "Conformity"
print [min(conform_perf), np.mean(conform_perf), max(conform_perf)]
print np.std(conform_perf)
print np.std(conform_perf)/sqrt(float(len(conform_perf)))


# In[ ]:


plt.figure(figsize=(16,20))
for i in range(5):
    r = float(i) / 4.0
    plt.subplot(5,4,1+i*4)
    plt.title("Best Neighbor")
    plt.ylabel("Rewire = %0.2f" % r)
    for v in best_values[i*20:(i+1)*20]:
        plot(v)
    plt.ylim([0.5,0.8])
    plt.subplot(5,4,2+i*4)
    plt.title("Conformity")
    for v in conform_values[i*20:(i+1)*20]:
        plot(v)
    plt.ylim([0.5,0.8])
    plt.subplot(5,4,3+i*4)
    plt.title("Local Consensus")
    for v in loc_cons_values[i*20:(i+1)*20]:
        plot(v)
    plt.ylim([0.5,0.8])
    plt.subplot(5,4,4+i*4)
    plt.title("Local Conformity")
    for v in loc_conform_values[i*20:(i+1)*20]:
        plot(v)
    plt.ylim([0.5,0.8])
plt.tight_layout()


# In[ ]:


plt.figure(figsize=(20,4))
for i in range(5):
    r = float(i) / 4.0
    plt.subplot(1,5,1+i)
    plt.title("Mean perf, n=20, rewire=%0.2f" % r)
    plot([np.mean(x) for x in zip(*best_values[i*20:(i+1)*20])], label="best")
    plot([np.mean(x) for x in zip(*conform_values[i*20:(i+1)*20])], label="conform")
    plot([np.mean(x) for x in zip(*loc_cons_values[i*20:(i+1)*20])], label="loc consensus")
    plot([np.mean(x) for x in zip(*loc_conform_values[i*20:(i+1)*20])], label="loc conform")
    plt.ylim([0.5,0.8])
    plt.legend()
plt.tight_layout()


# In[ ]:


plot(df["degree"], df["mean_path"], '.')


# In[ ]:


plt.figure(figsize=(16,20))
for i in range(5):
    pr = float(i) / 4.0
    plt.subplot(5,4,1+i*4)
    plot(degree[i*20:(i+1)*20], best_perf[i*20:(i+1)*20], '.')
    r,p = spstats.pearsonr(degree[i*20:(i+1)*20], best_perf[i*20:(i+1)*20])
    plt.title("Best Neighbor, r=%0.2f p=%0.4f" % (r,p))
    plt.ylabel("Rewire = %0.2f" % pr)
    plt.xlabel("Degree")
    plt.subplot(5,4,2+i*4)
    plot(degree[i*20:(i+1)*20], conform_perf[i*20:(i+1)*20], '.')
    r,p = spstats.pearsonr(degree[i*20:(i+1)*20], conform_perf[i*20:(i+1)*20])
    plt.title("Conformity, r=%0.2f p=%0.4f" % (r,p))
    plt.xlabel("Degree")
    plt.subplot(5,4,3+i*4)
    plot(degree[i*20:(i+1)*20], loc_cons_perf[i*20:(i+1)*20], '.')
    r,p = spstats.pearsonr(degree[i*20:(i+1)*20], loc_cons_perf[i*20:(i+1)*20])
    plt.title("Local Consensus, r=%0.2f p=%0.4f" % (r,p))
    plt.xlabel("Degree")
    plt.subplot(5,4,4+i*4)
    plot(degree[i*20:(i+1)*20], loc_conform_perf[i*20:(i+1)*20], '.')
    r,p = spstats.pearsonr(degree[i*20:(i+1)*20], loc_conform_perf[i*20:(i+1)*20])
    plt.title("Local Conformity, r=%0.2f p=%0.4f" % (r,p))
    plt.xlabel("Degree")
plt.tight_layout()


# In[ ]:


plt.figure(figsize=(16,4))
plt.subplot(1,4,1)
plot(degree, best_perf, '.')
r,p = spstats.pearsonr(degree, best_perf)
plt.title("Best Neighbor, r=%0.2f p=%0.4f" % (r,p))
plt.xlabel("Degree")
plt.subplot(1,4,2)
plot(degree, conform_perf, '.')
r,p = spstats.pearsonr(degree, conform_perf)
plt.title("Conformity, r=%0.2f p=%0.4f" % (r,p))
plt.xlabel("Degree")
plt.subplot(1,4,3)
plot(degree, loc_cons_perf, '.')
r,p = spstats.pearsonr(degree, loc_cons_perf)
plt.title("Local Consensus, r=%0.2f p=%0.4f" % (r,p))
plt.xlabel("Degree")
plt.subplot(1,4,4)
plot(degree, loc_conform_perf, '.')
r,p = spstats.pearsonr(degree, loc_conform_perf)
plt.title("Local Conformity, r=%0.2f p=%0.4f" % (r,p))
plt.xlabel("Degree")
plt.tight_layout()


# In[ ]:


plt.plot(rewire, meanpath)


# In[ ]:




