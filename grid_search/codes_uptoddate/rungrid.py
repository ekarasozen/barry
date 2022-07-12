import os
import grid_search_functions as grid
import plotgrid as plot

#grid.makestalist("AK","BAE,BAW,DIV,EYAK,FID,GHO,GLI,HIN,KLU,KNK,M23K,P23K,PS12,PWL,RC01,SAW,SCM,SLK,SSN,SWD,VMT,WAT6","BHZ","*","2020-10-05 05:01:50") 
#grid.creategrid(-150.0,-146.0,0.1,60,62,0.05,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2020-10-05 05:01:50",180)  
grid.locate("ttgridfile.npy","before_ts_wfs.mseed","lonlatgridfile.npy",5)
#plot.plotGrid("lonlatgridfile.npy","strengthfile.npy") #might move this into grid_functions
