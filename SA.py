import random
import copy
import math


class SA:
    def __init__(self, no_vertex, T=200, no_iterations=500, p_stagnancy=0.1):
        self.T_0 = T
        self.no_iteration = no_iterations
        self.p_stagnancy = p_stagnancy
        self.no_vertex = no_vertex
        self.weight_table = []
        self.initializing_weight()
        self.previous = []
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

    def evaluation(self, lst):
        cost = 0
        for i in range(0, len(lst)-1):
            x = lst[i]
            y = lst[i+1]
            cost += self.weight_table[x][y]
        return cost

    def schedule(self, t):
        T = self.T_0 - self.T_0/self.no_iteration * t
        return T

    def probablity(self, E, E_prime, T):
        if E_prime <= E:
            return 1
        else:
            return pow(math.e, -1*(E_prime-E)/T)

    def find_neighbour(self, lst):
        ngb = []
        for i in range(0, len(lst)-1):
            tmp = lst.copy()
            a = tmp[i+1]
            tmp[i+1] = tmp[i]
            tmp[i] = a
            neighbour = [tmp, self.evaluation(tmp)]
            ngb.append(neighbour)
        return ngb

    def stop(self, n, stagnancy):
        if n >= self.no_iteration or stagnancy >= int(self.no_iteration * self.p_stagnancy):
            return True
        return False

    def my_print(self, i, curr):
        print("iteration =", i, "| best value =", curr[1], "| Solution =", curr[0])
        return

    def main_loop(self):
        lst = []
        while len(lst) != self.no_vertex:
            x = random.randrange(0, self.no_vertex)
            if x not in lst:
                lst.append(x)
        curr = [lst, self.evaluation(lst)]
        self.previous = curr
        stagnant_no = 0
        count_generation = 0
        while not self.stop(count_generation, stagnant_no):
            T = self.schedule(count_generation)
            ngb = self.find_neighbour(curr[0])
            next = ngb[random.randrange(0, len(ngb))]
            if self.probablity(curr[1], next[1], T) >= random.random():
                curr = next
            self.my_print(count_generation, curr)
            count_generation += 1
            if self.previous[1] == curr[1]:
                stagnant_no += 1
            else:
                self.previous = copy.deepcopy(curr)
                stagnant_no = 0
