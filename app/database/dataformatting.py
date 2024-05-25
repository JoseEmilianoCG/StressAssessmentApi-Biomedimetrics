import numpy as np

def format(data):
    data_dict = {'bvp':[],'gsr':[]}

    for physdataname in ['bvp','gsr']:
        data_dict[physdataname] = data[physdataname]

    bvp_data = np.array([float(value) for value in data_dict['bvp']])
    eda_data = np.array([float(value) for value in data_dict['gsr']])

    return bvp_data, eda_data