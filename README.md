# varymvn
Executing Maven-based Java projects in multiple environments/libraries' versions

## How to execute the script

To execut the script you need a project where you will launch the script, this project must be in a directory named inputProject and you need to create a outputProject directory to store the result of the execution.
  
```bash
python3 varymvn.py inputProject/XXXXXXXX
```

If you want to launch it on many different project you can use it like that

```
python3 varymvn.py inputProject/
```

After that if you want to get the informations about a clone you must tap the following command

```
python3 AnalyseData.py outputProject/name_of_the_clone 0
python3 AnalyseData.py outputProject/name_of_the_clone 1
python3 AnalyseData.py outputProject/name_of_the_clone 2
```

If you only want to have all the informations in a CSV format just tap the first command, the second command make a CSV with the min, max and average execution time for each dependencies and the last command create a CSV for plot

If you want to have a graphic render 

```
python3 PlotInformation.py outputProject/name_of_the_clone
```
