#!/bin/bash
core=60
for m in $(seq 1 $core)
 do
#    cp bigdcd.tcl $(printf 'bigdcd_%02d.tcl' $m) 
   cp dencity.tcl $(printf 'dencity_%02d.tcl' $m) 
 done
wait

 let bin=100000/$core+1 ; # Find out the number of frame in the DCD file   50667 
 for n in $(seq 1 $core)
  do 
    let j=$n-1
    let new1=$bin*$j
    let new2=$bin*$n-1
    echo $new1  $new2 $n
    old1=$(awk  'NR==3{print $3}' dencity.tcl)
    old2=$(awk  'NR==4{print $3}' dencity.tcl)
    old=$(awk  'NR==2{print $3}' dencity.tcl)
    sed -i "s/set fst $old1/set fst $new1/g" $(printf 'dencity_%02d.tcl' $n) >> $(printf 'dencity_%02d.tcl' $n)
    sed -i "s/set lst $old2/set lst $new2/g" $(printf 'dencity_%02d.tcl' $n) >> $(printf 'dencity_%02d.tcl' $n)
    sed -i "s/set ii $old/set ii $n/g" $(printf 'dencity_%02d.tcl' $n) >> $(printf 'dencity_%02d.tcl' $n)
 done

 

for i in $(seq 0 21)  
do
  mkdir ../$i
  cp dencity.tcl $(printf 'dencity_%02d.tcl' $i)
  sed -i "s/set ii 1/set ii $i/g" $(printf 'dencity_%02d.tcl' $i)
  sed -i "s/mmpbsa.log/mmpbsa.$ii.log/g" $(printf 'dencity_%02d.tcl' $i)
  mv $(printf 'dencity_%02d.tcl' $i) ../$i
done  

    
 
for i in $(seq 0 21)  
do
  cp main.sh $(printf 'main_%02d.sh' $i)
  sed -i "s/i=0/i=$i/g" $(printf 'main_%02d.sh' $i)
  mv $(printf 'main_%02d.sh' $i) ../File
done 
