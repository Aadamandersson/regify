#!/bin/bash

positive_dir="$(find ./ -d -name positive)"
negative_dir="$(find ./ -d -name negative)"
exe="./testsuite/tests/go.py"
echo "=========RUNNING ALL POSITIVE TESTS========="
cntr=0
for f in $positive_dir/*.re; do
	echo "===================TEST $cntr==================="
	./$exe $f
	if [ $? -eq 1 ]; then
		exit $?
	fi
	cntr=$((cntr+1))
done

echo "=========RUNNING ALL NEGATIVE TESTS========="
echo 
cntr=0
for f in $negative_dir/*.re; do
	echo "===================TEST $cntr==================="
	./$exe $f
	cntr=$((cntr+1))
done




