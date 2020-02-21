#!/bin/bash


echo "=========RUNNING ALL POSITIVE TESTS========="
cntr=0
for f in ./tests/positive/*.rms; do
	echo "===================TEST $cntr==================="
	./src/go.py $f
	cntr=$((cntr+1))
done



