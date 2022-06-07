import os
import grid_search_functions as grid
import plotgrid as plot
import plotrecordsec as rec

#grid.makestalist("AK","FID,GHO,GLI,KNK,M23K,PWL,RC01,SAW,SCM,VMT","BHZ","*","2020-10-05 05:01:00") 
#grid.creategrid(-150.0,-147.0,0.1,59,62,0.1,3.5,"stafile.csv")
#grid.prepwaveforms("stafile.csv","2020-10-05 05:01:00",360)  
#grid.locate("ttgridfile.npy","before_ts_wfs.mseed","lonlatgridfile.npy",3)                 
plot.plotGrid("lonlatgridfile.npy","strengthfile.npy") #might move this into grid_functions
