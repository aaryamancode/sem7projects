import math
import random
import numpy
from functools import reduce
import sys
import re
from matplotlib import pyplot as plt

alfa = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
fileName = "eg1.txt"
iterations = 20
ants = 22

xcoord=[]
ycoord=[]
pointnum=[]

def getData(fileName):
    f = open(fileName, "r")
    content = f.read()
    optimalValue = re.search("Optimal value: (\d+)", content, re.MULTILINE)
    if(optimalValue != None):
        optimalValue = optimalValue.group(1)
    else:
        optimalValue = re.search("Best value: (\d+)", content, re.MULTILINE)
        if(optimalValue != None):
            optimalValue = optimalValue.group(1)
    capacity = re.search("^CAPACITY : (\d+)$", content, re.MULTILINE).group(1)
    graph = re.findall(r"^(\d+) (\d+) (\d+)$", content, re.MULTILINE)
    demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
    graph = {int(a):(int(b),int(c)) for a,b,c in graph}
    demand = {int(a):int(b) for a,b in demand}
    capacity = int(capacity)
    optimalValue = int(optimalValue)
    return capacity, graph, demand, optimalValue

def generateGraph():
    capacityLimit, graph, demand, optimalValue = getData(fileName)
    vertices = list(graph.keys())
    vertices.remove(1)
    
    for i in range(len(graph)):
        xcoord.append(graph[i+1][0])
        ycoord.append(graph[i+1][1])
        pointnum.append(i+1)

    edges = { (min(a,b),max(a,b)) : numpy.sqrt((graph[a][0]-graph[b][0])**2 + (graph[a][1]-graph[b][1])**2) for a in graph.keys() for b in graph.keys()}
    feromones = { (min(a,b),max(a,b)) : 1 for a in graph.keys() for b in graph.keys() if a!=b }
    return vertices, edges, capacityLimit, demand, feromones, optimalValue

def solutionOfOneAnt(vertices, edges, capacityLimit, demand, feromones):
    solution = list()

    while(len(vertices)!=0):
        path = list()
        city = numpy.random.choice(vertices)
        capacity = capacityLimit - demand[city]
        path.append(city)
        vertices.remove(city)
        while(len(vertices)!=0):
            probabilities = list(map(lambda x: ((feromones[(min(x,city), max(x,city))])**alfa)*((1/edges[(min(x,city), max(x,city))])**beta), vertices))
            probabilities = probabilities/numpy.sum(probabilities)
            
            city = numpy.random.choice(vertices, p=probabilities)
            capacity = capacity - demand[city]

            if(capacity>0):
                path.append(city)
                vertices.remove(city)
            else:
                break
        solution.append(path)
    return solution

def rateSolution(solution, edges):
    s = 0
    for i in solution:
        a = 1
        for j in i:
            b = j
            s = s + edges[(min(a,b), max(a,b))]
            a = b
        b = 1
        s = s + edges[(min(a,b), max(a,b))]
    return s

def updateFeromone(feromones, solutions, bestSolution):
    Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions))/len(solutions)
    feromones = { k : (ro + th/Lavg)*v for (k,v) in feromones.items() }
    solutions.sort(key = lambda x: x[1])
    if(bestSolution!=None):
        if(solutions[0][1] < bestSolution[1]):
            bestSolution = solutions[0]
        for path in bestSolution[0]:
            for i in range(len(path)-1):
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = sigm/bestSolution[1] + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    else:
        bestSolution = solutions[0]
    for l in range(sigm):
        paths = solutions[l][0]
        L = solutions[l][1]
        for path in paths:
            for i in range(len(path)-1):
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (sigm-(l+1)/L**(l+1)) + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    return bestSolution

def run():
    bestSolution = None
    vertices, edges, capacityLimit, demand, feromones, optimalValue = generateGraph()
    
    for i in range(iterations):
        solutions = []
        for _ in range(ants):
            solution = solutionOfOneAnt(vertices.copy(), edges, capacityLimit, demand, feromones)
            solutions.append((solution, rateSolution(solution, edges)))
        bestSolution = updateFeromone(feromones, solutions, bestSolution)
        print(str(i)+":\t"+str(int(bestSolution[1]))+"\t"+str(optimalValue))
#         print("Path taken:"+str(bestSolution[0])+"\n")
    return bestSolution

alfa = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
iterations = 100
ants = 22

solution = run()

print("Found solution: \t %0.3f" % (solution[1]))
print("Path: \n"+str(solution[0]))

if(fileName=="eg1.txt"):
    optimalSolution = ([[18, 21, 19, 16, 13], [17, 20, 22, 15], [14, 12, 5, 4, 9, 11], [10, 8, 6, 3, 2, 7]], 375)
    print("\nOptimal solution: \t"+str(optimalSolution[1]))
    print("Optimal Path: \n"+str(optimalSolution[0]))

print("\nfile name:\t"+str(fileName)+ "\nalpha:\t\t"+str(alfa)+ "\nbeta:\t\t"+str(beta)+ "\nsigma:\t\t"+str(sigm)+
      "\nrho:\t\t"+str(ro)+ "\ntheta:\t\t"+str(th)+ "\niterations:\t"+str(iterations)+ 
      "\nnumber of ants:\t"+str(ants)+"\n")


plt.figure(figsize=(10,8))
plt.scatter(xcoord,ycoord)
plt.scatter(xcoord[0],ycoord[0],color="red")

for i,txt in enumerate(pointnum):
    plt.annotate(txt, (xcoord[i],ycoord[i]))

plt.show()
