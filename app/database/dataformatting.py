import json
import numpy as np

def format(json_data):
    with open('prueba3.json', 'r') as fp:
        data = json.load(fp)

    data_dict = {'bvp':[],'gsr':[]}

    for physdataname in ['bvp','gsr']:
        for item in data[physdataname]:
            data_dict[physdataname].extend(data[physdataname][item].values())

    bvp_data = np.array([float(value) for value in data_dict['bvp']])
    eda_data = np.array([float(value) for value in data_dict['gsr']])
    
    return bvp_data, eda_data