import math
from operator import indexOf

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
        self.cityNames= list(map(self.getNamesOfCities,lines[3:len(lines)-1]))
        self.corTupels= list(map(self.getCoorOfCities,lines[3:len(lines)-1]))
        resultDic = dict(zip(self.cityNames, self.corTupels))
        return resultDic
         
        
    def creatPath(self,cities):
        ## takes path and return permutated list of it ##
        return np.random.permutation(cities)



    
    def createPopulationList(self, path):
        f = open(path, "r")
        lines=f.read().splitlines()
        self.cityCoordinates=self.getcityCoordinates(lines[3:]) # {1: ('41', '49'), 2: ('35', '17')
        self.populationList=[] #[1,2,3,4,5,6,
        count=0
        for x in range(0,100):
            self.populationList.append(self.creatPath(self.cityNames))
  

        self.coordinates=[] # [('41', '49'), ('35', '17'),

        return None

    def euclidean_distance(self,p0, p1):
       # print(float(p1[0]) ,' ', float(p0[0]))
       # print(float(p1[1]) ,' ', float(p0[1]))

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
        for p in  self.populationList:
            coordLists.append(self.getCoordinates(p))
        for coordList in coordLists:
            for i in range(0,len(coordList)-2):
               # print(coordList[i],' ',coordList[i+1])
                sum=sum+self.euclidean_distance(coordList[i],coordList[i+1])
            costList.append( sum)                
            sum=0

        print(costList)
        print(self.populationList[costList.index(min(costList))])
        print(min(costList))
            


            
            

        
        


    


f= TSP()
words = f.createPopulationList('D:\\Cities Coordinates.tsp') #puts the file into an arraypr
f.fitness()