import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","CTG,BAL,WAX,TGL,CRQ,KAI,RAG,BMR,BESE","BHZ","*","2012-05-21 14:23:00") 
#grid.creategrid(-142.0,-137.0,0.1,58,62,0.1,4.1,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2012-05-21 14:23:00",360)  
#grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
#plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
rec.plotRecordSection("before_stack_wfs.mseed","best_stack_wfs.mseed","stafile.csv","stacked_locfile.csv")

