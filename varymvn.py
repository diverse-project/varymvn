import sys, os, shutil, subprocess, DependenciesName, VersionModifier, DataGet

def launch(pathFile):
    projectName = str(pathFile)
    
    #First of all we build and test the initial project in order to have the execution time of the initial project
    os.chdir(projectName)
    os.system("sudo mvn --log-file ./buildOutput.txt compile")
    os.system("sudo mvn test > ./testOutput.txt")
    
    os.system("sudo rm -rf " + str(sys.argv[1]) + "/totalExecutionTime.json " + str(sys.argv[1]) + "/resultExecutionTime.json")
    
    DataGet.getOriginalProjectInformation()
    
    os.chdir("../..")
    
    #If it's not the first used of the script on this initial project, we remove the previous output data
    newProjectName = projectName[13:len(projectName)] + "_clone"
    os.system("sudo rm -rf outputProject/" + newProjectName + " totalExecutionTime.json dataPlot.json")

    #We recreate or create the directory where the output data of the clone will be store
    os.mkdir("outputProject/" + newProjectName)   
    os.chdir("outputProject/" + newProjectName)

    newProjectName = projectName[13:len(projectName)]

    #We add all the dependencies in a file to have the N iteration will do
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
            
            #Make a copy of the initial project with a new name like : initialProjectName_NumberOfTheDependence_NumberOfTheChangeOfDependence
            shutil.copytree("../../" + projectName, newVersionDependence)
            
            os.chdir(newVersionDependence)
            
            #Now we apply the script for change the version of the current dependency
            VersionModifier.modifyVersionDependency("pom.xml")
            
            #Here we put in a file if the current dependency have a range version which is not null
            rangeFile = open("../range.txt", "r")
            range = rangeFile.readlines()
            rangeFile.close()
            
            #If this range is null so we stop to iterate in this dependency and pass to the next
            if range[0] == "False":
                os.chdir("..")
                newVersionDependence = newProjectName
                break
            
            #Now that we have change the version we launch a build and a test
            os.system("sudo mvn --log-file ./buildOutput.txt compile")
            os.system("sudo mvn test > ./testOutput.txt")
            
            #Here we launch the script where we get all the informations about the build and the execution time of the tests suite
            DataGet.getExecutionTimeForEachProject(newVersionDependence)
            
            os.chdir("..")
            
            newVersionDependence = projectName[13:len(projectName)]
            
            i += 1
            
        count += 1
        
        newProjectName = projectName[13:len(projectName)]
        
        #Here we remove the current dependency name to the file and we pass to the next dependency
        DependenciesName.delNameToFile()

    if os.path.isfile("range.txt"):
        os.system("sudo rm range.txt dependenciesName.txt")
    else:
        os.system("sudo rm dependenciesName.txt")
        print("Aucune dépendence à modifier dans le projet.")
     
     
#Here we have two ways to launch the script the first is to launch it with only one project and the second is for launch it with a directory where many project are store   
if str(sys.argv[1]) == "inputProject/":
    for dir in os.listdir("inputProject/"):
        launch("inputProject/" + dir)
        os.chdir("../..")
else:
    launch(str(sys.argv[1]))