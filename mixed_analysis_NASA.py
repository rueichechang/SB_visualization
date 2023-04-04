import argparse
import os
import copy
import json
from generate_analysis import generate_result
import pandas as pd


sighted_folder = "/Users/rueichechang/Documents/SB_visualization/sighted/"
blind_folder = "/Users/rueichechang/Documents/SB_visualization/blind/"

ID = [str(i) for i in range(1,10)]
scenes = ['scene1', 'scene2', 'scene3']
conditions = ['proxies', 'baseline', 'noise_cancellation']
loggers = ['logger_0', 'logger_1', 'logger_2', 'logger_3', 'logger_4']


ANALYSIS_DICT = {
    "Mental_Demand": 0,
    "Physical_Demand": 0,
    "Temporal_Demand": 0,
    "Perforamnce": 0,
    "Effort": 0,
    "Frustration": 0,
    "Overall": 0,
}

header = [
    'BlindOrSighted', 
    'RandomInterceptByID',
    'Scene', 
    'Condition',
    
    'Mental_Demand',
    'Physical_Demand',
    'Temporal_Demand',
    'Perforamnce',
    'Effort',
    'Frustration',
    'Overall',
    
]



def create_NASA_csv(df, path, person_type):
    # df = pd.DataFrame(columns = header)
    

    for id in ID:    
        json_file = path + id + "/NASA.json"
        if not os.path.isfile(json_file): print(json_file + " not found")
        with open(json_file) as json_file:
            data = json.load(json_file)

        for scene in scenes:
            for condition in conditions:
                for key in data:
                    if scene in key and condition in key:
                        temp_dict = {}
                        temp_dict['BlindOrSighted'] = person_type
                        temp_dict['RandomInterceptByID'] = int(id) if person_type == "blind" else int(id)+9
                    
                        temp_dict['Scene']           = scene
                        temp_dict['Condition']       = condition
                        temp_dict['Mental_Demand']   = data[key]['Mental_Demand']
                        temp_dict['Physical_Demand'] = data[key]['Physical_Demand']
                        temp_dict['Temporal_Demand'] = data[key]['Temporal_Demand']
                        temp_dict['Perforamnce']     = data[key]['Perforamnce']
                        temp_dict['Effort']          = data[key]['Effort']
                        temp_dict['Frustration']     = data[key]['Frustration']
                        temp_dict['Overall']         = data[key]['Overall']
                        df =  pd.concat([df, pd.DataFrame.from_records([temp_dict])], ignore_index=True)

    return df



if __name__ == "__main__":
    df = pd.DataFrame(columns = header)
    df = create_NASA_csv(df, blind_folder, "blind")
    df = create_NASA_csv(df, sighted_folder, "sighted")
    df.to_csv('soundblender_NASA.csv',index=True)