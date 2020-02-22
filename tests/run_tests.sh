#!/bin/bash


echo "=========RUNNING ALL POSITIVE TESTS========="
cntr=0
for f in ./tests/positive/*.rms; do
	echo "===================TEST $cntr==================="
	./src/go.py $f
	if [ $? -eq 1 ]; then
		exit $?
	fi
	cntr=$((cntr+1))
done

echo "=========RUNNING ALL NEGATIVE TESTS========="
echo 
cntr=0
for f in ./tests/negative/*.rms; do
	echo "===================TEST $cntr==================="
	./src/go.py $f
	if [ $? -eq 1 ]; then
		exit $?
	fi
	cntr=$((cntr+1))
done




