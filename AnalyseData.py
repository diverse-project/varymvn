import os, csv, sys, re, XMLParser, json

from numpy import mean
import pandas as pd

def construcCSV():
    dirRegex = "^" + str(sys.argv[1][14:-6]) + "_"
    dependenciesName, dependenciesVersion, dependenciesPropertyName, propertiesVersion = XMLParser.getAllDependenciesOfXMLFile("inputProject" + str(sys.argv[1])[13:-6] + "/pom.xml")
    outputData = []

    t = []

    #Build of the header of the CSV file
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
    t.append("Change")

    outputData.append(t)

    #Get all the informations of each clone of the initial project
    for f in os.listdir(str(sys.argv[1])):
        fileCheck = re.match(dirRegex, f)
        #Check if dir is a clone or not
        if fileCheck:
            try:
                with open(str(sys.argv[1]) + "/totalExecutionTime.json", "r") as in_file:
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
                    
                    if ':' in otherData[f]['executionTime']:
                        tempData.append(convertTimeInSeconds(otherData[f]['executionTime']))
                    else:
                        tempData.append(otherData[f]['executionTime'])
                        
                    tempData.append(otherData[f]['change'])
                            
                    outputData.append(tempData)
            except IOError:
                print("The file dependenceInformation.json or totalExecutionTime.json didn't exist.")
                
    with open(str(sys.argv[1]) + "/dataTab.csv", "w", newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(outputData)
    
def convertTimeInSeconds(timeStr):
    temp = timeStr.split(":")
    return (float(temp[0]) * 60) + float(temp[1])

def getEssentialInformation():
    dependenciesName, dependenciesVersion, dependenciesPropertyName, propertiesVersion = XMLParser.getAllDependenciesOfXMLFile("inputProject" + str(sys.argv[1])[13:-6] + "/pom.xml")
    data = pd.read_csv(str(sys.argv[1]) + "/dataTab.csv")
    
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
        
        if dependenciesExecutionTime[key] != [] and dependenciesExecutionTime[key][0] != 'nc':
            print(dependenciesExecutionTime[key])
            temp.append(key)
            temp.append(mean(dependenciesExecutionTime[key]))
            temp.append(min(dependenciesExecutionTime[key]))
            temp.append(max(dependenciesExecutionTime[key]))
            outDataStruct.append(temp)
    
    temp = []
    
    executionTime = data['Execution Time']
    print(executionTime)
    if len(executionTime) >= 1 and executionTime[0] != "nc":
        temp.append("All dependencies")
        temp.append(mean(executionTime))
        temp.append(min(executionTime))
        temp.append(max(executionTime))
    
    outDataStruct.append(temp)
    
    with open(str(sys.argv[1]) + "/essentialData.csv", "w", newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(outDataStruct)
                
    df = pd.read_csv(str(sys.argv[1]) + '/essentialData.csv')
    
    print(df)
                
def construcPlotProjectCSV():
    outputData = []
    t = []
    
    t.append("Project")
    t.append("Execution time")
    t.append("State")
    
    outputData.append(t)
    
    t = []
    
    with open("inputProject/" + str(sys.argv[1])[14:-6] + "/totalExecutionTime.json", "r") as in_file:
        initialTime = json.load(in_file)
        t.append("Initial Project")
        if ':' in initialTime["original"]["executionTime"]:
            t.append(convertTimeInSeconds(initialTime["original"]["executionTime"]))
        else:
            t.append(initialTime["original"]["executionTime"])
        
        outputData.append(t)
        t = []
    

    data = pd.read_csv(str(sys.argv[1]) + "/dataTab.csv")
    dependencyName = data["Dependency changed"]
    execTime = data["Execution Time"]
    state = data["Change"]

    i = 0
    while i < len(execTime):
        if execTime[i] == "nc" :
            break
                
        if str(execTime[i]) != "nan" and dependencyName[i] != "nc":
            t.append(dependencyName[i])
            t.append(float(execTime[i]))
            t.append(state[i])
                
            outputData.append(t)
            t = []
        
        i += 1
                
    with open(str(sys.argv[1]) + "/plotProjectData.csv", "w", newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(outputData)
        
def rateExecutionTime():
    data = pd.read_csv(str(sys.argv[1]) + "/dataTab.csv")
    initProject = pd.read_csv(str(sys.argv[1]) + "/plotProjectData.csv")["Execution time"][0]
    state = data["Change"]
    execTime = data["Execution Time"]
    rateChange = [0,0,0]
    i = 0
    
    while i < len(execTime):
        if execTime[i] >= float(initProject):
            rateChange[0] += 1
        elif execTime[i] < float(initProject):
            if state[i] == "UPGRADE":
                rateChange[1] += 1
            elif state[i] == "DOWNGRADE":
                rateChange[2] += 1
        
        i += 1
        
    with open(str(sys.argv[1]) + "/result.txt", "w") as out_file:
        out_file.write(str(rateChange[0]) + "," + str(rateChange[1]) + "," + str(rateChange[2]))    
            
    
if sys.argv[2] == "0":
    construcCSV()
elif sys.argv[2] == "1":
    getEssentialInformation()
elif sys.argv[2] == "2":
    construcPlotProjectCSV()
elif sys.argv[2] == "3":
    rateExecutionTime()