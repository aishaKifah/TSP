from collections import Counter
import math
from operator import indexOf
from os import path
import random


import numpy as np 

class TSP:


    def getNamesOfCities(self , x):
        ## takes 1 line of file and return citieis as 1,2,3,4 ##
        return x.split(' ')[0]
    def getCoorOfCities(self , x):
        ## takes  1 line of file and returns coordinates as tuples ##
        return x.split(' ')[1],x.split(' ')[2]
   

    def getcityCoordinates(self,lines):
        ## takes lines and creats dictionary with key=city name value= coordinats##
        count=0
        self.cityNames= list(map(self.getNamesOfCities,lines))
        self.corTupels= list(map(self.getCoorOfCities,lines))
        resultDic = dict(zip(self.cityNames, self.corTupels))
        return resultDic
         
        
    def creatPath(self,cities):
        ## takes path and return permutated list of it ##
        return np.random.permutation(cities)



    
    def createPopulationList(self, path):
        f = open(path, "r")
        lines=f.read().splitlines()
       
        self.cityCoordinates=self.getcityCoordinates(lines[3:len(lines)-1]) # {1: ('41', '49'), 2: ('35', '17')
        self.populationList=[] #[1,2,3,4,5,6,
        count=0
        for x in range(0,100):
            self.populationList.append(self.creatPath(self.cityNames))
            
  

        self.coordinates=[] # [('41', '49'), ('35', '17'),

        return self.populationList

    def euclidean_distance(self,p0, p1):
        x = float(p1[0]) - float(p0[0])
        y = float(p1[1]) - float(p0[1])
        return int(math.sqrt((x * x + y * y) + 0.5))

    def getCoordinates(self,pathList):
            coordList=[]
            for city in pathList:
                coordList.append(self.cityCoordinates.get(city))

            return coordList

                
    
    def fitness(self):
        sum=0
        coordLists=[]
        costList=[]
        self.pathes_costes_dic={}
        for p in  self.populationList:
            coordLists.append(self.getCoordinates(p))

        for coordList in coordLists:
            for i in range(0,len(coordList)-2):
               # print(coordList[i],' ',coordList[i+1])
                sum=sum+self.euclidean_distance(coordList[i],coordList[i+1])
            costList.append( sum)  
            sum=0
 
        self.pathes_costes_dic=dict(zip(  costList,np.array(self.populationList ).tolist()))


        #print(costList)
        #print(self.populationList[costList.index(min(costList))])
        #print(min(costList))
        return costList

    def selectParnet(self):
        costs=sorted(self.fitness()) ## we are taking the cost from fitness
        parnets=[self.populationList[costs.index(costs[len(costs)-2])],self.populationList[costs.index(costs[len(costs)-1])]]
        
        #print(self.populationList[costs.index(costs[len(costs)-2])])
        #print(self.populationList[costs.index(costs[len(costs)-1])])
        return parnets
    def findMissedCities(self,path):
        return list(set(self.cityNames) - set(path))
        
    def findDublicated_indexes(self,List):
        '''''
        in this menthod we take the dublicted indexes after cross over 
        '''''
        d1 = {item:list(List).count(item) for item in List}  # item and their counts
        elems = list(filter(lambda x: d1[x] > 1, d1))  # get duplicate elements
        d2 = dict(zip(range(0, len(List)), List))  # each item and their indices
        duplicated_indexes=[]
        # item and their list of duplicate indices
        res = {item: list(filter(lambda x: d2[x] == item, d2)) for item in elems}
        for key in res:
            duplicated_indexes.append(res.get(key)[0])
        return duplicated_indexes

    def crossover(self,path1,path2):

        #print('cost parnet 1 befor cross over :',list(self.pathes_costes_dic.keys())[list(self.pathes_costes_dic.values()).index(path1)])
        #print('cost parnet 2 befor cross over :',list(self.pathes_costes_dic.keys())[list(self.pathes_costes_dic.values()).index(path2)])
        #print(path1)
       # index = self.populationList.index(path1)
       # print('The index of disney+ is:', index)
        #if len(self.populationList) > 0 and len(self.populationList[0]) > 0:
          #  print('First Index of element with value 15 is ', self.populationList[0][0])
       # keys_list = list(self.pathes_costes_dic)
       # key = keys_list[int(self.populationList[0][0])]
       # print(key)
       # print(self.pathes_costes_dic.get(key))
        
        for key,v in self.pathes_costes_dic.items():
            if v==list(path1) or v==list(path2):
                print(key ,' ', v)

        start=random.randint(1,102)# [4,6,7,8]
        end=random.randint(1,102)# [4,6,7,8]
        if start==None or end==None:
            self.crossover(self,path1,path2)
        if start>end:
            temp=end
            end=start
            start=temp

        temp=[]
        for i in range(start,end):
            temp.append(path2[i])
        path2[start:end], path1[start:end] = path1[start:end], temp # cross over
        missedcites_list1=self.findMissedCities(path1) 
        missedcites_list2=self.findMissedCities(path2)
        dublicatedIndexes1=self.findDublicated_indexes(path1)# child 1 
        dublicatedIndexes2=self.findDublicated_indexes(path2)# child 2
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
        print('###################################')
        self.fitness()
        childs_list=[path1,path2]
        print('child1: ',childs_list[0])
        print('child2: ',childs_list[1])

        for key,v in self.pathes_costes_dic.items():
            if v==list(childs_list[0]) or v==list(childs_list[1]):
                print(key ,' ', v)
        
        return childs_list

    #def parents_child_replacment(self, childs_list):

        #print(childs_list)
       # for path in self.populationList:
         #   if list(path)==list(childs_list[0]) or list(path)==list(childs_list[1]):


  
 



 

        # note: below list has more than one kind of duplicates
        
       


 

        

     



       






            
            


            
            

        
        


    

f= TSP()
words = f.createPopulationList('D:\\Cities Coordinates.tsp') #puts the file into an arraypr
lis=f.selectParnet()
childs=f.crossover(lis[0],lis[1])
#f.parents_child_replacment(childs)


