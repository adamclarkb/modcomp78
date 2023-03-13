from graphviz import Digraph 

class DAG:
    """
    A DAG is represented as an "adjacency list" (list of children for each node) using a single dict.

    Example: Covid-19

    child_dict = {
        'Z': ['X2', 'Y'],
        'Y': ['X3'],
        'X1': ['Z', 'X3']
    }
        
    G = DAG(child_dict=child_dict)
    """

    def __init__(self, child_dict = None):
        # Store adjacency list of children
        self.graph = {}
        # Store adjacency list of parents
        self.parents = {}
        #Store nodes in a list (used for topological ordering)
        self.nodes = []

        if child_dict:
            self.set_graph(child_dict)

    #wrapper function for setting the graph dict and updating the related variables
    def set_graph(self, child_dict):
        self.graph = child_dict 
        #ensure that all nodes mentioned in the dict get their own key
        #In the Covid-19 example, the following adds to the dict 'X2' : [], 'X3' : []
        nodes = set([child for sublist in self.graph.values() for child in sublist])
        for n in nodes:
            self.graph[n] = self.graph.get(n, [])
        #update node list
        self.nodes = list(self.graph)
        #update parent graph (dictionary containing list of parents for each node)
        parents = {n : [] for n in self.nodes}
        for n in parents:
            for c in self.graph[n]:
                parents[c] += [n]
        self.parents = parents
        
    #This function finds a topological ordering of the graph, and updates self.nodes accordingly
    #Based on the algorithm and implementation given here: https://www.geeksforgeeks.org/topological-sorting/
    def topologicalSort(self):        
        stack = []
        visited_nodes = {n : False for n in self.nodes}
        for n in self.nodes:
            if not visited_nodes[n]:
                self.topologicalSortUtil(n, visited_nodes, stack)
        self.nodes = stack[::-1]

    #A recursive auxillary function for topologicalSort
    def topologicalSortUtil(self, n, visited_nodes, stack):
        visited_nodes[n] = True
        for c in self.graph[n]:
            if not visited_nodes[c]:
                self.topologicalSortUtil(c, visited_nodes, stack)
        stack.append(n)

    #Function for computing list of reachable nodes
    def reachable(self, X, Z):
        """
        In:
            X: node
            Z: list of nodes
        Out:
            list of nodes that are reachable from X given Z
        """
        #Sort the nodes
        self.topologicalSort()

        """
        Notation:
            A: Ancestors of Z
            R: Reachable nodes
            V: Visited nodes
            L: Nodes to be investigated
        """
        # --- Step 1: Find ancestors of Z --- 
        A = Z.copy()
        for n in self.nodes[::-1]:
            if n in A:
                A += self.parents[n]
        A = set(A)

        # --- Step 2: Traverse active paths from X to find reachable nodes --- 
        L = [(X, 'up')]
        R = set({})
        V = set({})

        while L:
            #pick first element of L and pop it from L
            (Y, d) = L[0]
            L = L[1::]
            #if visited, continue with next element
            if (Y, d) in V:
                continue
            #Mark it as vistited 
            V.add((Y, d))
            #Add it to R if it is not in Z
            if Y not in Z:
                R.add(Y)
            #Trail up
            if d == 'up'  and Y not in Z:
                    L += [(p, 'up') for p in self.parents[Y]]
                    L += [(c, 'down') for c in self.graph[Y]]
            #Trail down
            elif d == 'down':
                if Y not in Z:
                    L += [(c, 'down') for c in self.graph[Y]]
                if Y in A:
                    L += [(p, 'up') for p in self.parents[Y]]
        #Return reachable nodes
        return list(R)

    #Function for vizualising the graph
    def draw(self, output_path):
        """
        In: 
            path: a string for the filename without file extension
        Out:
            The graph visualized in a .pdf.
        """
        graph = Digraph()

        for n in self.nodes:
            graph.node(n)
            for c in self.graph[n]:
                graph.edge(n, c)

        graph.render(output_path)


