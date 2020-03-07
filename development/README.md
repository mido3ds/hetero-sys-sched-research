# Heterogeneous Systems Scheduling Research   

This folder contains the code for all experiments.

### Introduction

Job Scheduling in Heterogeneous Systems (HeDCS) are divided into two main categories based on their target metric:

- Application-Specific: where target is job execution speed (performance).
- System-Specific: where target is resource utilization.

### Paper Goal

Recursive approximation of static/local scheduling policies of heterogeneous systems (HeDCS).

### Baseline

The proposed methods are to be compared to Heterogeneous Earliest Finish Time (HEFT) algorithm, which is a well-established widely-used algorithm for HeDCS scheduling. It's a static local scheduling algorithm, where inputs are DAG of the jobs to be scheduled, set of machines, the running time of each job on each machine and the time of communicating the results to the children jobs.

### Experiments 

##### Neural Networks

The main contribution of the paper. The proposed network approximates the scheduling algorithms much faster. It takes as an input the machines specs and the jobs specs and generates for each job: a machine to run on, the actual start time and the actual finish time. We have included an implementation to the proposed architecture in this repo.

##### Genetic Algorithms

Another method for recursive approximation. The input to such algorithm is a DAG of the jobs to be scheduled, set of machines and the running time of each job on each machine. It's an online optimization process, so it takes a lot more time than trained neural networks. 

##### Reinforcement Learning [OPTIONAL]
Q-Learning.
