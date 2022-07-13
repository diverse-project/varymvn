import xml.dom.minidom as DM
import sys, XMLParser


def addNameToFile():
    doc = DM.parse(str(sys.argv[2]))

    res = ""
    dependencies = doc.getElementsByTagName('dependency')
    for dependency in dependencies:
        res += XMLParser.getDependenciesDetails(dependency.getElementsByTagName('artifactId')) + "\n"
        
    with open("dependenciesName.txt", "w") as out_file:
        out_file.write(res)
        
def delNameToFile():
    with open('dependenciesName.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('dependenciesName.txt', 'w') as fout:
        fout.writelines(data[1:])
        

if sys.argv[1] == '0':
    addNameToFile()
else:
    delNameToFile()