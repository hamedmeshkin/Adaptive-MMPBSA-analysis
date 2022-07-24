#!/bin/bash 
core=21
let bin=500/$core+1 
bin=50
step=0
Offset=2

echo "parmbox nobox"
echo "parmbox x 70.937 y 70.937 z 120.25 alpha 90 beta 90 gamma 120"
echo "parminfo"
echo "box x 70.937 y 70.937 z 120.25 alpha 90 beta 90 gamma 120"
echo "strip :WAT"
echo "strip :Na+"
echo "strip :Cl-"
echo "autoimage :84,894,492,390,288,186@CA"
echo "align :1-612@CA"

for n in $(seq 1 $core)
do 
	let j=$n-1
	let new1=$bin*$j+$step
	let new2=$bin*$n-1+$step
 	echo "trajout  traj/complex.$n.dcd start $new1 stop $new2 offset $Offset"
done

echo "go"
echo "parmwrite out hexmolsol.prmtop"
