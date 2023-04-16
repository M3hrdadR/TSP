from numpy.random import choice
import random
class Ant:
    def __init__(self):
        self.path = list()
        self.fitness = 0
        return


class AS:
    def __init__(self, no_vertex, no_ants, alpha=0.7, beta=0.7, rho=0.6, no_iteration=100):
        self.no_iteration = no_iteration
        self.no_vertex = no_vertex
        self.no_ants = no_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.pheromones_table = list()
        self.weight_table = list()
        self.initializing_weight()
        self.initial_tau()
        self.initializing_pheromone_table()
        self.best_path = []
        return

    def initial_tau(self):
        v = 0
        path = []
        path.append(v)
        cost = 0
        while len(path) != self.no_vertex:
            tmp = self.weight_table[v]
            mx = max(tmp)
            for w in path:
                tmp[w] = mx + 1
            cost += min(tmp)
            v = tmp.index(min(tmp))
            path.append(v)
        self.tau = self.no_ants/cost
        return

    def initializing_pheromone_table(self):
        for i in range(self.no_vertex):
            a = list()
            self.pheromones_table.append(a)
            for j in range(self.no_vertex):
                self.pheromones_table[i].append(self.tau)
        return

    def initializing_weight(self):
        for i in range(self.no_vertex):
            tmp = []
            self.weight_table.append(tmp)
        i = 0
        file = open('input.txt', 'r')
        lines = file.readlines()
        for line in lines:
            self.weight_table[i] = list(map(int, line.split())).copy()
            i += 1
        return

    def find_next(self, path):
        possible_vertex = []
        for i in range(self.no_vertex):
            if i not in path:
                possible_vertex.append(i)
        v = path[-1]
        probability_list = []
        for w in possible_vertex:
            p = pow(self.pheromones_table[v][w], self.alpha)
            p *= pow(1/self.weight_table[v][w], self.beta)
            probability_list.append(p)
        # this is just because of limitations of numpy
        s = 0
        for p in probability_list:
            s += p
        for i in range(len(probability_list)):
            probability_list[i] *= 1/s
        num = choice(possible_vertex, 1, p=probability_list)
        return num[0]

    def constructing_path(self, ants):
        for k in range(len(ants)):
            x = random.randint(0, self.no_vertex-1)
            ants[k].path.append(x)
            while len(ants[k].path) != self.no_vertex:
                x = self.find_next(ants[k].path)
                ants[k].path.append(x)

        return

    def vaporization(self):
        for i in range(len(self.pheromones_table)):
            for j in range(len(self.pheromones_table[0])):
                self.pheromones_table[i][j] = (1-self.rho) * self.pheromones_table[i][j]
                # self.pheromones_table[i][j] = round(self.pheromones_table[i][j], 4)
        return

    def fitness(self, path):
        sum = 0
        for i in range(len(path)-1):
            v = path[i]
            w = path[i + 1]
            sum += self.weight_table[v][w]
        return sum

    def evaluation(self, ants):
        for ant in ants:
            ant.fitness = self.fitness(ant.path)
        return

    def affecting_pheromones(self, ants):
        for ant in ants:
            delta = 100 / ant.fitness
            for i in range(len(ant.path) - 1):
                v = ant.path[i]
                w = ant.path[i+1]
                self.pheromones_table[v][w] += delta
                # self.pheromones_table[v][w] = round(self.pheromones_table[v][w], 4)

        return

    def find_best_path(self):
        v = 0
        path = []
        path.append(v)
        while len(path) != self.no_vertex:
            tmp = self.pheromones_table[v].copy()
            for v in path:
                tmp[v] = -100
            index = 0
            max = tmp[0]
            for i in range(len(tmp)):
                if tmp[i] > max:
                    index = i
                    max = tmp[i]
            v = index
            path.append(index)
        return path

    def My_print(self, path, iteration):
        print("number of iteration =", iteration, "| path =", end=" ")
        for x in path:
            print(x, end=" ")
        print("| fitness =", self.fitness(path))
        print("----------------------")
        return

    def stop_condition(self, iter, stag):
        if stag > self.no_iteration / 10 or iter >= self.no_iteration:
            return True
        return False

    def main_loop(self):
        iteration = 0
        stag = 0
        best_path = []
        while not self.stop_condition(iteration, stag):
            ants = list()
            for i in range(self.no_ants):
                ants.append(Ant())
            self.constructing_path(ants)
            self.vaporization()
            self.evaluation(ants)
            self.affecting_pheromones(ants)
            best_path = self.find_best_path()

            if best_path == self.best_path:
                stag += 1
            else:
                stag = 0
                self.best_path = best_path.copy()
            self.My_print(best_path, iteration)
            iteration += 1
        return
