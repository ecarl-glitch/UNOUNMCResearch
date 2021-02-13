# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:38:06 2020

@author: Donovan
"""
from scipy.stats import spearmanr
import xlrd
import pandas as pd

def averageTrialsPerSubject(data):
    average_data = data.drop('Trial', axis = 1)
    return average_data.groupby('Subject').mean()

def allTrials(data):
    return data.groupby(['Subject', 'Trial']).mean()

def saveSpearman(file_names, preprocess):
    for file_name in file_names:
        file_information = xlrd.open_workbook(r'Second Set/Data/' + file_name + '.xlsx', on_demand = True)
        sheet_names = file_information.sheet_names()

        for sheet_name in sheet_names:
            data = pd.read_excel('Second Set/Data/' + str(file_name) + '.xlsx', sheet_name = str(sheet_name))
            average_data = preprocess(data)
            X = average_data.values
            y = average_data.index.values
            try:
                coeff, p_values = spearmanr(X.T) 
    #            for row_idx, row in enumerate(coeff):
    #                for col_idx, col in enumerate(row):
    #                    if col >= .8 and row_idx < col_idx:
    #                        print(str(file_name) + '_' + str(sheet_name) + ' found: (' + str(row_idx), str(col_idx) + ') value = ' + str(col))
                coeff = pd.DataFrame(coeff, columns = list(range(1, len(coeff) + 1)))
                coeff['Subject'] = list(range(1, len(coeff) + 1))
                coeff.to_csv('Spearman_' + str(file_name) + '_' + str(sheet_name) + '.csv', index = list('Subject').append(list(coeff['Subject'])), index_label = 'Subject')
            except(TypeError):
                print(str(file_name) + '_' + str(sheet_name) + '\n\tOnly 1 row or col')
            
file_names = ['PT', 'NP', 'WB', 'WL', 'WR', 'ALL']
saveSpearman(file_names, averageTrialsPerSubject)
