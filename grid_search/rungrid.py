import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec
#grid.makestalist("AK","BAE,BAT,KNK,PWL,GLI,M23K,SAW,SCM,GHO,VMT,FID,RC01","BHZ","*","2021-08-09 07:45:47") 
#grid.creategrid(-149.0,-148.7,0.1,60,60.3,0.1,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2021-08-09 07:45:47",360)  
grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
#plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
#rec.plotRecordSection("readytostack.mseed","stacked_wfs_02.mseed","stafile.csv","stacked_locfile.npy")
