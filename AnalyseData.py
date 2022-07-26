import os, csv, sys, re, XMLParser, json

from numpy import mean
import pandas as pd

def construcCSV():
    dirRegex = "^" + str(sys.argv[1]) + "_"
    dependenciesName, dependenciesVersion, dependenciesPropertyName, propertiesVersion = XMLParser.getAllDependenciesOfXMLFile(str(sys.argv[1]) + "/pom.xml")
    outputData = []

    t = []


    print(dependenciesVersion)
    for d in dependenciesName:    
        t.append(d)
        
    t.append("Dependency changed")
    t.append("isBuild?")
    t.append("passedTS?")
    t.append("Number of executed test")
    t.append("Number of fail test")
    t.append("Number of error test")
    t.append("Number of skip test")
    t.append("Execution Time")

    outputData.append(t)

    for f in os.listdir(str(sys.argv[1]) + "_clone"):
        fileCheck = re.match(dirRegex, f)
        if fileCheck:
            try:
                with open(str(sys.argv[1]) + "_clone/" + "totalExecutionTime.json", "r") as in_file:
                    otherData = json.load(in_file)
                    
                if(f in otherData.keys()):
                    tempData = []
                    
                    for d in dependenciesName:
                        if(d == otherData[f]['dependencyName']):
                            tempData.append(otherData[f]['dependencyNewVersion'])
                        else:
                            tempData.append(dependenciesVersion[d])
                    
                    tempData.append(otherData[f]['dependencyName'])
                    tempData.append(otherData[f]['isBuild'])
                    tempData.append(otherData[f]['passedTS'])
                    tempData.append(otherData[f]['NumberOfExecutedTest'])
                    tempData.append(otherData[f]['NumberOfFailTest'])
                    tempData.append(otherData[f]['NumberOfErrorTest'])
                    tempData.append(otherData[f]['NumberOfSkippedTest'])
                    tempData.append(otherData[f]['executionTime'])
                            
                    outputData.append(tempData)
            except IOError:
                print("The file dependenceInformation.json or totalExecutionTime.json didn't exist.")
                
    with open(str(sys.argv[1]) + "_clone" + "/dataTab.csv", "w", newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(outputData)
                
    df = pd.read_csv(str(sys.argv[1]) + "_clone" + '/dataTab.csv')
    

def getEssentialInformation():
    dependenciesName, dependenciesVersion, dependenciesPropertyName, propertiesVersion = XMLParser.getAllDependenciesOfXMLFile(str(sys.argv[1]) + "/pom.xml")
    data = pd.read_csv(str(sys.argv[1]) + "_clone/" + "dataTab.csv")
    
    outDataStruct = []
    
    temp = []
    
    temp.append("Dependency name")
    temp.append("Average")
    temp.append("Minimum")
    temp.append("Maximum")
    
    outDataStruct.append(temp)
    
    dependenciesExecutionTime = {}
    
    for name in dependenciesName:
        dependenciesExecutionTime[name] = []
        
    dataIterator = data.iterrows()
    line = next(dataIterator, None)
    
    while line != None:
        if line[1]['Dependency changed'] != "nc":
            dependenciesExecutionTime[line[1]['Dependency changed']].append(line[1]['Execution Time'])
        
        line = next(dataIterator, None)
    
    
    for key in dependenciesExecutionTime.keys():
        temp = []
        
        if dependenciesExecutionTime[key] != []:
            temp.append(key)
            temp.append(mean(dependenciesExecutionTime[key]))
            temp.append(min(dependenciesExecutionTime[key]))
            temp.append(max(dependenciesExecutionTime[key]))
            outDataStruct.append(temp)
    
    temp = []
    
    executionTime = data['Execution Time']
    temp.append("All dependencies")
    temp.append(mean(executionTime))
    temp.append(min(executionTime))
    temp.append(max(executionTime))
    
    outDataStruct.append(temp)
    
    with open(str(sys.argv[1]) + "_clone" + "/essentialData.csv", "w", newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(outDataStruct)
                
    df = pd.read_csv(str(sys.argv[1]) + "_clone" + '/essentialData.csv')
    
    print(df)
    
    
    
if sys.argv[2] == "0":
    construcCSV()
elif sys.argv[2] == "1":
    getEssentialInformation()