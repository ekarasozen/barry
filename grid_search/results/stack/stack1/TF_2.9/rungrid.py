import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","RKAV,SAMH,TABL,YAH,MESA,PIN,BAGL,GRNC,LOGN,CYK,BARK,ISLE,KULT,CTG,BCP,SSP,WAX,BARN,KIAG,TGL","BHZ","*","2015-10-18 05:16:00") 
#grid.creategrid(-143.0,-139.0,0.1,59,63,0.1,2.9,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2015-10-18 05:16:00",360)  
#grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
#rec.plotRecordSection("before_stack_wfs.mseed","best_stack_wfs.mseed","stafile.csv","stacked_locfile.csv")
