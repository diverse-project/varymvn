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
    regex = re.compile("BUILD.FAILURE")
    with open("./testOutput.txt", "r") as in_file:
        for line in in_file:
            check = re.match(regex, line)
            if check:
                return False
    
    return True
                

def getExecutionTimeTestSuite():
    surefirePath = str(sys.argv[1])
    regexString = re.compile("^TEST")
    
    for f in os.listdir(surefirePath):
        fileCheck = re.match(regexString, f)
        if fileCheck:
            
            doc = DM.parse(surefirePath + f)
            
            testsuite = doc.getElementsByTagName("testsuite")
            name = testsuite[0].getAttribute("name")
            executingTime = testsuite[0].getAttribute("time")
            
            try:
                with open("./resultExecutionTime.json", "r") as fp:
                    data = json.load(fp)
            except IOError:
                print("The file resultExecutionTime.json didn't exist.")
                data = {"totalTime" : "0.0", "failure": 0}
                
            data['failure'] = data['failure'] or testsuite[0].getAttribute("failures")
            
            time = float(data["totalTime"])
            time += float(executingTime)
            data["totalTime"] = str(time)    
                
            data[name] = executingTime     
            
            
            with open("./resultExecutionTime.json", "w") as outfile:
                json.dump(data, outfile)
        
    
def getExecutionTimeForEachProject():
    try:
        getExecutionTimeTestSuite()
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
        
    with jsonlines.open("../totalExecutionTime.json", "w") as out_file:
        if(data != "nc"):    
            dataTime[str(sys.argv[2])] = {
                'dependencyName': dependencyInformation['name'],
                'dependencyOldVersion': dependencyInformation['oldVersion'],
                'dependencyNewVersion': dependencyInformation['newVersion'],
                'isBuild': getBuildInfo(),
                'passedTS': getTSInfo(),
                'executionTime': data['totalTime'],
                'pathToBuildInformation': str(sys.argv[2]) + "/buildOutput.txt",
                'pathToTestFile': str(sys.argv[2]) + "/" + str(sys.argv[1])
            }
        else:
            dataTime[str(sys.argv[2])] = {
                'dependencyName': dependencyInformation['name'],
                'dependencyOldVersion': dependencyInformation['oldVersion'],
                'dependencyNewVersion': dependencyInformation['newVersion'],
                'isBuild': getBuildInfo(),
                'passedTS': getTSInfo(),
                'executionTime': data,
                'pathToBuildInformation': str(sys.argv[2]) + "/buildOutput.txt",
                'pathToTestFile': str(sys.argv[2]) + "/" + str(sys.argv[1])
            }
            
        out_file.write(dataTime)


getExecutionTimeForEachProject()