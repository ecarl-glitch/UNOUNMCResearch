# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:02:51 2020

@author: Donovan
"""
import pandas as pd
import xlrd

def saveDictAsXLSX(dictionary, save_file_name = 'Combined'):
    with pd.ExcelWriter(str(save_file_name) + '.xlsx') as writer:  
        for key in dictionary.keys():
            dictionary[key].to_excel(writer, sheet_name = str(key), index = False)

def reformatColumns(data, file_name):
    for column in data.columns:
        if column != 'Subject' and column != 'Trial':
            data.rename(columns={str(column) : file_name + '_' + str(column)}, inplace=True)
    return data

def readyDataset(file_name, sheet_names):
    ready_data = {}
    for sheet_name in sheet_names:
        ready_data[str(sheet_name)] = reformatColumns(pd.read_excel(file_name + '.xlsx', sheet_name = str(sheet_name)), file_name)
    return ready_data

def combineDatasets(file_names):
    combined_data = {}
    while file_names != []:
        file_name = str(file_names.pop())
        file_information = xlrd.open_workbook(r'' + file_name + '.xlsx', on_demand = True)
        data = readyDataset(file_name, file_information.sheet_names())
        if combined_data != {}:
            for sheet_name in file_information.sheet_names():
                combined_data[str(sheet_name)] = combined_data[str(sheet_name)].merge(data[str(sheet_name)], on = ['Subject', 'Trial'])
        else:
            combined_data = data
    return combined_data

file_names = ['WR', 'WL', 'NP', 'PT']   #This is the list of xlsx files you wish to combine
save_file_name = 'ALL'                  #This is what you would like to save the combined file as

#file_names = ['WR', 'WL']               #This is the list of xlsx files you wish to combine
#save_file_name = 'WB'                   #This is what you would like to save the combined file as

combined_data = combineDatasets(file_names)
saveDictAsXLSX(combined_data, save_file_name)
