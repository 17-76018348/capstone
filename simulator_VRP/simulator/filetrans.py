import pandas as pd
import json
command = 'loadCarrier /home/didrmswp/capstone/simulator_VRP/instance_vrp/rizzo_stguillain_ds-vrptw/OC-100-70-25%-1/12-18-0-0/lockers-no/carrier.json'
command = command.replace('loadCarrier ', '', 1).rstrip()
data = None
with open(command) as data:
    dataLoaded = json.load(data)
    data = pd.DataFrame.from_dict({(i,j): dataLoaded[i][j] 
                           for i in dataLoaded.keys() 
                           for j in dataLoaded[i].keys()},
                       orient='index')
print(data)
#