#!/bin/bash
PROJECT_NAME="$1"
NEW_PROJECT=$PROJECT_NAME

NEW_PROJECT+="_clone"
sudo rm -rf $NEW_PROJECT totalExecutionTime.json dataPlot.json

mkdir $NEW_PROJECT
cd $NEW_PROJECT

NEW_PROJECT=$PROJECT_NAME

python3 ../DependenciesName.py 0 ../$1/pom.xml

COUNT_ITERATION=$(wc -l < dependenciesName.txt)

for i in $(seq 1 1 $COUNT_ITERATION)
do
	NEW_PROJECT+="_"
	NEW_PROJECT+=$i

	for j in $(seq 1 1 $2)
	do
		NEW_VERSION_DEPENDENCE=$NEW_PROJECT
		NEW_VERSION_DEPENDENCE+="_"
		NEW_VERSION_DEPENDENCE+=$j
		cp -r ../$PROJECT_NAME $NEW_VERSION_DEPENDENCE

		cd $NEW_VERSION_DEPENDENCE
    	python3 ../../VersionModifier.py pom.xml

		for next in `cat ../range.txt`; do
    		if [ "$next" = "False" ]
			then
				echo "$next"
				cd ..
				NEW_VERSION_DEPENDENCE=$NEW_PROJECT
				break 2
			fi  
		done

		sudo mvn --log-file ./buildOutput.txt compile
		sudo mvn test > ./testOutput.txt

		python3 ../../DataGet.py target/surefire-reports/ $NEW_VERSION_DEPENDENCE
		cd ..

		NEW_VERSION_DEPENDENCE=$NEW_PROJECT
	done

	NEW_PROJECT=$PROJECT_NAME
	python3 ../DependenciesName.py 1
done

python3 ../AnalyseData.py ../$PROJECT_NAME
rm dependenciesName.txt range.txt
cd ..