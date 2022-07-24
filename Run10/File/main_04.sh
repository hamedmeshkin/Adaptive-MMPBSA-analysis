#!/bin/bash
i=4
cd $i/
pwd
vmd -dispdev text -e $(printf 'mmpbsa_%02d.tcl' $i) > vmd.log
