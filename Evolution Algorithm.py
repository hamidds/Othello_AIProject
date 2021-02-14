import gui
import othello
import random
import numpy as np

UPPERBOUND = 75
LOWERBOUND = -75

ROWS = 8
COLUMNS = 8
RES = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120]
]
POPULATION = []


class Gen:
    def __init__(self, weights, black_score, white_score, gen):
        self.weights = weights
        self.black_score = black_score
        self.white_score = white_score
        self.gen = gen
        self.margin = black_score - white_score
        self.wins = 0

    def set_margin(self, margin):
        self.margin = margin

    def increment(self):
        self.wins += 1

    def __str__(self):
        return self.gen


def new_game(first_player, black_weights, white_weights):
    game = othello.OthelloGame(ROWS, COLUMNS, othello.BLACK, first_player=first_player, black_weights=black_weights,
                               white_weights=white_weights)
    return game


def population_initialization(init):
    for i in range(init):
        gen = random.sample(range(LOWERBOUND, UPPERBOUND), 8)
        current_gen = Gen(create_weights(gen), 0, 0, gen)
        # current_gen.set_margin(i)
        POPULATION.append(current_gen)
    return POPULATION


def fitness_function(gen1, gen2):
    black_weights = gen1.weights
    white_weights = gen2.weights
    print()
    # print(str(gen1.gen) + " VS. " + str(gen2.gen))
    print("                                   " + str(dist(gen1.gen)) + " VS. " + str(dist(gen2.gen)))
    current_game = new_game(othello.BLACK, black_weights, white_weights)
    first_score, second_score = current_game.ai_vs_ai()
    gen1.black_score = gen2.white_score = first_score
    gen1.white_score = gen2.black_score = second_score
    if first_score > second_score:
        return gen1
    else:
        return gen2


def selection(gens, pop):
    selected1 = []
    for i in range(int(pop / 6)):
        winner1, winner2, winner3 = precise_select(gens, i)
        selected1.append(winner1)
        selected1.append(winner2)
        selected1.append(winner3)
    random.shuffle(selected1)
    return selected1


def select(gens, i):
    winner1 = fitness_function(gens[(i * 6) + 0], gens[(i * 6) + 1])
    print("winner1 = " + str(winner1.gen) + " " + str(dist(winner1.gen)))
    winner2 = fitness_function(gens[(i * 6) + 2], gens[(i * 6) + 3])
    print("winner2 = " + str(winner2.gen) + " " + str(dist(winner2.gen)))
    winner3 = fitness_function(gens[(i * 6) + 4], gens[(i * 6) + 5])
    print("winner3 = " + str(winner3.gen) + " " + str(dist(winner3.gen)))
    return winner1, winner2, winner3


def compare_gen(gen1, gen2):
    arr1 = gen1.gen
    arr2 = gen2.gen
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True


def precise_select(gens, i):
    gens_temp = list.copy(gens[(i * 6) + 0:(i * 6) + 6])
    final_opp = []
    # print("Size of gens_temp = " + str(len(gens_temp)))
    for i in range(len(gens_temp)):
        opponent_list = list.copy(gens_temp)
        main_opponent = opponent_list[i]
        final_opp.append(main_opponent)
        main_opponent.wins = 0
        del opponent_list[i]
        for o in range(len(opponent_list)):
            winner = fitness_function(main_opponent, opponent_list[o])
            if compare_gen(winner, main_opponent):
                main_opponent.increment()
        print("Gen " + str(i) + " : " + str(main_opponent.wins) + " wins, Weights = " + str(main_opponent.gen))
    sort = sorted(final_opp, key=lambda x: x.wins, reverse=True)
    print()
    print(sort[0].gen)
    print(sort[1].gen)
    print(sort[2].gen)
    print()
    return sort[0], sort[1], sort[2]


def mutation(crossovered, number):
    for i in range(number):
        p = random.randint(1, 3)
        if p == 1:
            crossovered[i].gen = add_noise(crossovered[i].gen)
        else:
            print("SORT MUTATE")
            crossovered[i].gen.sort()
            crossovered[i].gen.reverse()

    return crossovered


def add_noise(arr1):
    for i in range(len(arr1)):
        noise = random.randint(-15, 30)
        arr1[i] += noise
        if arr1[i] > UPPERBOUND:
            arr1[i] = UPPERBOUND
        if arr1[i] < LOWERBOUND:
            arr1[i] = LOWERBOUND
    return arr1


def crossover(selected, childs):
    values = len(selected)
    temp = selected
    for i in range(childs):
        rand_index = random.sample(range(0, values), 2)
        avr = average(selected[rand_index[0]], selected[rand_index[1]])
        curr_black_score = selected[rand_index[0]].black_score + selected[rand_index[1]].black_score
        curr_white_score = selected[rand_index[0]].white_score + selected[rand_index[1]].white_score
        current_gen = Gen(create_weights(avr), curr_black_score, curr_white_score, avr)
        # current_gen.set_margin(i)
        temp.append(current_gen)
    return temp


def average(gen1, gen2):
    # alpha1 = gen1.margin / (gen1.margin + gen2.margin)
    # alpha2 = gen2.margin / (gen1.margin + gen2.margin)
    arr1 = gen1.gen
    arr2 = gen2.gen
    # avr1 = [x * (alpha1 + 0.001) for x in arr1]
    # avr2 = [x * (alpha2 + 0.001) for x in arr2]
    avr = [sum(x) for x in zip(arr1, arr2)]
    avr = [x / 2 for x in avr]
    return avr


def dist(gen):
    temp = gen
    best = [120, 20, 15, 5, 3, -5, -20, -40]
    sub = [a_i - b_i for a_i, b_i in zip(best, temp)]
    return sum(sub)


def genetic_algorithm(init, pc=1, pm=0.5, epochs=15):
    population = population_initialization(init)

    for epoch in range(epochs):
        print("==================================================================================")
        print("                                  EPOCH " + str(epoch) + "                        ")
        selected = selection(population, init)

        pct = random.uniform(0., 1.)
        if pct <= pc:
            crossovered = crossover(selected, int(init / 2))

        pmt = random.uniform(0., 1.)
        # crossovered_sorted = sorted(crossovered, key=lambda x: x.margin, reverse=False)
        crossovered_sorted = crossovered

        if pmt < pm:
            print("MUTATION IN THIS GEN")
            mutated = mutation(crossovered_sorted, 20)
        else:
            mutated = crossovered_sorted
        print_list(population)
        # population = random.shuffle(mutated)
        population = mutated
        print("==================================================================================")


def create_weights(gen=None):
    if gen is None:
        gen = [120, 20, 3, 4, 5, 6, 7, 8]

    for i in range(8):
        for j in range(8):
            if RES[i][j] == 120:
                RES[i][j] = gen[0]
            if RES[i][j] == 20:
                RES[i][j] = gen[1]
            if RES[i][j] == 15:
                RES[i][j] = gen[2]
            if RES[i][j] == 5:
                RES[i][j] = gen[3]
            if RES[i][j] == 3:
                RES[i][j] = gen[4]
            if RES[i][j] == -5:
                RES[i][j] = gen[5]
            if RES[i][j] == -20:
                RES[i][j] = gen[6]
            if RES[i][j] == -40:
                RES[i][j] = gen[7]

    return RES


def print_list(list):
    for j in range(len(list)):
        # print(str(list[j].gen))
        print(str(list[j].gen) + " Margin = " + str(list[j].margin))
    print()


# crossover(0, 0)
# population_initialization(10)

# print_list(POPULATION)

# res = mutation(POPULATION, 10)
# print_list(res)

# mutation_sorted = sorted(POPULATION, key=lambda x: x.margin, reverse=False)
# print_list(mutation_sorted)

# crossovered_sorted = crossover(POPULATION, 5)
# print_list(crossovered_sorted)

# current_game = othello.OthelloGame(ROWS, COLUMNS, othello.BLACK)
# current_game.ai_vs_ai()

genetic_algorithm(60)

# ss = [4, 2, 3, 4, 5]
# ss2 = [4, 2, 3, 4, 5]
# ss1 = list.copy(ss)
# del ss[0]
# print(ss)
# print(ss1)
# print(ss2.sort() == ss.sort())
