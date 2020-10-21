from domain import *
from random import *

class ui:

    def __init__(self):
        self._domain = DirectedGraph()

    def printOptions(self):
        print("1. Read from file")
        print("2. Save to file")
        print("3. Number of vertices")
        print("4. Check existence of edge")
        print("5. In degree")
        print("6. Out degree")
        print("7. Modify cost between 2 edges")
        print("8. Cost between 2 edges")
        print("9. Add edge")
        print("10. Remove edge")
        print("11. Add vertex")
        print("12. Remove vertex")
        print("13. Random graph generator")
        print("14. Make a copy")
        print("15. Revert to original")
        print("16. Iterate vertices")
        print("17. Outbound edges of vertex")
        print("18. Inbound edges of vertex")
        print("19. Breadth-first search shortest path")
        print("20. Strongly connected components")
        print("21. Lowest cost walk between two vertices")
        print("22. Number of lowest cost paths")
        print("23. Graph is DAG")
        print("24. Highest cost path between 2 vertices")
        print("25. Max clique")
        print("26. Exit")

    def menu(self):
        self.printOptions()
        while True:
            try:
                try:
                    choice = int(input("-> "))
                except:
                    raise ValueError("Invalid input!")

                if choice == 1:
                    self.readFile()

                elif choice == 2:
                    self.saveFile()

                elif choice == 3:
                    print(self._domain.getNumberVertices())

                elif choice == 4:
                    firstVertex = int(input("First Vertex: "))
                    secondVertex = int(input("Second Vertex: "))
                    if self._domain.checkEdge(firstVertex, secondVertex) is True:
                        print("There exists an edge!")
                    else:
                        print("There doesn't exist an edge!")

                elif choice == 5:
                    vertex = int(input("vertex: "))
                    print("The in degree is " + str(self._domain.inDegree(vertex)))

                elif choice == 6:
                    vertex = int(input("vertex: "))
                    print("The out degree is " + str(self._domain.outDegree(vertex)))

                elif choice == 7:
                    firstVertex = int(input("First Vertex: "))
                    secondVertex = int(input("Second Vertex: "))
                    cost = int(input("Cost: "))
                    self._domain.setCost(firstVertex, secondVertex, cost)
                    print("Cost successfully updated!")

                elif choice == 8:
                    firstVertex = int(input("First Vertex: "))
                    secondVertex = int(input("Second Vertex: "))
                    print("The cost is: " + str(self._domain.getCost(firstVertex, secondVertex)))

                elif choice == 9:
                    firstVertex = int(input("First Vertex: "))
                    secondVertex = int(input("Second Vertex: "))
                    cost = int(input("Cost: "))
                    self._domain.addEdge(firstVertex, secondVertex, cost)
                    print("Edge successfully added!")

                elif choice == 10:
                    firstVertex = int(input("First Vertex: "))
                    secondVertex = int(input("Second Vertex: "))
                    self._domain.removeEdge(firstVertex, secondVertex)
                    print("Edge successfully removed!")

                elif choice == 11:
                    vertex = self._domain.getNumberVertices()
                    self._domain.addVertex(vertex)
                    print("Vertex successfully added!")

                elif choice == 12:
                    vertex = int(input("Vertex: "))
                    if self._domain.removeVertex(vertex) is True:
                        print("Vertex successfully removed.")

                elif choice == 13:
                    numberVertices = int(input("Number of vertices: "))
                    numberEdges = int(input("Number of edges: "))
                    try:
                        self.rnd(numberVertices, numberEdges)
                    except:
                        raise Exception("Invalid input!")

                elif choice == 14:
                    self._domain.makeCopy()

                elif choice == 15:
                    self._domain.revertOriginal()

                elif choice == 16:
                    print("All vertices: " + str(self._domain.getAllVertices()))

                elif choice == 17:
                    vertex = int(input("Vertex: "))
                    print("Outbound edges: " + str(self._domain.outboundEdges(vertex)))

                elif choice == 18:
                    vertex = int(input("Vertex: "))
                    print("Inbound edges: " + str(self._domain.inboundEdges(vertex)))

                elif choice == 19:
                    start = int(input("Start: "))
                    end = int(input("End: "))
                    print(str(self._domain.bfsShortestPath(start, end)))
                    print("The length is: " + str(len(self._domain.bfsShortestPath(start, end)) - 1))

                elif choice == 20:
                    components = self._domain.KosarajuAlgorithm()
                    print("The strongly connected components of the graph are:")
                    for each in range(len(components)):
                        print(str(each + 1) + ". " + str(components[each + 1]))

                elif choice == 21:
                    start = int(input("Start: "))
                    end = int(input("End: "))
                    prev = [-1] * self._domain.getNumberVertices()
                    try:
                        cost = self._domain.lowestCostWalk(start, end, prev)
                        if str(cost) == 'inf':
                            raise Exception("No existent path!")
                        print("Cost of lowest length path: " + str(cost))
                        result = ''
                        while end != start:
                            result = result + str(end) + ' <- '
                            end = prev[end]
                        result = result + str(start)
                        print("Lowest cost path: " + result)
                    except Exception as msg:
                        print(msg)

                elif choice == 22:
                    start = int(input("Start: "))
                    end = int(input("End: "))
                    result = self._domain.nrOfLowCostWalks(start, end)
                    print("Number of lowest cost walks: " + str(result))

                elif choice == 23:
                    result = self._domain.topologicalSortPredecessorCounting()
                    if result == None:
                        print("The graph has cycles, it is not a DAG")
                    else:
                        print("The graph does not have cycles, it is a DAG")
                        print(result)

                elif choice == 24:
                    start = int(input("Start: "))
                    end = int(input("End: "))
                    result = self._domain.topologicalSortPredecessorCounting()
                    if result == None:
                        print("The graph has cycles, it is not a DAG")
                    else:
                        self._domain.highestCostPath(result, start, end)

                elif choice == 25:
                    self._domain.maxClique()
                    self._domain.maxClique2()


                elif choice == 26:
                    break

                else:
                    raise Exception("Invalid input!")

            except Exception as msg:
                print(msg)

    def readFile(self):
        f = open("graph.txt", "r")
        line = f.readline()
        line = line.split()
        numberVertices = int(line[0])
        numberEdges = int(line[1])
        self._domain.setNumberVertices(numberVertices)
        for each in range(numberVertices):
            self._domain.addVertex(each)
        for each in range(numberEdges):
            line = f.readline()
            line = line.split()
            firstVertex = int(line[0])
            secondVertex = int(line[1])
            cost = int(line[2])
            self._domain.addEdge(firstVertex, secondVertex, cost)

        self._domain.setNumberVertices(numberVertices)
        f.close()

    def saveFile(self):
        open('graph.txt', 'w').close()
        f = open("graph.txt", "w")
        f.write(str(self._domain.getNumberVertices()) + " " + str(self._domain.getNumberEdges()) + '\n')
        dictOut = self._domain.graphList()
        numberVertices = self._domain.getNumberVertices()
        for each in range(numberVertices):
            if self._domain.outDegree(each) == 0 and self._domain.inDegree(each) == 0:
                f.write(str(each) + '\n')
            for element in range(len(dictOut[each])):
                f.write(str(each) + " " + str(dictOut[each][element]) + " " + str(self._domain.getCost(each, dictOut[each][element])) + '\n')
        f.close()

    def rnd(self, numberVertices, numberEdges):
        self._domain.setNumberVertices(numberVertices)
        for each in range(numberVertices):
            self._domain.addVertex(each)

        while numberEdges != 0:
            firstVertex = randint(0, numberVertices-1)
            secondVertex = randint(0, numberVertices - 1)
            while self._domain.checkEdge(firstVertex, secondVertex) is True:
                firstVertex = randint(0, numberVertices - 1)
                secondVertex = randint(0, numberVertices - 1)
            cost = randint(-100, 200)
            self._domain.addEdge(firstVertex, secondVertex, cost)
            numberEdges -= 1
        self._domain.setNumberVertices(numberVertices)
        self.saveFile()
        # for the random graph, I changed the file used in save file to have the 2 graphs in the right place


if __name__=='__main__':
    current_ui=ui()
    current_ui.menu()