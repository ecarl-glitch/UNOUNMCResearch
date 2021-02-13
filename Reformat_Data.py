# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:05:23 2020

@author: Donovan
"""

import pandas as pd
def bothHandReformat(data, file_name, number_of_trials = 5):
    import numpy as np
    data = data.drop(0)
    data.loc[-1] = np.NaN
    all_sessions = {}
    feature_vectors = []
    for i in range(number_of_trials):
        feature_vectors.append([])
    current_session = None
    current_subj = None
    for row in data.values:
        if pd.isna(row[2]):  #If end of session
            temp_dataframe = pd.DataFrame(feature_vectors, columns = ['Subject', 'Trial', 'RBC_RMS', 'RBC_ENV', 'RBC_MEDF', 'RTRI_RMS', 'RTRI_ENV', 'RTRI_MEDF', 'RFCR_RMS', 'RFCR_ENV', 'RFCR_MEDF', 'RED_RMS', 'RED_ENV', 'RED_MEDF', 'LBC_RMS', 'LBC_ENV', 'LBC_MEDF', 'LTRI_RMS', 'LTRI_ENV', 'LTRI_MEDF', 'LFCR_RMS', 'LFCR_ENV', 'LFCR_MEDF', 'LED_RMS', 'LED_ENV', 'LED_MEDF'])
            if current_session not in all_sessions.keys():
                all_sessions[current_session] = temp_dataframe
            else:
                all_sessions[current_session] = all_sessions[current_session].append(temp_dataframe)
                
        else:
            trial = 0
            if pd.isna(row[1]) == False:
                current_session = row[1]
                if pd.isna(row[0]) == False:
                    current_subj = row[0]
                feature_vectors = []
                for i in range(number_of_trials):
                    feature_vectors.append([current_subj, i + 1])
            for col in row[2:-2]:
                if pd.isna(col):
                    trial += 1
                else:
                    feature_vectors[int((trial/2) % number_of_trials)].append(col)
    
    with pd.ExcelWriter(file_name) as writer:  
        for key in all_sessions.keys():
            all_sessions[key].to_excel(writer, sheet_name = str(key), index = False)

        
PT_data = pd.read_excel('First dataset_Donovan_Copy.xlsx', sheet_name = 'PT')
NP_data = pd.read_excel('First dataset_Donovan_Copy.xlsx', sheet_name = 'NP')
WR_data = pd.read_excel('First dataset_Donovan_Copy.xlsx', sheet_name = 'WR')
WL_data = pd.read_excel('First dataset_Donovan_Copy.xlsx', sheet_name = 'WL')
bothHandReformat(PT_data, 'PT.xlsx')
bothHandReformat(NP_data, 'NP.xlsx')
bothHandReformat(WR_data, 'WR.xlsx')
bothHandReformat(WL_data, 'WL.xlsx')
