# NK-Net-Learn
Social learning on the NK Model. Used in (Platt & Romero, 2018).

## Overview
These jupyter notebooks create an NK model (Kauffman & Levin, 1987) and
run repeated trials of agent-based simulations to evaluate the effectiveness of
several social learning strategies. These notebooks use "concern-based networks"
in which the network between agents is generated from particular NK loci and
their neighbors. In some trials, the connections are rewired to vary the
degree distribution. The main scripts support parallel processing using the
`multiprocessing` library.

## Scripts

### NK Net Learn MP
This is the main script that generates NK models and runs agent-based simulations.
Several parameters can be adjsted, including: sampling, rewiring, strategies,
iterations per trial, total trials.

### Plot NK Network
This notebook uses the output of the above file to generate the plots used in the
publication.

### Plot NK Network NoSample
Plots results for trials without sampling. Used as a robustness check.

### Plot NK Network Delete
Plot results for trials where edges are deleted instead of rewired.
Used as a robustness check.

### Plot NK Network Delete NoSample
Plots results for trials where edges are deleted instead of rewired and
where no sampling is used. Useed as a robustness check.

### simulator.py
Defines a `Simulator` class which can run an agent based simulation given an NK model and
learning strategy.

### strategy.py
Defines classes for each learning strategy.

### net.py
Utility functions for sampling and rewiring networks.

## References
* Platt, E. L., & Romero, D. M. (2015).
"Network Structure, Efficiency, and Performance in WikiProjects."
In _ICWSM_.
* Kauffman, S., & Levin, S. (1987).
Towards a general theory of adaptive walks on rugged landscapes.
_Journal of theoretical Biology_, 128(1), 11-45.