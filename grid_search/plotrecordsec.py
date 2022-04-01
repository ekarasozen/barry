from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
import obspy.signal
from obspy.clients.fdsn.header import FDSNNoDataException
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
# slightly hacked  ~/anaconda/envs/obspy/lib/python3.6/site-packages/obspy/imaging/waveform.py  to be able to integrate azimuth

#Function to create time-shifted distance and azimuth record sections and compare these to the stacked waveform.
#Inputs: wfs, sta_file, stacked_location, stacked_strength why do we need stacked_strength? 

#best mseed strength. not sure what is the best way to do this? ask mike perhaps
#figure out to turn azimuth over, and both. this is easy, just rename the axis title. could be done internally perhaps? 
#I need to do the starttime I think. I guess so. 
#need to figure out the error location thing. 
#plotgrid is working but not perfect. need to make sure grid locs are ok
#then pygmt




def plotRecordSection(wfs,mseed,stafile,stacked_locfile):
    st = read (wfs)
    stdist = read (mseed)      
    stazim = read (mseed)      
    nosb = len(st)
    nos = len(stdist)
    df = pd.read_csv(stafile,index_col=None,keep_default_na=False)
    nos = len(df) #number of stations
    station = df['station']
    stalat = df['latitude']
    stalon = df['longitude']
    cord = np.load(stacked_locfile)
    evlat = cord[0]
    evlon = cord[1]
    for s in range(nos):
        dist = client_distaz.distaz(stalat[s],stalon[s],evlat,evlon) 
        distdeg = dist['distance'] 
        distm = dist['distancemeters'] 
        azim = dist['azimuth']*1000 #this is the hacked section to plot azimuth as distance in record section
        st[s].stats.distance = distm #distances are saved in meters 
        stdist[s].stats.distance = distm #distances are saved in meters 
        stazim[s].stats.distance = azim #if you want azimuth to be plotted. 
    st.sort(keys=['distance'])
    stdist[:-1].sort(keys=['distance'])
    stazim[:-1].sort(keys=['distance'])
    fig = plt.figure(figsize=(4, 8))
    gs1 = gridspec.GridSpec(3, 1)
    gs1.update(wspace=0.01, hspace=0.5) # set the spacing between axes. 
    ###PLOT BEFORE DISTANCE
    ax0 = fig.add_subplot(gs1[0])
    st.plot(type="section", time_down=True, linewidth=.75, grid_linewidth=.25, orientation='vertical',show=False, fig=fig)
    transform = blended_transform_factory(ax0.transData, ax0.transAxes)
    for tr in st:
       ax0.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,va="bottom", ha="center", transform=transform, zorder=10)
    ax0.set_xlabel('Distance (km)') 
    ax0.set_title('BEFORE')
    ###PLOT AFTER DISTANCE   
    ax1 = fig.add_subplot(gs1[1])
    stdist[:-1].plot(type="section",time_down=True, linewidth=.75, grid_linewidth=.25, orientation='vertical',show=False, fig=fig)
    transform = blended_transform_factory(ax1.transData, ax1.transAxes)
    for tr in stdist[:-1]:
       ax1.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,va="bottom", ha="center", transform=transform, zorder=10)
    ax1.set_xlabel('Distance (km)') 
    ax1.set_title('AFTER')
   ###PLOT AFTER AZIMUTH   
    ax2 = fig.add_subplot(gs1[2])
    stazim[:-1].plot(type="section",time_down=True, linewidth=.75, grid_linewidth=.25, orientation='vertical',show=False, fig=fig)
    transform = blended_transform_factory(ax2.transData, ax2.transAxes)
    for tr in stazim[:-1]:
       ax2.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,va="bottom", ha="center", transform=transform, zorder=10)    
    ax2.set_xlabel('Azimuth [°]')
    ###ax0.set_xlim(100, 550) 
    fig.savefig('denemerecord_all.png')