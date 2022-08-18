import sys, os, shutil, subprocess, DependenciesName, VersionModifier, DataGet

def launch(pathFile):
    projectName = str(pathFile)
    
    os.chdir(projectName)
    os.system("sudo mvn --log-file ./buildOutput.txt compile")
    os.system("sudo mvn test > ./testOutput.txt")
    
    os.system("sudo rm -rf " + str(sys.argv[1]) + "/totalExecutionTime.json " + str(sys.argv[1]) + "/resultExecutionTime.json")
    
    DataGet.getOriginalProjectInformation()
    
    os.chdir("../..")
    
    newProjectName = projectName[13:len(projectName)] + "_clone"
    os.system("sudo rm -rf outputProject/" + newProjectName + " totalExecutionTime.json dataPlot.json")

    os.mkdir("outputProject/" + newProjectName)   
    os.chdir("outputProject/" + newProjectName)

    newProjectName = projectName[13:len(projectName)]

    DependenciesName.addNameToFile("../../" + projectName + "/pom.xml")

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
            
            print(os.getcwd())
            print(newVersionDependence)
            shutil.copytree("../../" + projectName, newVersionDependence)
            
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
            
            newVersionDependence = projectName[13:len(projectName)]
            
            i += 1
            
        count += 1
        
        newProjectName = projectName[13:len(projectName)]
        DependenciesName.delNameToFile()

    if os.path.isfile("range.txt"):
        os.system("sudo rm range.txt dependenciesName.txt")
    else:
        os.system("sudo rm dependenciesName.txt")
        print("Aucune dépendence à modifier dans le projet.")
        
if str(sys.argv[1]) == "inputProject/":
    for dir in os.listdir("inputProject/"):
        launch("inputProject/" + dir)
        os.chdir("../..")
else:
    launch(str(sys.argv[1]))