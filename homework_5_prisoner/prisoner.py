import random
from deap import base, creator, tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

YEARS_CC = 1   # both cooperate
YEARS_DD = 3   # both defect
YEARS_DC = 0   # I defect, opponent cooperates (go free)
YEARS_CD = 5   # I cooperate, opponent defects (sucker)
ROUNDS   = 150 # interactions per pairing

POP_SIZE   = 50
NGEN       = 40
CXPB       = 0.7
MUTPB      = 0.2
GENOME_LEN = 5

def betray(my_history, opponent_history, genome):
    """
    Reactive memory-1 strategy: 5-bit genome
      [init, resp(CC), resp(CD), resp(DC), resp(DD)]
    Returns 0 (cooperate) or 1 (defect).
    """
    # First move: no history yet
    if not my_history:
        return genome[0]

    me_last  = my_history[-1]
    opp_last = opponent_history[-1]

    # Four possible last-round cases:
    if me_last == 0 and opp_last == 0:  # CC
        return genome[1]
    elif me_last == 0 and opp_last == 1:  # CD
        return genome[2]
    elif me_last == 1 and opp_last == 0:  # DC
        return genome[3]
    else:  # me_last == 1 and opp_last == 1 (DD)
        return genome[4]


def play_iterated(genome1, genome2, rounds=ROUNDS):
    hist1, hist2 = [], []
    years1 = years2 = 0
    for _ in range(rounds):
        m1 = betray(hist1, hist2, genome1)
        m2 = betray(hist2, hist1, genome2)
        hist1.append(m1)
        hist2.append(m2)
        # assign years based on moves
        if m1 == 0 and m2 == 0:
            years1 += YEARS_CC; years2 += YEARS_CC
        elif m1 == 1 and m2 == 1:
            years1 += YEARS_DD; years2 += YEARS_DD
        elif m1 == 1 and m2 == 0:
            years1 += YEARS_DC; years2 += YEARS_CD
        else:
            years1 += YEARS_CD; years2 += YEARS_DC
    return years1, years2


# Fitness eval
def evaluate_population(pop):
    n = len(pop)
    totals = [0.0]*n

    # Round-robin tournament
    for i in range(n):
        for j in range(i+1, n):
            y1, y2 = play_iterated(pop[i], pop[j])
            totals[i] += y1
            totals[j] += y2

    total_all_rounds = (n-1) * ROUNDS
    for index, individual in enumerate(pop):
        individual.fitness.values = (totals[index] / total_all_rounds,)




toolbox = base.Toolbox()
toolbox.register("attr_bit", random.randint, 0, 1)
toolbox.register(
    "individual",
    tools.initRepeat,
    creator.Individual,
    toolbox.attr_bit,
    GENOME_LEN
)
toolbox.register(
    "population",
    tools.initRepeat,
    list,
    toolbox.individual
)
toolbox.register("mate",   tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate_population)

# ------------ Evolutionary loop ------------
def run_evolution():
    pop = toolbox.population(n=POP_SIZE)
    # Evaluate initial population
    evaluate_population(pop)

    for gen in range(NGEN):
        # Selection and reproduction
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring)) # deep copy

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

        invalid_offspring = []
        for individual in offspring:
            if not individual.fitness.valid:
                invalid_offspring.append(individual)

        if len(invalid_offspring) > 0:
            evaluate_population(offspring) # set fitness to invallids

        # Replace the old population with the new generation
        pop[:] = offspring

        # Collect all fitness values into a list
        fits = []
        for individual in pop:
            fitness_value = individual.fitness.values[0]
            fits.append(fitness_value)
            
        print(f"Gen {gen:2d} — Min avg years: {min(fits):.3f}, "
              f"Mean avg years: {sum(fits)/len(fits):.3f}")

    # Final evaluation and result
    evaluate_population(pop)
    best = tools.selBest(pop, 1)[0]
    print("\nBest evolved genome:", best)
    print("Avg years per round:", best.fitness.values[0])
    return best

if __name__ == "__main__":
    run_evolution()
