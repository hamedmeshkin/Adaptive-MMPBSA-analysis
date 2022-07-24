#!/bin/bash
for j in $(seq 1 10)
do 
for i in $(seq 1 21)  
do
  mkdir -p Run$j/$i
  cp mmpbsa.tcl $(printf 'mmpbsa_%02d.tcl' $i)
  sed -i "s/set ii 1/set ii $i/g" $(printf 'mmpbsa_%02d.tcl' $i)
  sed -i "s/mmpbsa.log/mmpbsa.$ii.log/g" $(printf 'mmpbsa_%02d.tcl' $i)
  mv $(printf 'mmpbsa_%02d.tcl' $i) Run$j/$i
done
done 
