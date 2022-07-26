import sys, os, shutil, subprocess, DependenciesName, VersionModifier, DataGet

projectName = str(sys.argv[1])
newProjectName = projectName + "_clone"
os.system("sudo rm -rf " + newProjectName + " totalExecitonTime.json dataPlot.json")

os.mkdir(newProjectName)
os.chdir(newProjectName)

newProjectName = projectName

DependenciesName.addNameToFile("../" + projectName + "/pom.xml")

subprocess.call(['chmod', '777', 'dependenciesName.txt'])

dependenceNameFile = open('dependenciesName.txt', 'rt')
lines = dependenceNameFile.readlines()
dependenceNameFile.close()

count = 1

for line in lines:
    newProjectName += "_" + str(count)
    
    i = 1
    
    while i <= int(sys.argv[2]):
        newVersionDependence = newProjectName + "_" + str(i)
        
        shutil.copytree("../" + projectName, newVersionDependence)
        
        os.chdir(newVersionDependence)
        VersionModifier.modifyVersionDependency("pom.xml")
        
        rangeFile = open("../range.txt", "r")
        range = rangeFile.readlines()
        rangeFile.close()
        
        if range[0] == "False":
            os.chdir("..")
            newVersionDependence = newProjectName
            break
        
        os.system("sudo mvn --log-file ./buildOutput.txt compile")
        os.system("sudo mvn test > ./testOutput.txt")
        
        DataGet.getExecutionTimeForEachProject(newVersionDependence)
        
        os.chdir("..")
        
        newVersionDependence = projectName
        
        i += 1
        
    count += 1
    
    newProjectName = projectName
    DependenciesName.delNameToFile()

os.system("sudo rm range.txt dependenciesName.txt")
