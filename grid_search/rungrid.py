import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","BAE,BAT,KNK,PWL,GLI,M23K,SAW,SCM,GHO,VMT,FID,RC01","BHZ","*","2021-08-09 07:43:00") 
#grid.creategrid(-150.0,-147.0,0.1,59,62,0.1,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2021-08-09 07:43:00",300)  
#grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
#rec.plotRecordSection("before_stack_wfs.mseed","best_stack_wfs.mseed","stafile.csv","stacked_locfile.csv")
