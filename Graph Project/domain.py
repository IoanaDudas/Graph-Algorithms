import math
from itertools import combinations

class DirectedGraph:

    def __init__(self):
        self._numberVetices = 0
        self._numberEdges = 0
        self._graphIn = {}
        self._graphOut = {}
        self._graphCost = {}

    def setNumberVertices(self, numberVetices):
        self._numberVetices = numberVetices

    def getNumberVertices(self):
        return self._numberVetices

    def setNumberEdges(self, numberEdges):
        self._numberEdges = numberEdges

    def getNumberEdges(self):
        return self._numberEdges

    def listCosts(self):
        return list(self._graphCost.keys())

    def inDegree(self, vertex):
        degree = 0
        for each in self._graphIn[vertex]:
            degree += 1
        return degree

    def outDegree(self, vertex):
        degree = 0
        for each in self._graphOut[vertex]:
            degree += 1
        return degree

    def checkVertex(self, vertex):
        '''
        :param vertex:
            - the vertex of the graph that will be verified
        :return:
            - True, if vertex is valid
            - False, otherwise
        '''
        if vertex in self._graphIn:
            return True
        if vertex >= 0:
            return False

    def addVertex(self, vertex):
        '''
        :return:
            - True, if the vertex was successfully added
            - False, otherwise
        '''
        if vertex <= self.getNumberVertices():
            if self.checkVertex(vertex) is False:
                self._graphIn[vertex] = []
                self._graphOut[vertex] = []
                self._numberVetices += 1
                return
        else:
            raise Exception("Vertex wasn't added!")

    def removeVertex(self, vertex):
        '''
        :return:
            - True, if the edge was successfully removed
            - False, otherwise
        '''
        if self.checkVertex(vertex) is True:
            self._numberVetices -= 1
            for each in self._graphOut[vertex]:
                self._graphIn[each].remove(vertex)
                del self._graphCost[(vertex, each)]
                self._numberEdges -= 1
            del self._graphOut[vertex]
            for each in self._graphIn[vertex]:
                self._graphOut[each].remove(vertex)
            del self._graphIn[vertex]
        else:
            raise Exception("Vertex wasn't removed!")

    def checkEdge(self, firstVertex, secondVertex):
        '''
        :return:
            - True, if there exists an edge between them
            - False, otherwise
        '''
        if self.checkVertex(firstVertex) and self.checkVertex(secondVertex):
            if (firstVertex, secondVertex) in self._graphCost:
                return True
        return False

    def addEdge(self, firstVertex, secondVertex, cost):
        '''
        :return:
            - True, if the edge was successfully added
            - False, otherwise
        '''
        if self.checkEdge(firstVertex, secondVertex) is False:
            self._graphOut[firstVertex].append(secondVertex)
            self._graphIn[secondVertex].append(firstVertex)
            self._graphCost[(firstVertex, secondVertex)] = cost
            self._numberEdges += 1
        else:
            raise Exception("Edge wasn't added!")

    def removeEdge(self, firstVertex, secondVertex):
        '''
        :return:
            - True, if the edge was successfully removed
            - False, otherwise
        '''
        if self.checkEdge(firstVertex, secondVertex) is True:
            self._graphOut[firstVertex].remove(secondVertex)
            self._graphIn[secondVertex].remove(firstVertex)
            del self._graphCost[(firstVertex, secondVertex)]
            self._numberEdges -= 1
        else:
            raise Exception("Edge wasn't removed!")

    def getCost(self, firstVertex, secondVertex):
        '''
        :return:
            - the cost between the 2 vertices, if there is one
        '''
        if self.checkEdge(firstVertex, secondVertex) is True:
            return self._graphCost[(firstVertex, secondVertex)]
        else:
            raise Exception("Cost doesn't exist!")

    def setCost(self, firstVertex, secondVertex, cost):
        if self.checkEdge(firstVertex, secondVertex) is True:
            self._graphCost[(firstVertex, secondVertex)] = cost
        else:
            raise Exception("Cost wasn't updated!")

    def graphList(self):
        return self._graphOut

    def makeCopy(self):
        self._dictIn = self._graphIn
        self._dictOut = self._graphOut
        self._dictCost = self._dictCost

    def revertOriginal(self):
        self._graphIn = self._dictIn
        self._graphOut = self._dictOut
        self._graphCost = self._dictCost

    def getAllVertices(self):
        vertices = []
        for each in self._graphOut:
            vertices.append(each)
        return vertices

    def inboundEdges(self, vertex):
        inbounds = []
        for each in self._graphOut[vertex]:
            inbounds.append(each)
        return inbounds

    def outboundEdges(self, vertex):
        outbounds = []
        for each in self._graphOut[vertex]:
            outbounds.append(each)
        return outbounds


    def bfsShortestPath(self, start, end):
        # keeps track of explored vertices
        explored = []
        # keeps track of all the paths that will be checked
        queue = [[start]]
        # returns path if the start is equal to the end
        '''if start == end:
            raise Exception("The start is equal to the end!")'''

        # keeps looping until all possible paths have been checked
        while queue:
            # pops the first path from the queue
            path = queue.pop(0)
            # gets the last vertex from the path
            vertex = path[-1]
            if vertex not in explored:
                neighbours = self._graphOut[vertex]
                # goes through all neighbour vertices, constructs a new path and pushes it into the queue
                for neighbour in neighbours:
                    newPath = list(path)
                    newPath.append(neighbour)
                    queue.append(newPath)
                    # returns the path if the neighbour is the end
                    if neighbour == end:
                        return newPath

                # marks vertex as explored
                explored.append(vertex)

        # in case there's no path between the 2 vertices
        raise Exception("Connecting path doesn't exist!")


    def DF1(self, vertex, visited, stack):
        for each in self._graphOut[vertex]:
            if each not in visited:
                visited.append(each)
                self.DF1(each, visited, stack)
        stack.append(vertex)


    def KosarajuAlgorithm(self):
        stack = []
        visited = []

        for each in range(self._numberVetices):
            if each not in visited:
                visited.append(each)
                self.DF1(each, visited, stack)

        visited.clear()
        queue = []
        connectedNumber = 0
        components = {}
        while len(stack) != 0:
            element = stack.pop(-1)
            if element not in visited:
                connectedNumber += 1
                components[connectedNumber] = [element]
                queue.append(element)
                visited.append(element)
                while len(queue) != 0:
                    vertex = queue.pop(-1)
                    for each in self._graphIn[vertex]:
                        if each not in visited:
                            visited.append(each)
                            queue.append(each)
                            components[connectedNumber].append(each)
        return components


    def lowestCostWalk(self, start, end, prev):
        numberEdges = self.getNumberEdges()
        numberVertices = self.getNumberVertices()

        d = [[math.inf for x in range(numberEdges + 1)] for y in range(numberVertices)]
        for i in range(numberEdges + 1):
            d[start][i] = 0
        last = [0] * numberVertices

        for i in range(numberVertices - 1):
            changed = False
            for edge in self.listCosts():
                if d[edge[1]][last[edge[0]]+1] > d[edge[0]][last[edge[0]]] + self.getCost(edge[0], edge[1]):
                    newCost = d[edge[0]][last[edge[0]]] + self.getCost(edge[0], edge[1])

                    for j in range(last[edge[0]] + 1, numberEdges + 1):
                        d[edge[1]][j] = newCost
                    changed = True
                    last[edge[1]] = last[edge[0]]+1
                    prev[edge[1]] = edge[0]
            if not changed:
                break

        for edge in self.listCosts():
            if d[edge[1]][last[edge[0]] + 1] > d[edge[0]][last[edge[0]]] + self.getCost(edge[0], edge[1]):
                raise Exception("Negative cost!")

        return d[end][numberEdges]


    def nrOfLowCostWalks(self, start, end):
        numberOfVertices = self._numberVetices

        dist = [math.inf] * numberOfVertices
        dist[start] = 0
        numberPaths = [0] * numberOfVertices
        numberPaths[start] = 1
        prev = [[] for i in range(numberOfVertices)]

        for i in range(numberOfVertices - 1):
            changed = False
            for edge in self.listCosts():
                if dist[edge[1]] > dist[edge[0]] + self.getCost(edge[0], edge[1]):
                    dist[edge[1]] = dist[edge[0]] + self.getCost(edge[0], edge[1])
                    numberPaths[edge[1]] = numberPaths[edge[0]]
                    if edge[0] not in prev[edge[1]]:
                        prev[edge[1]].append(edge[0])
                    changed = True
                elif dist[edge[1]] == dist[edge[0]] + self.getCost(edge[0], edge[1]) and edge[0] not in prev[edge[1]]:
                    numberPaths[edge[1]] += numberPaths[edge[0]]
                    prev[edge[1]].append(edge[0])
                    for p in prev:
                        if edge[1] in p:
                            p.remove(edge[1])
                    changed = True
            if not changed:
                break

        return numberPaths[end]


    def topologicalSortPredecessorCounting(self):

        sortedList = []
        queue = []
        count = {}
        for x in self._graphIn.keys():
            count[x] = self.inDegree(x)
            if count[x] == 0:
                queue.append(x)
        while len(queue) != 0:
            x = queue.pop(0)
            sortedList.append(x)
            for y in self.outboundEdges(x):
                count[y] = count[y] - 1
                if count[y] == 0:
                    queue.append(y)
        if len(sortedList) < len(self._graphIn.keys()):
            sortedList = None
        return sortedList


    def highestCostPath(self, sortedList, start, end):

        vertices = self.getNumberVertices()
        costList = [-1000000] * vertices
        costList[start] = 0

        for current in sortedList:
            if current == end:
                break
            for neighbour in self.outboundEdges(current):
                edgeCost = self.getCost(current, neighbour)
                if costList[neighbour] < costList[current] + edgeCost:
                    costList[neighbour] = costList[current] + edgeCost


        if costList[end] < 0:
            print("No cost between the vertices")
        else:
            print(costList[end])


    def isClique(self, listVerify):
        '''
            - verifies if the graph given by the list is a clique (it is complete)
        :param listVerify:
        :return:
            True - if it is a cliquw
            False - otherwise
        '''

        for i in range(0, len(listVerify)):
            for j in range(i + 1, len(listVerify)):
                if self.checkEdge(listVerify[i], listVerify[j]) is False and self.checkEdge(listVerify[j], listVerify[i]) is False:
                    return False
        return True


    def maxClique(self):
        '''
            - finds the maximal clique of the graph, if there exists one
            - prints the clique and its length
        :return:
        '''

        vertices = self.getNumberVertices()

        for i in range(vertices, 1, -1):
            # the method starts to generate the combinations of vertices, starting with the number of vertices until 1
            comb = list(combinations(list(range(0, vertices)), i))
            for combList in list(comb):
                # if the method finds a clique then it prints the clique and the clique's length and the method stops
                if self.isClique(combList) is True:
                    print("Max size of clique: " + str(len(combList)))  # printing the clique
                    print("Max clique: " + str(combList))  # printing the clique's size
                    return  # the method stops


    def maxClique2(self):
        '''
            - finds the maximal clique of the graph, if there exists one
            - prints the clique and its length
        :return:
        '''

        maxCliqueSize = 0
        maxClique = []
        start = 0
        end = self.getNumberVertices()

        # the method searches for a maximal clique in the graph
        for i in range(start, end):
            for j in range(end, start, -1):
                listToVerify = list(range(i, j))
                if self.isClique(listToVerify) is True:
                    max = j - i
                    if max > maxCliqueSize:  # if the clique found is bigger than the one saved, we replace the saved one with the new one
                        maxCliqueSize = max  # saving the clique's size
                        maxClique = list(range(i, j))  # saving the clique

        print("Max size of clique: " + str(maxCliqueSize))  # printing the clique
        print("Max clique: " + str(maxClique))  # printing the clique's size

