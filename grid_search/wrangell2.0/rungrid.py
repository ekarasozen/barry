import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","BAGL,BAL,BARK,BARN,BERG,BGLC,CRQ,CTG,DOT,EYAK,GLB,GOAT,GRIN,GRNC,HMT,ISLE,KHIT,KIAG,KULT,MCAR,MESA,NICH,PAX,PTPK,RAG,RIDG,SCM,SGA,SSP,SUCK,TABL,TGL,VRDI,WAX,YAH","BHZ","*","2013-07-25 10:12:00") 
#grid.creategrid(-145.0,-140.5,0.1,60,64,0.1,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2013-07-25 10:12:00",360)  
#grid.shiftstack("ttgridfile.npy","before_stack_wfs.mseed","lonlatgridfile.npy")                 
#plot.plotGrid("lonlatgridfile.npy","stacked_strengthfile.npy")
rec.plotRecordSection("before_stack_wfs.mseed","best_stack_wfs.mseed","stafile.csv","stacked_locfile.csv")
