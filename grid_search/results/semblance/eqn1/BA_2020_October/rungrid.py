import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","BAE,BAW,FID,GHO,GLI,KNK,M23K,PWL,RC01,SAW,SCM,VMT","BHZ","*","2020-10-17 21:17:00") 
#grid.creategrid(-150.0,-147.0,0.1,59,62,0.1,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2020-10-17 21:17:00",360)  
#grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
#rec.plotRecordSection("before_stack_wfs.mseed","best_stack_wfs.mseed","stafile.csv","stacked_locfile.csv")
