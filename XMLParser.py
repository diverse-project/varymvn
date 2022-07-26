import xml.dom.minidom as DM
import json, re
from urllib.request import urlopen

'''
    Return the value contain in XML node
'''
def getDependenciesDetails(nodelist):
    for node in nodelist:
        if node.firstChild.nodeType == node.TEXT_NODE or node.CDATA_SECTION_NODE:
            details = node.firstChild.nodeValue
            return details

'''
    Return the current version of a dependency
'''
def getDependenciesCurrentVersion(nodelist):
    if nodelist == []:
        return -1
        
    for node in nodelist:
        if node.firstChild.nodeType == node.TEXT_NODE:
            details = node.firstChild.nodeValue
    return details 

'''
    Set the new version in two differents way
'''
def setDependenciesNewVersion(propertyName, newVersion, pomFile, propertiesVersion):
    doc = DM.parse(pomFile)
    
    if propertiesVersion == True:
        nodelist = doc.getElementsByTagName(propertyName)
        for node in nodelist:
            if node.firstChild.nodeType == node.TEXT_NODE:
                node.firstChild.nodeValue = str(newVersion)
    else:
        dependencies = doc.getElementsByTagName('dependency')
        
        for dependency in dependencies:
            groupId = getDependenciesDetails(dependency.getElementsByTagName('groupId'))
        
            if groupId == propertyName:
                dependency.childNodes[5].firstChild.nodeValue = str(newVersion)
                break
    
    
    with open(pomFile, "w") as file:
        file.write(doc.toxml())
        file.close()

'''
    Return the groupId, artifactId and version of each dependencies in pom.xml
'''
def getAllDependenciesOfXMLFile(pomFile):
    dependenciesDetails = {}
    dependenciesVersion = {}
    dependenciesPropertyName = {}
    
    #parse the pom.xml file
    doc = DM.parse(pomFile)

    #get all the XML node which has a dependency
    dependencies = doc.getElementsByTagName('dependency')
    for dependency in dependencies:
        groupID = getDependenciesDetails(dependency.getElementsByTagName('groupId'))     
        
        #put in dict the groupId for the key and the artifactId for the value
        artifactID = getDependenciesDetails(dependency.getElementsByTagName('artifactId'))
        dependenciesDetails[artifactID] = groupID

        version = getDependenciesDetails(dependency.getElementsByTagName('version'))
        
        if(version != None):
            #Check if the value of version tag name is a variable or not
            checkVersion = re.match("^\$", version)
            
            if checkVersion:        
                propertyName = version[2:len(version)-1]
            
                dependenciesPropertyName[groupID] = groupID
            
                dependenciesVersion[artifactID] = getDependenciesCurrentVersion(doc.getElementsByTagName(propertyName))
                
                propertiesVersion = True
            else: 
                dependenciesPropertyName[groupID] = groupID
                
                dependenciesVersion[artifactID] = version
                
                propertiesVersion = False
        else:
            dependenciesPropertyName[groupID] = groupID
                
            dependenciesVersion[artifactID] = version
                
            propertiesVersion = False
            
            with open("range.txt", "w") as out_file:
                out_file.write("False")
        
    return dependenciesDetails, dependenciesVersion, dependenciesPropertyName, propertiesVersion
        
def getVersionRangeFromJSon(pomFile):
    listOfDependencies = getAllDependenciesOfXMLFile(pomFile)
    allReleaseVersion = []
    regexString = re.compile("^[0-9]?[0-9]?.[0-9]?[0-9]?(.[0-9]?[0-9]?)?$")
    
    with open("../dependenciesName.txt", "r") as in_file:
        artifactID = in_file.readline()
        print(artifactID)
    
    #Request to Maven Central REST API which get all the information of a specific dependence with is groupId and artifactId
    url = "https://search.maven.org/solrsearch/select?q=g:" + listOfDependencies[0][artifactID[0:-1]] + "+AND+a:" + artifactID[0:-1] + "&core=gav&rows=500&wt=json"
    
    response = urlopen(url)
    data = json.loads(response.read())
         
    t = data['response']['docs']
    for item in t:
        version = item['v']
        
        #Check if the version is a release or not
        checkVersion = re.match(regexString, version)
        
        #If it's not a release so it append in the range
        if checkVersion:
            allReleaseVersion.append(version)
                
                
    print(listOfDependencies[0])
    print(artifactID)
    return allReleaseVersion, artifactID[0:-1]