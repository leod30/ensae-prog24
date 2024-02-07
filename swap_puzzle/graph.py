"""
This is the graph module. It contains a minimalistic Graph class.
"""

class Graph:
    """
    A class representing undirected graphs as adjacency lists. 

    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [neighbor1, neighbor2, ...]
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    edges: list[tuple[NodeType, NodeType]]
        The list of all edges
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 

        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes 
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
        
    def __str__(self):
        """
        Prints the graph as a list of neighbors for each node (one per line)
        """
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the graph with number of nodes and edges.
        """
        return f"<graph.Graph: nb_nodes={self.nb_nodes}, nb_edges={self.nb_edges}>"

    def add_edge(self, node1, node2):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 
        When adding an edge between two nodes, if one of the ones does not exist it is added to the list of nodes.

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append(node2)
        self.graph[node2].append(node1)
        self.nb_edges += 1
        self.edges.append((node1, node2))

    #Our first bfs is the following, it stopped when it reached the dst cell, but we understood later with the question 8 that it must not, so our real bfs is after this function
    """def bfs(self, src, dst): 
        
        Finds a shortest path from src to dst by BFS.  

        Parameters: 
        -----------
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        
        queue = [src]
        marked = [src]
        prev = [None for i in range(self.nb_nodes)] #list of the parents, in the same order as the nodes
        while len(queue) != 0 and dst not in queue :
            current = queue.pop(0)
            for neighbor in self.graph[current]:
                if neighbor not in marked:
                    queue.append(neighbor)
                    marked.append(neighbor)
                    prev[neighbor-1]=current
        if prev[dst-1] != None: #case where dst is reachable from src
            path=[dst]
            while src not in path:
                path.append(prev[path[-1]-1])
            path.reverse()
        else: #case where dst is not reachable from src
            path = None
        return path"""

    
    def bfs(self, src, dst): 
        """
        Finds a shortest path from src to dst by BFS.  

        Parameters: 
        -----------
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """ 
        queue = [src]
        marked = [src]
        prev = [None for i in range(self.nb_nodes)] #list of the parents, in the same order as the nodes
        while len(queue) != 0 :
            current = queue.pop(0)
            for neighbor in self.graph[current]:
                if neighbor not in marked:
                    queue.append(neighbor)
                    marked.append(neighbor)
                    prev[neighbor-1]=current
        if prev[dst-1] != None: #case where dst is reachable from src
            path=[dst]
            while src not in path:
                path.append(prev[path[-1]-1])
            path.reverse()
        else: #case where dst is not reachable from src
            path = None
        return path


    @classmethod
    def graph_from_file(cls, file_name):
        """
        Reads a text file and returns the graph as an object of the Graph class.

        The file should have the following format: 
            The first line of the file is 'n m'
            The next m lines have 'node1 node2'
        The nodes (node1, node2) should be named 1..n

        Parameters: 
        -----------
        file_name: str
            The name of the file

        Outputs: 
        -----------
        graph: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            graph = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 2:
                    node1, node2 = edge
                    graph.add_edge(node1, node2) # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")
        return graph


def test_graph(graph_number):
    """this function gets the graph in graph.in and tests if the bfs function works with the graph.path.out, by testing bfs(src,dst) (with src and dst the first 2 numbers of each line in graph1.in) and then compares it to the list at the end of the line"""
    G = Graph.graph_from_file(f"/home/onyxia/work/ensae-prog24/input/graph"+str(graph_number)+".in")
    # Open the file in read mode
    with open(f"/home/onyxia/work/ensae-prog24/input/graph"+str(graph_number)+".path.out", "r") as file:
        tuple_list = []  # list with tuples of integers, representing the first 2 numbers of each line in the file graph1.path.out
        list_list = []  # list with lists of integers, representing the path in each line in the file graph1.path.out
        
        # Read each line of the file
        for line in file:
            elements = line.split(" ") #splits the elements in each line separed by a space
            if elements[-1] == "None\n":
                elements[-1] = "None"
            else:
                last_number = (elements.pop())[:-2] #at the end of each line, is a "\n" in order to return to a new line in the file, so we extract the number
                elements.append(last_number)
                elements.append("]") #puts back the "]"
                num3 = eval(elements.pop(2)) #case where there is 3 numbers and 1 list
            
            # Convertir les trois premiers éléments en nombres entiers
            num1 = eval(elements.pop(0))
            num2 = eval(elements.pop(0))
            
            #removes the \n at the end of each line
            list = "".join(elements)
            path = eval(list) #python understands its a list, or a None object
            tuple_nums = (num1, num2)
            
            tuple_list.append(tuple_nums)
            list_list.append(path)

    function_work = True
    for i in range(len(list_list)):
        path_bfs = G.bfs(tuple_list[i][0], tuple_list[i][-1])
        if path_bfs != list_list[i]:
            function_work = False
    
    return "It works with graph number "+str(graph_number)+"!" if function_work else "It doesn't work"

print(test_graph(1))
print(test_graph(2))