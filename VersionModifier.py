import XMLParser, random, sys, json

def majorRange(range, currentVersion):
    newRange = []
    
    for version in range:
        currentVersion = str(currentVersion)
        if version[0] != currentVersion[0] or version == currentVersion:
            newRange.append(version)
            
    return newRange
            

def modifyVersionDependency(pomFile):
    newVersion = 0
        
    #Get all the dependencies in pom.xml
    detailsDependencies = XMLParser.getAllDependenciesOfXMLFile(pomFile)
    
    #Get the range of version and the name of dependency for a random dependency in pom.xml
    versionRangeDependency, dependencyName = XMLParser.getVersionRangeFromJSon(pomFile)
    print("Dependency Name (VersionModifier): " + dependencyName)
    dependencyVersion = detailsDependencies[1][dependencyName]
    newRange = majorRange(versionRangeDependency, dependencyVersion)
    
    if len(newRange) == 0 or len(newRange) == 1:
        check = "False"
    else:
        check = "True"
        
    with open("../range.txt", "w") as out_file:
            out_file.write(check)
            
    print("dependencyVersion : " + str(dependencyVersion))
    print(newRange)
        
    #If the version of a dependency is not specified so we did nothing
    if dependencyVersion != -1 and dependencyVersion != None:
        if len(newRange) > 1:
            if dependencyVersion not in newRange:
                dependencyVersion = newRange[len(newRange) // 2] 
            
            index = newRange.index(dependencyVersion)
            
            if(index == 0):
                newVersion = newRange[random.randint(index + 1, len(newRange) - 1)]
                state = "DOWNGRADE"
            elif(index == len(newRange) - 1):
                newVersion = newRange[random.randint(0, index - 1)]
                state = "UPGRADE"
            else:
                r = random.randint(0,1)
                
                if(r == 0):
                    newVersion = newRange[random.randint(0, index - 1)]
                    state = "UPGRADE"
                else:
                    newVersion = newRange[random.randint(index + 1, len(newRange) - 1)]
                    state = "DOWNGRADE"
                    
                print("OldVersion : " + str(dependencyVersion))
                print("NewVersion : " + str(newVersion))
                    
            
            XMLParser.setDependenciesNewVersion(dependencyName, newVersion, pomFile, detailsDependencies[3])    

            with open("./dependenceInformation.json", "w") as out_file:
                json.dump({'name': dependencyName, 'oldVersion': dependencyVersion, 'newVersion': newVersion, 'state': state}, out_file)
