import os, csv, sys, re, XMLParser, json
import pandas as pd

dirRegex = "^" + str(sys.argv[1]) + "_"
dependenciesName, dependenciesVersion, dependenciesPropertyName, propertiesVersion = XMLParser.getAllDependenciesOfXMLFile(str(sys.argv[1]) + "/pom.xml")
outputData = []

t = []


print(dependenciesVersion)
for d in dependenciesName:    
    t.append(d)
    
t.append("isBuild?")
t.append("passedTS?")
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
                
                tempData.append(otherData[f]['isBuild'])
                tempData.append(otherData[f]['passedTS'])
                tempData.append(otherData[f]['executionTime'])
                        
                outputData.append(tempData)
        except IOError:
            print("The file dependenceInformation.json or totalExecutionTime.json didn't exist.")
            
with open(str(sys.argv[1]) + "_clone" + "/dataTab.csv", "w", newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerows(outputData)
            
df = pd.read_csv(str(sys.argv[1]) + "_clone" + '/dataTab.csv')

print(df)