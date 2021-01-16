# Multiobjective-Knapsack-Optimisation
Multiobjective optimisation using Black-Box approaches to solve Knapsack problem. 

Implemented Evolutionary Algorithm NSGA-II which is the second edition of Non-Sorting Genetic dominated Algorithm developed by DEAP, to optimise objective. DEAP library is a novel evolutionary computation framework for rapid prototyping and testing of ideas. Selection of Hyperparameters for Crossover, Mutation, Lambda, Number of Generations and Selection proved very important when finding best solution for HyperVolume. The HyperVolume indicator is the method that different solutions are compared for the knapsack problem. This involves choosing a possible solution or “reference point” much worse than any possible solution for all objectives and calculating the corresponding volume between this point and the associated Pareto front of optimal values obtained by an optimisation algorithm to the knapsack problem.

Many different tests were run to compare the output of different hyperparamters. The best configuration is neither a tiny population (and many generations) nor a huge population (and few generations). The best in this case is somewhere in between, but nearer to the small population end, eg population = 100 and 5000 generations.
Example of Pareto Front Output:

![pareto front](https://github.com/ronanmmurphy/Multiobjective-Knapsack-Optimisation/blob/main/Images/pareto_graph_6_knapPI_2_500_1000_1_100.png?raw=true)



Used taskfarming on ICHEC (Irish Center for High-End Computing) to run code. 
