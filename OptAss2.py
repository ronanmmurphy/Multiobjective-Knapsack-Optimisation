'''
Created on 13 Mar 2020

@author: Conor Melody , Ronan Murphy
'''


import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import sys
import matplotlib.pyplot as plt
from deap.benchmarks.tools import hypervolume

""" This function takes a data file and a number (which represents a percentage)
and returns this percentage of the data file as a random sample"""
def read_knapsack_data(f,percent):
    data = numpy.genfromtxt(f, delimiter=" ", dtype=int)
    N_ITEMS, MAX_WEIGHT = data[0] #Number of data points, max weight
    data = data[1:]
    sample_size = int((percent/100)*len(data)) # Creating necessary sample size from input percentage
    samp = numpy.random.choice(len(data), size= sample_size, replace=False) # This is the random sample of data from the original data file, this is where we are varying the population
    
    data_shuff = data[samp] 
    numpy.random.shuffle(samp)
    data[samp] = data_shuff #Shuffling the data
    
    items = {}
    for idx, line in enumerate(data_shuff):
        val, wt = line
        items[idx] = (val, wt)
    return N_ITEMS, MAX_WEIGHT, items

""" This function evaluates an individual (solution) and penalises individuals which 
fail to satisfy the max weight condition """ 
def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        #print(items[item])
        value += items[item][0]
        weight += items[item][1]
    if len(individual) > NBR_ITEMS or weight > MAX_WEIGHT:
        return 0, MAX_WEIGHT- weight # Ensure overweighted bags are dominated
    return value, weight

""" Taken from knapsack_week06_sol""" 
def cxSet(ind1, ind2):
    """Apply a crossover operation on input sets. The first child is the
    intersection of the two sets, the second child is the difference of the
    two sets.
    """
    temp = set(ind1)                # Used in order to keep type
    ind1 &= ind2                    # Intersection (inplace)
    ind2 ^= temp                    # Symmetric Difference (inplace)
    return ind1, ind2
    
""" Taken from knapsack_week06_sol"""     
def mutSet(individual):
    """Mutation that pops or add an element."""
    if random.random() < 0.5:
        if len(individual) > 0:   # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,


# Run this program from the command line using the command
# python OptAss2.py <input filename> <population percentage> <number of generations>
if len(sys.argv) != 4:
    print("usage:python OptAss2.py <input filename> <population percentage> <number of generations> ")
    sys.exit(0)
else:
    input_file = sys.argv[1]
    population_percentage = int(sys.argv[2])
    number_of_generations = int(sys.argv[3])

#print("Input File", input_file)
#print("Population percentage", population_percentage)
#print("Number of Generations", number_of_generations)
    

NBR_ITEMS, MAX_WEIGHT, items = read_knapsack_data(input_file, population_percentage)

NBR_ITEMS = (NBR_ITEMS/100)*population_percentage #Defining initial population size

IND_INIT_SIZE = int(numpy.sqrt(NBR_ITEMS))
#print(IND_INIT_SIZE)
creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0)) # Here we look to minimise weight and maximise value
creator.create("Individual", set, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_item", random.randrange, NBR_ITEMS)

# Structure initializers for individuals in population 
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, IND_INIT_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#setup evaluate, mate, mutate and select methods using defined above. Selects using NSGA2 algorithm
toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)
toolbox.register("select", tools.selNSGA2)


#initalise the hyperparameters, NGEN is scanned in for each test
NGEN = number_of_generations
#100 mutations per generation
MU = 100
#lambda value used in algorithm 
LAMBDA = 100
#probability of new individuals to be similar to parents or mutations
CXPB = 0.9
MUTPB = 0.1
    
hyp = 0 #Initialising the hypervolume

# Here we take the average hypervolume over 10 runs
# with the same parameters to account for variability between runs
for i in range(10):
    pop = toolbox.population(n=MU)
	#pop is the population of mutations
    hof = tools.ParetoFront()
	#hall of fame is the optimal pareto front
	
	#stats for min and max recorded to logbook
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
	#evolutionary algorithm using deap takes in the parameters and outputs the final population and logbook (verbose set to false) 
    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats ,halloffame=hof, verbose = False)
	
	#calculate the hypervolume of pareto front compare with arbitrary point 3000,500 much worse than any other possible value
    print("Hypervolume at iteration {}, {}".format(i, hypervolume(hof, [3000, 500])))
	
	#add all hypervolume results from each run used to get average over 10 runs
    hyp += hypervolume(hof, [3000, 500])
	
	#graph the pareto front for each run and save it to png file
    optimal_front = numpy.array([ind.fitness.values for ind in hof])
    optimal_front = numpy.array(optimal_front)
    plt.scatter(optimal_front[:,0], numpy.negative(optimal_front[:,1]), c="r")
    filename = str(input_file ) +"_" +str(population_percentage)
    plt.savefig("pareto_graph_%s_%s.png" % (str(i), filename))
    plt.close()

#get the average hyper volume over the 10 runs
average_hypervolume = hyp/10

#output this average value to the data file
print("Average hypervolume over 10 runs %f" % average_hypervolume)


#used to plot data in test runs
    
#plot_data = numpy.genfromtxt("knapPI_2_500_1000_1", delimiter=" ", dtype=int)
#N_ITEMS, MAX_WEIGHT = plot_data[0]
#optimal_front = plot_data[1:]
# Use 500 of the 1000 points in the json file
#optimal_front = optimal_front.tolist()
#optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 20))
    
#pop.sort(key=lambda x: x.fitness.values)
   
#hof.sort(key=lambda x: x.fitness.values)
    
    
#front = numpy.array([ind.fitness.values for ind in pop])
#optimal_front = numpy.array([ind.fitness.values for ind in hof])
    
#optimal_front = numpy.array(optimal_front)
#plt.scatter(optimal_front[:,0], numpy.negative(optimal_front[:,1]), c="r")
#plt.scatter(plot_data[:,0], numpy.negative(plot_data[:,1]), c="b")
#plt.axis("tight")
#plt.show()
    
