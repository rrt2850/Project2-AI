#!/bin/bash
#run using bash testFile.sh <java/python> <program name>
#not sure if this will help anyone but me


testPath="./testcases"
PROG="$1 $2"

FILES="$testPath/*/*.cnf"
for fP in $FILES; do
		 basename $fP
		#echo $PROG $fP
		timeout -s 9 60s $PROG $fP
#		$PROG $fP
done

#echo 

