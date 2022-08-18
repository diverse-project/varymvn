import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os, sys

def plotCompareInitialProjectWithCopy():
    fig, axes = plt.subplots(nrows=1, ncols=2)
    
    sns.set(style='whitegrid')

    dataSet = pd.read_csv(str(sys.argv[1]) + "/plotProjectData.csv")
 
    graph = sns.boxplot(ax=axes[0], x="Project", y="Execution time", data=dataSet[1:-1])

    graph.axhline(dataSet["Execution time"][0], color='r', linewidth=2)
    
    label = ["Initial Project", "UPGRADE", "DOWNGRADE"]
    
    with open(str(sys.argv[1]) + "/result.txt", "rt") as in_file:
        temp = in_file.read()
    
    data = temp.split(",")
    
    axes[1].pie(data, labels=label, colors=sns.color_palette('pastel'), autopct='%0.0f%%')

    plt.show()
    
    
if sys.argv[2] == "0":
    plotCompareInitialProjectWithCopy()