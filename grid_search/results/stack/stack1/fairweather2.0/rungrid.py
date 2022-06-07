import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","BCP,BESE,JIS,PIN,PNL","BHZ","*","2016-09-05 04:39:00") 
#grid.creategrid(-140.0,-135.0,0.1,57,61,0.1,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2016-09-05 04:39:00",360)  
grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
#plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
#rec.plotRecordSection("before_stack_wfs.mseed","best_stack_wfs.mseed","stafile.csv","stacked_locfile.csv")
