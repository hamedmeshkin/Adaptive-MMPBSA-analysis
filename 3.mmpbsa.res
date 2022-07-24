#!/bin/bash
for i in $(seq 1 10)
do
	cd test$i
	tail */mmpbsa.*.log | grep "Total" | awk {'print  $3'}  
	cd ../
done

