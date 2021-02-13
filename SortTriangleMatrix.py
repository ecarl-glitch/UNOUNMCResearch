# -*- coding: utf-8 -*-
"""
Created on Tue May 19 08:54:08 2020

@author: Donovan
"""
import pandas as pd
from os import listdir
from os.path import isfile, join

PATH = 'Second Set/Spearman/'
FILES = [f for f in listdir(PATH) if isfile(join(PATH, f))]



def triangleMatrix2Array(matrix):
    matrix_list = []
    matrix = matrix.drop('Subject', axis = 1)
    for ridx, row in enumerate(matrix.values[:-2]):
        for cidx, col in enumerate(row[:-2]):
            if ridx < cidx:
                matrix_list.append(col)
    return matrix_list

def createHistrogram(values, ymax = None, name = None):
    import matplotlib.pyplot as plt
    from scipy.stats import skew 
    plt.hist(values, bins = [value/1000 for value in range(860,1005,5)])
    if ymax != None:
        plt.ylim(ymin = 0, ymax = ymax)
    if name != None:
        plt.savefig(name)
    plt.show()

masterlist = []
session_dict = {'0' : [], '1 wk' : [], '4 wks' : [],}
task_dict = {'All' : [], 'WB' : [], 'WL' : [], 'WR' : [], 'PT' : [], 'NP' : []}
task = 0
for idx, file in enumerate(FILES):
    matrix = pd.read_csv(PATH + str(file))
    matrix_list = triangleMatrix2Array(matrix)
    sorted_list = sorted(matrix_list)
    masterlist.extend(sorted_list)
    if file[-5] == '0':
        session_dict['0'].extend(sorted_list)
    elif file[-5] == 'k':
        session_dict['1 wk'].extend(sorted_list)
    elif file[-5] == 's':
        session_dict['4 wks'].extend(sorted_list)
    
    if file[9] == 'A':
        task_dict['All'].extend(sorted_list)
    elif file[9] == 'W':
        if file[10] == 'B':
            task_dict['WB'].extend(sorted_list)
        elif file[10] == 'L':
            task_dict['WL'].extend(sorted_list)
        elif file[10] == 'R':
            task_dict['WR'].extend(sorted_list)
    elif file[9] == 'P':
        task_dict['PT'].extend(sorted_list)
    elif file[9] == 'N':
        task_dict['NP'].extend(sorted_list)
        
    with open(PATH + 'Sorted/' + str(file),'w') as f:
        f.write(str(sorted_list)[1:-1])
    print(str(file))
    createHistrogram(sorted_list, 50, PATH + 'Hist/Individual/' + str(file)[9:-4] + '_Hist.png')
    
print('Master')
createHistrogram(sorted(masterlist), name = PATH + 'Hist/Master.png')

for key in session_dict.keys():
    print(str(key))
    createHistrogram(sorted(session_dict[key]), 120, PATH + 'Hist/Session/' + str(key) + '.png')

for key in task_dict.keys():
    print(str(key))
    createHistrogram(sorted(task_dict[key]), 120, PATH + 'Hist/Task/' + str(key) + '.png')

