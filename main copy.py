from collections import Counter
import math
from operator import indexOf
from os import path
import random

import numpy as np


class TSP:
    def getNamesOfCities(self, x):
        return x.split(' ')[0]

    def getCoorOfCities(self, x):
        return x.split(' ')[1], x.split(' ')[2]

    def getcityCoordinates(self, lines):
        self.cityNames = list(map(self.getNamesOfCities, lines))
        self.corTupels = list(map(self.getCoorOfCities, lines))
        resultDic = dict(zip(self.cityNames, self.corTupels))
        return resultDic

    def creatPath(self, cities):
        x = np.array(cities)
        pop_group = []
        while len(pop_group) < 100:
            y = np.random.permutation(x)
            if not any((y == x).all() for x in pop_group):
                pop_group.append(y.tolist())

        return pop_group

    def createPopulationList(self, path):
        f = open(path, "r")
        lines = f.read().splitlines()

        self.cityCoordinates = self.getcityCoordinates(lines[3:len(lines) - 1])  # {1: ('41', '49'), 2: ('35', '17')
        self.populationList = []  # [1,2,3,4,5,6,
        self.coordinates = []  # [('41', '49'), ('35', '17'),
        self.populationList=self.creatPath(self.cityNames)
        return self.populationList

    def euclidean_distance(self, p0, p1):
        x = float(p1[0]) - float(p0[0])
        y = float(p1[1]) - float(p0[1])
        return int(math.sqrt((x * x + y * y) + 0.5))

    def getCoordinates(self, pathList):
        coordList = []
        for city in pathList:
            coordList.append(self.cityCoordinates.get(city))

        return coordList

    def fitness(self):
        sum = 0
        coordLists = []
        costList = []
        self.pathes_costes_dic = {}
        for p in self.populationList:
            coordLists.append(self.getCoordinates(p))

        for coordList in coordLists:
            for i in range(0, len(coordList) - 2):
                sum = sum + self.euclidean_distance(coordList[i], coordList[i + 1])
            costList.append(sum)
            sum = 0

        self.pathes_costes_dic = dict(zip(costList, np.array(self.populationList).tolist()))
        return costList

    def selectParnet(self):
        costs = sorted(self.fitness())  ## we are taking the cost from fitness
        self.parents = [self.populationList[costs.index(costs[len(costs) - 2])],
                   self.populationList[costs.index(costs[len(costs) - 1])]]

        return self.parents

    def findMissedCities(self, path):
        return list(set(self.cityNames) - set(path))

    def findDublicated_indexes(self, List):
        '''''
        in this menthod we take the dublicted indexes after cross over 
        '''''
        d1 = {item: list(List).count(item) for item in List}  # item and their counts
        elems = list(filter(lambda x: d1[x] > 1, d1))  # get duplicate elements
        d2 = dict(zip(range(0, len(List)), List))  # each item and their indices
        duplicated_indexes = []
        res = {item: list(filter(lambda x: d2[x] == item, d2)) for item in elems}
        for key in res:
            duplicated_indexes.append(res.get(key)[0])
        return duplicated_indexes

    def crossover(self, path1, path2):
        start = random.randint(0, 101)  # [4,6,7,8]
        end = random.randint(0, 101)  # [4,6,7,8]
        if start == None or end == None:
            self.crossover(self, path1, path2)
        if start > end:
            temp = end
            end = start
            start = temp

        temp = []
        for i in range(start, end):
            temp.append(path2[i])
        path2[start:end], path1[start:end] = path1[start:end], temp  # cross over
        missedcites_list1 = self.findMissedCities(path1)
        missedcites_list2 = self.findMissedCities(path2)
        dublicatedIndexes1 = self.findDublicated_indexes(path1)  # child 1
        dublicatedIndexes2 = self.findDublicated_indexes(path2)  # child 2
        '''  
        1- loop in path1 
        2- stop in duplicated index 
        3- replace the value at duplicated index with elemnent from missed cities list
        '''
        # replacement
        for (index, missed_city) in zip(dublicatedIndexes1, missedcites_list1):
            path1[index] = missed_city
        for (index, missed_city) in zip(dublicatedIndexes2, missedcites_list2):
            path2[index] = missed_city
        self.fitness()
        childs_list = [path1, path2]
        return childs_list

    def best_path(self):
        self.fitness()
        best_path = []
        min_cost = min(self.pathes_costes_dic.keys())
        for key, v in self.pathes_costes_dic.items():
            if key == min_cost:
                best_path = v
                break

        return best_path,min_cost
        
    def inversion_mutation(self,in_list):
        a = random.randint(0, len(in_list) - 1)
        b = random.randint(0, len(in_list) - 1)
        if a < b:
            a = a
            b = b
        elif a > b:
            a = b
            b = a
        else:
            pass
        first, second, third = in_list[:a], in_list[a:b], in_list[b:]
        in_list = first + second[::-1] + third
        return in_list

    def mutation(self, mutation_operator):
        for i in range(0, int(round(mutation_operator, 1) * len(self.populationList))):
            index = random.randint(0, len(self.populationList) - 1)
            if self.populationList[index] == self.parents[0] or self.populationList[index] == self.parents[1]:
                self.mutation( mutation_operator)
            self.populationList[index] = self.inversion_mutation(self.populationList[index])
    def plot_costs(self, generation,costs):
        plt.plot(generation, costs)
 
        # naming the x axis
        plt.xlabel('generation')
        # naming the y axis
        plt.ylabel('costs')
        
        # giving a title to my graph
        plt.title('TSP ')
        
        # function to show the plot
        plt.show()
                                                                           


f = TSP()
f.createPopulationList('Cities Coordinates.tsp')  # puts the file into an arraypr
costs=[]
paths=[]
for i in range(0, 60000):
    mutation_operator = random.uniform(0.1, 1.0)
    lis = f.selectParnet()
    f.crossover(lis[0], lis[1])
    f.mutation(mutation_operator)
    if i == 1000 or i == 2000 or i == 5000:
        print('After ', i, ' generation')
        index=costs.index(min(costs))
        print('best path: ', paths[index],' cost: ', min(costs))
    costs.append(f.best_path()[1])
    paths.append(f.best_path()[0])