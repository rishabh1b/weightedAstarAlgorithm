import sys
import math
import itertools
import heapq

class GraphNode:
    def __init__(self, x, y, nodenumber):
        self.__x = x
        self.__y = y
        self.__neighbours = []
        self.__parentNode = None
        self.__costToStart = float("inf")
        self.nodeNumber = nodenumber

    def addneighbour(self, next):
        self.__neighbours.append(next)

    def __hash__(self):
        return hash(self.nodeNumber)

    def __eq__(self, other):
        return self.nodeNumber == other.nodeNumber

    def setCostToStart(self, cost):
        self.__costToStart = cost

    def setParentNode(self, node):
        self.__parentNode = node

    def getCostToStart(self):
        return self.__costToStart

    def getParentNode(self):
        return self.__parentNode

    def getNeighbours(self):
        return self.__neighbours

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    # For testing
    def printNeighbours(self):
        print self.__neighbours

############################################################################################################
# Priority Queue implementation taken from Python Documentation - https://docs.python.org/2/library/heapq.html
class priorityqueue:
    def __init__(self):
        self.__pq = []                         # list of entries arranged in a heap
        self.__entry_finder = {}               # mapping of tasks to entries
        self.__REMOVED = '<removed-task>'      # placeholder for a removed task
        self.__counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=0.0):
        'Add a new task or update the priority of an existing task'
        if task in self.__entry_finder:
            self.remove_task(task)
        count = next(self.__counter)
        entry = [priority, count, task]
        self.__entry_finder[task] = entry
        heapq.heappush(self.__pq, entry)

    def remove_task(self,task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.__entry_finder.pop(task)
        entry[-1] = self.__REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.__pq:
            priority, count, task = heapq.heappop(self.__pq)
            if task is not self.__REMOVED:
                del self.__entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    #An extra method to determine whether pq is empty
    def isEmpty(self):
        return len(self.__pq) == 0

##################################################################################################################

def weightedastaralgorithm(start, goal, unvisited, edges, weight):
    pq = priorityqueue()
    start.setCostToStart(0)
    unvisited.remove(start)
    pq.add_task(start)
    path_to_goal = []
    while not pq.isEmpty():
        curr_node = pq.pop_task()
        if curr_node is goal:
            while curr_node.getParentNode() is not None:
                path_to_goal.append(curr_node.nodeNumber)
                curr_node = curr_node.getParentNode()
            path_to_goal.append(start.nodeNumber)
            break

        neighbours = curr_node.getNeighbours()
        for neigh in neighbours:
            curr_edge_cost = edges[(curr_node.nodeNumber,neigh.nodeNumber)]
            if neigh in unvisited or neigh.getCostToStart() > curr_node.getCostToStart() + curr_edge_cost:
                if neigh in unvisited:
                    unvisited.remove(neigh)
                neigh.setParentNode(curr_node)
                neigh.setCostToStart(curr_node.getCostToStart() + curr_edge_cost)
                priority = neigh.getCostToStart() + weight * heuristicPriority(neigh,goal)
                pq.add_task(neigh, priority)

    return list(reversed(path_to_goal))

def heuristicPriority(node, goalnode):
    return math.sqrt((goalnode.getY() - node.getY())**2 + (goalnode.getX() - node.getX())**2)


def main(args):
    #inpfilenodes = open("Data\graph1_nodes.txt", "r")
    #inpfileedges = open("Data\graph1_edges.txt", "r")

    # Actual Problem Files
    inpfilenodes = open("Data/rand1_nodes.txt", "r")
    inpfileedges = open("Data/rand1_edges.txt", "r")

    # count - keeps track of the node number as they come from the file line wise
    # graphnodes - A Set containing the node objects of the class GraphNode
    # node_finder - A Dictionary to get hold of the node objects corresponding to their node number
    # edges - A Dictionary that keeps the node numbers of this edge as the key and their cost as the value
    count = 1
    graphnodes = set()
    node_finder = {}
    edges = {}

    for line in inpfilenodes:
        curr_node = line.split(',')
        curr_node_x = float(curr_node[0])
        curr_node_y = float(curr_node[1])
        node = GraphNode(curr_node_x, curr_node_y, count)
        graphnodes.add(node)
        node_finder[count] = node
        count = count + 1

    for line in inpfileedges:
        curr_edge = line.split(',')
        curr_edge_pt1 = int(curr_edge[0])
        curr_edge_pt2 = int(curr_edge[1])
        curr_edge_weight = float(curr_edge[2])
        edges[(curr_edge_pt1, curr_edge_pt2)] = curr_edge_weight
        node_1 = node_finder[curr_edge_pt1]
        node_2 = node_finder[curr_edge_pt2]
        node_1.addneighbour(node_2)

    inpfilenodes.close()
    inpfileedges.close()

    # Enter the start, end and weight from the problem statement
    startindex = 643
    endindex = 608
    weight = 100.0

    # Get the node objects corresponding to the node number
    startnode = node_finder[startindex]
    goalnode = node_finder[endindex]

    path = weightedastaralgorithm(startnode, goalnode, graphnodes, edges, weight)
    print path

    # Dump the output to a corresponding file
    """
    f = open('Solutions\Problem_5.txt', 'w')
    for i in range(len(path)):
        f.write((str(path[i])) + '\n')
    f.close()
    """


if __name__ == '__main__':
    main(sys.argv)