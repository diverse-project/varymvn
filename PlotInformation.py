import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

def getInformationForPlot():
    with open("./totalExecutionTime.json", "rt") as in_file:
        data = json.load(in_file)
        
    dataNamePlot = []
    dataValuePlot = []    
    
    for key in data.keys():
        dataNamePlot.append(data[key]['dependencyName'])
        
        if(data[key]['executionTime'] == 'nc'):
            dataValuePlot.append(0)
        else: 
            dataValuePlot.append(float(data[key]['executionTime']))

    return dataNamePlot, dataValuePlot


name, value = getInformationForPlot()

y_pos = np.arange(len(name))

plt.figure(figsize=(10, 12), dpi=80)
plt.bar(y_pos, value, align='center', alpha=0.5)
plt.xticks(y_pos, name, rotation=90)
plt.ylabel('Execution Time')
plt.title('Programming language usage')

plt.show()
