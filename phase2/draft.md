STUPID FUCKING USELESS DRAFT [SFUD]
===================================

INTRODUCTION
------------
A "Heterogeneous System" is a system with multiple processors with some of them based on different instruction-set architecture (ISA) or micro-architecture. Usually, each processor excels at some aspect and performs poorly at another, and by combining them, we provide the best of each world. 
Heterogeneous systems are more complex than homogeneous ones, because processors have different architectures. That means they need more complex scheduling policies to utilize the different properties efficiently.

THE PROBLEM
-----------
Our goal is to explore the possibility of providing more optimal scheduler policy for heterogeneous systems through 
heuristic parameter optimization methods like different machine learning [1] and/or genetic algorithms [2].
We plan to build a simulation for some popular heterogeneous system, and integrate our optimization technique to 
find better policy for different scenarios.

WHY
---
Because heterogeneous systems are relatively new concept, they lack good support from OS developers, 
and thus their schedulers policies still need more optimizations. 
Recent findings show that they, the heterogeneous systems, can achieve lower energy delay product over homogeneous systems as much as 21%-23% [3]. We assume that with more efficient scheduling they can achieve lower power consumption, and then they can become more economical.

REFERENCES
----------
[1] @article{orhean2018new,
  title={New scheduling approach using reinforcement learning for heterogeneous distributed systems},
  author={Orhean, Alexandru Iulian and Pop, Florin and Raicu, Ioan},
  journal={Journal of Parallel and Distributed Computing},
  volume={117},
  pages={292--302},
  year={2018},
  publisher={Elsevier}
}

* Why this paper: So we get insights into how to use machine learning in achieving better scheduling policies.
* Paper research problem: Heterogeneous systems task scheduling problem.
* Paper goal: Determining a more efficient scheduling policy for heterogeneous systems.
* Tools: BURLAP library, Java RMI API, remote allocated schedulers and WorkflowSim.
* Conclusion: The paper proposed a platform of scheduling solutions as a service based on machine learning agents. 
And found out that reinforcement learning has the limitation of with more nodes the system was incapable of learning optimal policy.

[2] @article{kumar2010genetic,
  title={Genetic algorithm approach to operating system process scheduling problem},
  author={Kumar, Rakesh and Kumar, Er Rajiv and Gill, Er Sanjeev and Kaushik, Er Ashwani},
  journal={International journal of Engineering science and Technology},
  volume={2},
  number={9},
  pages={4247--4252},
  year={2010}
}

* Why this paper: Because we plan to use GA as one of the methods of optimization, which what the paper used,
even though the paper target wasn't heterogeneous systems.
* Paper research problem: General-purpose OS task scheduling problem.
* Paper goal: Optimize scheduling parameters using GA.
* Conclusion: GA’s can provide a highly flexible and user-friendly, near optimal solution to the general job sequencing problem.

[3] @inproceedings{venkat2014harnessing,
  title={Harnessing ISA diversity: Design of a heterogeneous-ISA chip multiprocessor},
  author={Venkat, Ashish and Tullsen, Dean M},
  booktitle={2014 ACM/IEEE 41st International Symposium on Computer Architecture (ISCA)},
  pages={121--132},
  year={2014},
  organization={IEEE}
}

* Why this paper: To understand heterogeneous systems structures.
* Paper research problem: Which one is more power effective, heterogeneous or homogeneous systems?
* Paper goal: prove heterogeneous systems are more power efficient
* Conclusion: heterogeneous systems improves energy efficiency over the most efficient single-ISA design by 23%.