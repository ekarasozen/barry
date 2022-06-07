import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","BRLK,BRSE,CAPN,CNP,FIRE,HOM,RC01,SLK,SWD","BHZ","*","2015-03-07 19:17:00") 
#grid.creategrid(-139.0,-134.0,0.1,56,60,0.1,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2015-03-07 19:17:00",360)  
#grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
#plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
rec.plotRecordSection("before_stack_wfs.mseed","best_stack_wfs.mseed","stafile.csv","stacked_locfile.csv")