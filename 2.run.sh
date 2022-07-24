#!/bin/bash
for i in $(seq 1 10)
do
cd test$i
#mkdir e.o
sbatch sim_mmpbsa.bbs 
pwd
cd ../
done
