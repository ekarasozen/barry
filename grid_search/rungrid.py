import os
import createttgrid as grid
import makestalist as sta
import prepwaveforms as wfs
import shiftstack as stack
#grid.createttGrid(-149.0,-148.7,0.1,60,60.3,0.1,3.5,"stafile.csv")
#sta.makestalistIris("AK","BAE,BAT,KNK,PWL,GLI,M23K,SAW,SCM,GHO,VMT,FID,RC01","BHZ","*","2021-08-09 07:45:47") 
#wfs.prepwaveformsIris("stafile.csv","2019-08-09 07:45:47",360)  
stack.shiftStack("ttgridfile.npy","readytostack.mseed")                 