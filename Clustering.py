# -*- coding: utf-8 -*-
"""
Spyder Editor

Donovan Orn.
"""
#library(Hmisc)
#library(GGally)
#library(sna)
#library(scales)
#library(NISTunits)
import os
import networkx as nx

class WeightedClusterGraph():
    ''' Adds each subject as a node to Graph G.
    
    Parameters
    ----------
    X : Pandas DataFrame
        The data that will be used to create edges in EdgeDefinition
        
    y : iterable
        Resulting variable of the data.
        
    EdgeDefinition : Function of form "Function(G, data_for_edge)"
        Function used to add edges based on desired criteria.
    
    G : Networkx Graph
        The graph nodes will be added to.
        
    Class Variables
    ---------------
    G : Networkx Graph
        The Weighted Graph.
    
    Built in Functions
    ------------------
    DrawGraph(node_color_map, edge_color_map, node_size)
        Saves the weighted graph in Graphs folder. Graphs folder will be created if it does not exist.
    
    convert2Excel()
        Saves an csv file that represents the weighted graph.
        This csv is of the form:
        SOURCE,TARGET,WEIGHT\n
        node,node,weight of edge\n
        ...\n
        ...
        
        Where each row represents the edges.
        (CyptoScape Friendly)
        
    minimumCut()
        Finds the minimum cut of  each subgraph.
    
    getAllWeightedDensity()
        Finds the weighted density of each subgraph.
    '''
    
    def __init__(self, X, y, EdgeDefinition, name = 'ClusterGraph'):
        def CreateNodes(G, y):
            for node_name in y:
                G.add_node(str(node_name))        
            return G
        G = nx.Graph()
        G.name = str(name)
        G = CreateNodes(G, y)
        G = EdgeDefinition(G, X)
        self.G = G
        self.node_color_map = None
        self.edge_color_map = None
        
    def SetNodeColorMap(self, color_dict):
        ''' Takes a dictionary object and sets the node_color_map.
            node_color_map determins the nodes' color when drawing the graph.
            
            Parameters
            ----------
            color_dict : dictionary object
                A dictionary where the keys represent the node 
                and the value of the key is the color of the node.
            
            Warning
            -------
            The color 'red' is used as a default for nodes not represented in color_dict.
            Although red can be used it is not recommended.'''
        self.color_dict = color_dict
        node_colors = []
        for node in self.G.nodes():
            if node in color_dict.keys():
                node_colors.append(color_dict[node])
            else:
                node_colors.append('red')
        self.node_color_map = node_colors
        
    def DrawGraph(self, node_size = 120, folder_extention = ''):
        """ Draws the network graph and saves them to 'Graphs' folder.
        
        Parameters
        ----------
        node_color_map : List of Strings
            contains the color order of the nodes.
            
        edge_color_map : List of Strings
            Contains the color order for each edge.
        
        node_size = 100 : integer
            Size of the nodes in the graphs
            
        """
        import matplotlib.pyplot as plt

        edges = self.G.edges()
        weights = [self.G[u][v]['weight'] * 2 for u, v in edges]
#        nx.draw(self.G, pos = nx.kamada_kawai_layout(self.G), node_size = node_size, node_color = self.node_color_map, edge_color = self.edge_color_map, width = weights, with_labels = True)
        if not os.path.exists('Graphs/' + str(folder_extention)):
            os.makedirs('Graphs/' + str(folder_extention))
#        plt.savefig('Graphs/'  + str(folder_extention) + self.G.name + '_kawai_minTrails.png')
#        plt.show()
        
        nx.draw(self.G, pos = nx.spring_layout(self.G), node_size = node_size, node_color = self.node_color_map, edge_color = self.edge_color_map, width = weights, with_labels = True)
        plt.savefig('Graphs/'  + str(folder_extention) + self.G.name + '_spring_minTrails.png')
        plt.show()
        
    def DrawSubGraphs(self, node_size = 150, folder_extention = ''):
        """ Draws each sub graph in the network graph and saves them to 'Graphs' folder.
        
        Parameters
        ----------
        node_color_map : List of Strings
            contains the color order of the nodes.
            
        edge_color_map : List of Strings
            Contains the color order for each edge.
        
        node_size = 100 : integer
            Size of the nodes in the graphs
            
        """
        import matplotlib.pyplot as plt
        
        sub_graphs = [c for c in sorted(nx.connected_components(self.G), key=len, reverse=True)]
        for idx, sub_G in enumerate(sub_graphs):
            if len(sub_G) > 1:
                sub_G = self.G.subgraph(sub_G)
                edges = sub_G.edges()
                weights = [sub_G[u][v]['weight'] * 2 for u, v in edges]
                node_colors = []
                for node in sub_G.nodes():
                    if node in self.color_dict.keys():
                        node_colors.append(self.color_dict[node])
                    else:
                        node_colors.append('red')
               
                nx.draw(sub_G, pos = nx.spring_layout(sub_G), node_size = node_size, node_color = node_colors, width = weights, with_labels = True)
                
                if not os.path.exists('Graphs/' + str(folder_extention) + self.G.name + '_spring_minTrials/'):
                    os.makedirs('Graphs/' + str(folder_extention) + self.G.name + '_spring_minTrials/')
                plt.savefig('Graphs/'  + str(folder_extention) + self.G.name + '_spring_minTrials/sub' + str(idx+1) + '.png')
                plt.show()   
        
    def convert2Excel(self, name = ''):
        """Saves a csv table file to be converted to Cyptoscape graph."""
        file_string = 'SOURCE,TARGET,WEIGHT\n'
        for edge in self.G.edges():
            source_node = edge[0]
            target_node = edge[1]
            weight = self.G.get_edge_data(edge[0], edge[1])['weight']
            file_string = file_string + str(source_node) + ',' + str(target_node) + ',' + str(weight) + '\n'
        with open(str(name) + self.G.name + '.csv', 'w') as file:
            file.write(file_string)
    
    def minimumCut(self):
        sub_graphs = [c for c in sorted(nx.connected_components(self.G), key=len, reverse=True)]
        print(sub_graphs)
        for sub_G in sub_graphs:
            sub_G = self.G.subgraph(sub_G)
            try:
                cut_value, partition = nx.stoer_wagner(sub_G, weight = 'corr')
                print(str(partition) + ': ' + str(cut_value))
            except nx.NetworkXError:
                print('Node ' + str(sub_G.nodes()) + ' is isolated')
        print()

    def getAllWeightedDensity(self):
        def weightedDensity(G):
            """
            Weighted Density = The sum of all edge weights / number of possible edges
                Weighted Density = (Sum((v in V,u in V, u != v) * weight(u,v)))/(len(V)* len(V-1))
            
            Notes
            -----
            1. Since G is undirected G.edges() returns (u,v) and not (v,u). 
            Therefore, the edge needs to be counted twice. 
            
            2. corr is between 0 and 1, thus density must also be between 0 and 1.
            """
            sum_edge_weights = 0
            for edge in G.edges():
                corr = nx.get_edge_attributes(G,'corr')
                sum_edge_weights += corr[edge] * 2                              # *2 to count edge(u,v) and edge(v,u)
            return sum_edge_weights/(len(G.nodes()) * (len(G.nodes()) - 1))
        
        sub_graphs = [c for c in sorted(nx.connected_components(self.G), key=len, reverse=True)]
        print(sub_graphs)
        for sub_G in sub_graphs:
            sub_G = self.G.subgraph(sub_G)
            try:
                density = weightedDensity(sub_G)
                print('Cluster ' + str(sub_G.nodes()) + ': ' + str(density))
            except ZeroDivisionError:
                print('Graph {' + str(sub_G.nodes()) + '} is isolated')
        print()

    def getWeightedDensity(self, nodes, name = ''):
        def weightedDensity(G):
            """
            Weighted Density = The sum of all edge weights / number of possible edges
                Weighted Density = (Sum((v in V,u in V, u != v) * weight(u,v)))/(len(V)* len(V-1))
            
            Notes
            -----
            1. Since G is undirected G.edges() returns (u,v) and not (v,u). 
            Therefore, the edge needs to be counted twice. 
            
            2. corr is between 0 and 1, thus density must also be between 0 and 1.
            """
            sum_edge_weights = 0
            for edge in G.edges():
                corr = nx.get_edge_attributes(G,'corr')
                sum_edge_weights += corr[edge] * 2                              # *2 to count edge(u,v) and edge(v,u)
            return sum_edge_weights/(len(G.nodes()) * (len(G.nodes()) - 1))
#        sub_graphs = self.G.subgraph(nodes)
#        sub_graphs = [c for c in sorted(nx.connected_components(sub_graphs), key=len, reverse=True)]
#        print(sub_graphs)
#        for sub_G in sub_graphs:
#            sub_G = self.G.subgraph(sub_G)
#            try:
#                density = weightedDensity(sub_G)
#                print(str(sub_G.nodes()) + ': ' + str(density))
#            except ZeroDivisionError:
#                print('Graph {' + str(sub_G.nodes()) + '} is isolated')
#        print()
        
        sub_graphs = self.G.subgraph(nodes)
#        print(sub_graphs)
        try:
            density = weightedDensity(sub_graphs)
            print(str(name) + ': ' + str(density))
        except ZeroDivisionError:
            print('Graph {' + str(sub_graphs.nodes()) + '} is an isolated graph\n Density : 0')