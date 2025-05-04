import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools

TARGET_LAKES        = 2       
TARGET_VARIABILITY  = 0.2     
TARGET_FLOOD_RATIO  = 0.7

USE_LAKES           = True
USE_VARIABILITY     = True
USE_FLOOD           = False  

W_LAKE_ERROR        = 1.0
W_VAR_ERROR         = 1.0
W_FLOOD_ERROR       = 1.0

POP_SIZE    = 500
NGEN        = 200
CXPB, MUTPB = 0.7, 0.2
TERRAIN_LEN = 100


# -------- Terrain visualization --------
def plotterrain(t, sea_level=0.5):
    fig, ax = plt.subplots()
    x = range(len(t))
    sea = [sea_level for _ in x]
    ax.fill_between(x, sea, color="turquoise")
    ax.fill_between(x, t,   color="sandybrown")
    ax.axis("off")
    plt.show()

# -------- Fitness evaluation --------
def evaluate_terrain(individual, sea_level=0.5):
    heights = np.array(individual)

    # Count lakes
    below = heights < sea_level
    lakes, sizes, size, in_lake = 0, [], 0, False
    for b in below:
        if b:
            size += 1
            if not in_lake:
                lakes += 1
                in_lake = True
        else:
            if in_lake:
                sizes.append(size)
            size, in_lake = 0, False
    if in_lake:
        sizes.append(size)

    # Variability
    var = float(np.std(heights))

    # Flooded ratio
    flooded_ratio = float(np.mean(below))

    # Compute absolute errors
    err_lakes   = abs(lakes - TARGET_LAKES)
    err_var     = abs(var - TARGET_VARIABILITY)
    err_flood   = abs(flooded_ratio - TARGET_FLOOD_RATIO)

    # Weighted fitness: negative total error (to maximize)
    fitness = -(
        (W_LAKE_ERROR * err_lakes        if USE_LAKES       else 0) +
        (W_VAR_ERROR  * err_var          if USE_VARIABILITY else 0) +
        (W_FLOOD_ERROR* err_flood        if USE_FLOOD       else 0)
    )

    return (fitness,)

# -------- Evolutionary algorithm --------
def run_evolution():


    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list,    fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.random)
    toolbox.register("individual",
                     tools.initRepeat,
                     creator.Individual,
                     toolbox.attr_float,
                     TERRAIN_LEN)
    toolbox.register("population",
                     tools.initRepeat,
                     list,
                     toolbox.individual)

    toolbox.register("evaluate", evaluate_terrain, sea_level=0.5)
    toolbox.register("mate",   tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian,
                     mu=0, sigma=0.1, indpb=0.1)
    toolbox.register("select", tools.selTournament,
                     tournsize=3)

    # Initialize and evaluate population
    pop = toolbox.population(n=POP_SIZE)
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    # Evolution loop
    for gen in range(NGEN):
        # Selection
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        # Crossover
        for c1, c2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(c1, c2)
                del c1.fitness.values, c2.fitness.values
        # Mutation
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Re-evaluate only invalid fitnesses
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid:
            ind.fitness.values = toolbox.evaluate(ind)
        pop[:] = offspring

        # Logging
        fits = [ind.fitness.values[0] for ind in pop]
        print(f"Gen {gen}: Max {max(fits):.3f}, Avg {np.mean(fits):.3f}")

    # Best solution
    best = tools.selBest(pop, 1)[0]
    print("Best fitness:", best.fitness.values[0])
    plotterrain(best)

if __name__ == "__main__":
    run_evolution()
