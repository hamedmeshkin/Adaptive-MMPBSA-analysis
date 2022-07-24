
set ii 11
set fst 0
set lst 100
set step 200

package require cafe 1.0

mmpbsa -top_type  parm7 \
       -top       ../../../common/hexmol.prmtop \
       -trj       ../traj/complex.$ii.dcd \
       -out       mmpbsa.$ii.log \
       -com       "all" \
       -rec       "protein" \
       -lig       "resname LIG" \
       -first     0 \
       -last      -1 \
       -stride    1 \
       -mm_exe    namd2 \
       -mm        1 \
       -pb        2 \
       -pb_exe    apbs \
       -pb_rad    parm7 \
       -pb_bcfl   mdh \
       -pb_chgm   spl4 \
       -pb_srfm   spl4 \
       -sa        1 \
       -sa_rad    parm7 \
       -sa_gamma  0.00542 \
       -sa_beta   0.92

exit
  
  
  
  
