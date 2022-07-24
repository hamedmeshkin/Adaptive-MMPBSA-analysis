#!/bin/bash
i=8
cd $i/
pwd
vmd -dispdev text -e $(printf 'mmpbsa_%02d.tcl' $i) > vmd.log
