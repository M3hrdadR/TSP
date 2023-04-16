import random
import copy


class Memetic:
    def __init__(self, number_of_elements, no_generation=200, p_cross_over=0.95,
                 p_mutation=0.2, p_trunc=0.5, no_population=1000,
                 p_stagnancy=0.15, p_baldwin=0.5):
        self.previous_best = [[], 0]
        self.best = []
        self.number_of_generations = no_generation
        self.p_cross_over = p_cross_over
        self.p_mutation = p_mutation
        self.p_trunc = p_trunc
        self.p_stagnancy = p_stagnancy
        self.p_baldwin = p_baldwin
        self.population = list()
        self.evaluation_table = list()
        self.population_size = no_population
        self.making_table(number_of_elements)
        self.initialize_population(number_of_elements)
        return

    def making_table(self, n):
        for i in range(n):
            tmp = []
            self.evaluation_table.append(tmp)
        i = 0
        file = open('input.txt', 'r')
        Lines = file.readlines()
        for line in Lines:
            self.evaluation_table[i] = list(map(int, line.split())).copy()
            i += 1
        return

    def initialize_population(self, n):
        for i in range(self.population_size):
            tmp = list()
            while len(tmp) != n:
                x = random.randint(0, n-1)
                if x not in tmp:
                    tmp.append(x)
            lst = [tmp.copy(), self.evaluation(tmp.copy())]
            self.population.append(lst)
        self.population.sort(key=lambda x: x[1])
        return

    def evaluation(self, lst):
        cost = 0
        for i in range(0, len(lst)-1):
            x = lst[i]
            y = lst[i+1]
            cost += self.evaluation_table[x][y]
        return cost

    def select_parents(self):
        selected = []
        count = 0
        number_different_answer = 0
        different_answer = []
        N = len(self.population) * self.p_trunc * 0.5

        for i in range(int(len(self.population)*self.p_trunc)):
            if self.population[i] not in different_answer:
                different_answer.append(self.population[i])
                number_different_answer += 1
        if N > number_different_answer:
            N = number_different_answer
        while count < N:
            index = random.randint(0, len(self.population) * self.p_trunc)
            if self.population[index] not in selected:
                selected.append(self.population[index])
                count += 1
        return selected

    def order_recombination(self, p1, p2):
        c1 = [0] * len(p1)
        c2 = [0] * len(p2)
        i = random.randint(0, len(p1) - 1)
        j = random.randint(0, len(p1) - 1)
        while i >= j:
            i = random.randint(0, len(p1) - 1)
            j = random.randint(0, len(p1) - 1)
        # print(i, j)
        for k in range(i, j + 1):
            c1[k] = p1[k]
            c2[k] = p2[k]
        index_1 = (j + 1) % len(p1)
        index_2 = (j + 1) % len(p1)
        for k in range(j + 1, len(p1)):
            if p2[k] not in c1:
                c1[index_1] = p2[k]
                index_1 = (index_1 + 1) % len(p1)
            if p1[k] not in c2:
                c2[index_2] = p1[k]
                index_2 = (index_2 + 1) % len(p1)
        for k in range(0, j + 1):
            if p2[k] not in c1:
                c1[index_1] = p2[k]
                index_1 = (index_1 + 1) % len(p1)
            if p1[k] not in c2:
                c2[index_2] = p1[k]
                index_2 = (index_2 + 1) % len(p1)
        return c1, c2

    def cross_over(self, parents):
        used_parents = []
        count = 0
        children = []
        while count < len(parents) // 2:
            i = random.randint(0, len(parents)-1)
            j = random.randint(0, len(parents)-1)
            while i in used_parents or j in used_parents or i == j:
                i = random.randint(0, len(parents) - 1)
                j = random.randint(0, len(parents) - 1)
            p = random.random()
            if p < self.p_cross_over:
                c1, c2 = self.order_recombination(parents[i][0], parents[j][0])
                tmp1 = [c1.copy(), 0]
                tmp2 = [c2.copy(), 0]
                children.append(tmp1.copy())
                children.append(tmp2.copy())
                used_parents.append(i)
                used_parents.append(j)
            count += 1
        return children

    def swap_mutation(self, child):
        mutated = child.copy()
        i = random.randint(0, len(child)-1)
        j = random.randint(0, len(child)-1)
        while i == j:
            i = random.randint(0, len(child) - 1)
            j = random.randint(0, len(child) - 1)
        tmp = mutated[i]
        mutated[i] = mutated[j]
        mutated[j] = tmp
        return mutated

    def mutation(self, chlidren):
        for child in chlidren:
            p = random.random()
            if p < self.p_mutation:
                self.swap_mutation(child[0])
            child[1] = self.evaluation(child[0])
        return chlidren

    def local_search(self, lst):
        best_local = copy.deepcopy(lst)
        for i in range(len(lst)-1):
            for j in range(i+1, len(lst)):
                order = lst[0].copy()
                tmp = order[i]
                order[i] = order[j]
                order[j] = tmp
                tmp = self.evaluation(order)
                if tmp < best_local[1]:
                    best_local[0] = order
                    best_local[1] = tmp
        return best_local

    def memetic_step(self, children):
        children.sort(key=lambda x: x[1])
        for i in range(len(children) // 2):
            tmp = self.local_search(children[i])
            p = random.random()
            if p < self.p_baldwin:
                children[i][1] = tmp[1]
            else:
                children[i] = copy.deepcopy(tmp)
        return children

    def replace(self, children):
        constant = len(self.population) - len(children)
        for i in range(constant, len(self.population)):
            index = i - constant
            self.population[i] = copy.deepcopy(children[index])
        self.population.sort(key=lambda x: x[1])
        self.best = copy.deepcopy(self.population[0])
        return

    def stop(self, n, stagnancy):
        if n >= self.number_of_generations or stagnancy >= int(self.number_of_generations * self.p_stagnancy):
            return True
        return False

    def evolution(self):
        count_generation = 0
        stagnant_no = 0
        while not self.stop(count_generation, stagnant_no):
            selected_parents = self.select_parents()
            children = self.cross_over(selected_parents)
            children = self.mutation(children)
            children = self.memetic_step(children)
            self.replace(children)

            print("iteration =", count_generation, ", best weight =", self.best[1], ", Solution =", self.best[0])
            count_generation += 1
            if self.previous_best[1] == self.best[1]:
                stagnant_no += 1
            else:
                self.previous_best = copy.deepcopy(self.best)
                stagnant_no = 0
        return

