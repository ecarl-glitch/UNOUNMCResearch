# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:13:09 2020

@author: Donovan
"""

def SpearmansCorrelation(data_for_edge, run_number, G):
    """ Finds the similarity of subjects based on Spearmans's Correlation and creates edges.
    
    Parameters
    ----------
    data_for_edge : Pandas DataFrame
        The data used to find similarity.
    
    run_number : Pandas Series
        The run number for each subject.
        
    G : Networkx Graph
        The graph to add edges to.
        
    Returns
    -------
    G : Networkx Graph
        The graph with added edges.
    """
    from scipy.stats import spearmanr
    coeff, p_values = spearmanr(data_for_edge.T)
    for i in range(len(coeff[:,1])): 
        for j in range(len(coeff[1,:])):
            if coeff[i,j]>0.95:
                node1 = run_number[i]
                node2 = run_number[j]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 3)
            elif coeff[i,j]>0.90:
                node1 = run_number[i]
                node2 = run_number[j]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 2)
            elif coeff[i,j]>.85:
                node1 = run_number[i]
                node2 = run_number[j]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 1)
            j += 1
        i += 1
    return G

    ##### Pearsons Correlation #####
def PearsonsCorrelation(data_for_edge, run_number, G):
    """ Finds the similarity of subjects based on Pearson's Correlation and creates edges.
    
    Parameters
    ----------
    data_for_edge : Pandas DataFrame
        The data used to find similarity.
    
    run_number : Pandas Series
        The run number for each subject.
        
    G : Networkx Graph
        The graph to add edges to.
        
    Returns
    -------
    G : Networkx Graph
        The graph with added edges.
    """
    from FeatureSelection.corrcoef import corrcoef
    cor = corrcoef(data_for_edge.T)
    p_values = cor[1]
    coeff = cor[0]
    countI = 0
    for i in p_values[:,1]: 
        countJ = 0
        for j in p_values[:,1]:
            if p_values[countI,countJ]<0.05 and coeff[countI,countJ]>0.99:
                node1 = run_number[countI]
                node2 = run_number[countJ]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 3)
            elif p_values[countI,countJ]<0.05 and coeff[countI,countJ]>0.99:
                node1 = run_number[countI]
                node2 = run_number[countJ]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 2)
            elif p_values[countI,countJ]<0.05 and coeff[countI,countJ]>.985:
                node1 = run_number[countI]
                node2 = run_number[countJ]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 1)
            countJ += 1
        countI += 1
    return G

                ##### Cosine Similarity ######
def CosineSimilarity(data_for_edge, run_number, G):
    """ Finds the similarity of subjects based on Cosine and creates edges.
    
    Parameters
    ----------
    data_for_edge : Pandas DataFrame
        The data used to find similarity.
    
    run_number : Pandas Series
        The run number for each subject.
        
    G : Networkx Graph
        The graph to add edges to.
        
    Returns
    -------
    G : Networkx Graph
        The graph with added edges.
    """
    from sklearn.metrics.pairwise import cosine_similarity
    countI = 0
    for index1, row1 in data_for_edge.iterrows(): 
        countJ = 0
        for index2, row2 in data_for_edge.iterrows():
            if index1 != index2:
                result = cosine_similarity([data_for_edge.iloc[index1,:].values], [data_for_edge.iloc[index2,:].values])
                if result > .995:
                    node1 = run_number[countI]
                    node2 = run_number[countJ]
                    if G.has_edge(node1, node2) == False:
                        G.add_edge(node1,node2, weight = 3)
                elif result > 0.99:
                    node1 = run_number[countI]
                    node2 = run_number[countJ]
                    if G.has_edge(node1, node2) == False:
                        G.add_edge(node1,node2, weight = 2)
                elif result > .985:
                    node1 = run_number[countI]
                    node2 = run_number[countJ]
                    if G.has_edge(node1, node2) == False:
                        G.add_edge(node1,node2, weight = 1)
            countJ += 1
        countI += 1
    return G
                