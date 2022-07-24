#!/bin/bash
i=0
cd $i/
pwd
vmd -dispdev text -e $(printf 'dencity_%02d.tcl' $i) > vmd.log
