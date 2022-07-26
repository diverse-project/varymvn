from genericpath import isdir
import xml.dom.minidom as DM
import json, re, sys, os, jsonlines

def getBuildInfo():
    with open("./buildOutput.txt", "r") as in_file: 
        for line in in_file:
            if("BUILD SUCCESS" in line):
                return True
            elif("BUILD FAILURE" in line):
                return False
    
def getTSInfo():
    infoTS = {"run" : 0, "fail": 0, "error": 0, "skip": 0}
    
    testRegex = re.compile("run:")
    failRegex = re.compile("^FAILURE")
    successRegex = re.compile("^SUCCESS")
    with open("./testOutput.txt", "r") as in_file:
        for line in in_file:
            lineSplit = line.split(" ")
            
            if len(lineSplit) > 2:
                if re.match(failRegex, lineSplit[2]):
                    return False, infoTS
                elif re.match(successRegex, lineSplit[2]):
                    return True, infoTS
                elif re.match(testRegex, lineSplit[1]):
                    print(lineSplit)
                    print(lineSplit[2][0:1])
                    infoTS["run"] += int(lineSplit[2][0:1])
                    infoTS["fail"] += int(lineSplit[4][0:1])
                    infoTS["error"] += int(lineSplit[6][0:1])
                    infoTS["skip"] += int(lineSplit[8][0:1])
                
def recursiveTestPath():
    if "target" in os.listdir("."):
        return getExecutionTimeWithTarget(".")            
    else:
        return getExecutionTimeWithNestedTarget(".")
    
    
def getExecutionTimeWithTarget(path):
    regexString = re.compile("^TEST")
    
    if os.path.isdir(path + "/target/surefire-reports"):
        for f in os.listdir(path + "/target/surefire-reports"):
                fileCheck = re.match(regexString, f)
                if fileCheck:
                    doc = DM.parse(path + "/target/surefire-reports/" + f)
                    
                    testSuite = doc.getElementsByTagName("testsuite")
                    name = testSuite[0].getAttribute("name")
                    executingTime = testSuite[0].getAttribute("time")

                    try:
                        with open("./resultExecutionTime.json", "r") as in_file:
                            data = json.load(in_file)
                    except IOError:
                        print("The file resultExecutionTime.json didn't exist.")
                        data = {"totalTime": "0.0", "failure": 0}
                        
                    time = float(data["totalTime"])
                    time += float(executingTime)
                    data["totalTime"] = str(time)
                    
                    data[name] = executingTime
                    
                    with open("./resultExecutionTime.json", "w") as out_file:
                        json.dump(data, out_file)

def getExecutionTimeWithNestedTarget(clonePath):
    targetPath = []   
        
    for dir in os.listdir(clonePath):
        if os.path.isdir(dir):
            if "target" in os.listdir(clonePath + "/" + dir):
                targetPath.append(clonePath + "/" + dir)
            
    for path in targetPath:
        getExecutionTimeWithTarget(path)
    
def getExecutionTimeForEachProject(newVersionDependence):
    recursiveTestPath()
    
    try:
        
        with open("./resultExecutionTime.json", "rt") as in_file:
            data = json.load(in_file)
    except IOError:
        print("The file resultExecutionTime.json didn't exist.")
        data = "nc"   
        
    try:
        with open("./dependenceInformation.json", "rt") as in_file:
            dependencyInformation = json.load(in_file)
    except IOError:
        print("The file dependenceInformation.json didn't exist.")
        dependencyInformation = {'name': "nc", 'oldVersion': "nc", 'newVersion': "nc"}
        
    try:
        with jsonlines.open("../totalExecutionTime.json", "r") as out_file:
            dataTime = out_file.read()
    except IOError:
        print("The file totalExecutionTime.json didn't exist.")
        dataTime = {}
        
    tsPassed, infoTs = getTSInfo()
        
    with jsonlines.open("../totalExecutionTime.json", "w") as out_file:
        if(data != "nc"):    
            dataTime[newVersionDependence] = {
                'dependencyName': dependencyInformation['name'],
                'dependencyOldVersion': dependencyInformation['oldVersion'],
                'dependencyNewVersion': dependencyInformation['newVersion'],
                'isBuild': getBuildInfo(),
                'passedTS': tsPassed,
                'NumberOfExecutedTest': infoTs["run"],
                'NumberOfFailTest': infoTs["fail"],
                'NumberOfErrorTest': infoTs["error"],
                'NumberOfSkippedTest': infoTs["skip"],
                'executionTime': data['totalTime'],
                'pathToBuildInformation': newVersionDependence + "/buildOutput.txt",
                'pathToTestFile': newVersionDependence + "/"
            }
        else:
            dataTime[newVersionDependence] = {
                'dependencyName': dependencyInformation['name'],
                'dependencyOldVersion': dependencyInformation['oldVersion'],
                'dependencyNewVersion': dependencyInformation['newVersion'],
                'isBuild': getBuildInfo(),
                'passedTS': tsPassed,
                'NumberOfExecutedTest': infoTs["run"],
                'NumberOfFailTest': infoTs["fail"],
                'NumberOfErrorTest': infoTs["error"],
                'NumberOfSkippedTest': infoTs["skip"],
                'executionTime': data,
                'pathToBuildInformation': newVersionDependence + "/buildOutput.txt",
                'pathToTestFile': newVersionDependence + "/"
            }
            
        out_file.write(dataTime)