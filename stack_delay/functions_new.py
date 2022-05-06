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

#########
########Code to get waveforms from IRIS
########

def getEventsIRIS(network,station,location,channel,starttime,endtime):
    st = client.get_waveforms(network=network, station=station, location=location, channel=channel, starttime=starttime, endtime=endtime, attach_response=True)
    return st
    
def getStationsIris(network,station,channel,starttime,endtime):
    inv = client.get_stations(network=network,station=station,channel=channel,starttime=starttime,endtime=endtime)
    return inv


def plotRecordSection(st,distance_array,name,vel):
    nos = len(st)
    print(nos)
    for s in range(nos): 
       st[s].stats.distance = distance_array[s]
    st.sort(keys=['distance'])
    fig0 = plt.figure()
    st.plot(type="section", 
      time_down=True, linewidth=.75, grid_linewidth=.25, orientation='vertical',
      show=False, fig=fig0)
    ax0 = fig0.axes[0]
    transform = blended_transform_factory(ax0.transData, ax0.transAxes)
    for tr in st:
       ax0.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,
           va="bottom", ha="center", transform=transform, zorder=10)
    plot_name = "after_ttcorr_"
    ###ax0.set_xlim(100, 550) 
   # text = (str(vel) + 'km/sec')
  # ax0.text(0.85, 0.10, text, transform=ax0.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')        
    fig0.savefig(name + plot_name + str(vel) + '.png')    
    

#distance = np.empty((0, 100))

def plotRecordSectionMseed(mseed,starttime,endtime,evlat,evlon):
    st = read (mseed)                 
    s1 = UTCDateTime(startime)  
    for tr in st: 
        inv = func.getStationsIris("AK",tr.stats.station,"BHZ",s1, s1+endtime) 
        net = inv[0] 
        sta = net[0] 
        dist = client_distaz.distaz(sta.latitude,sta.longitude,evlat,evlon) 
        distdeg = dist['distance'] 
        distm = dist['distancemeters'] 
       # distance = np.append(distance, [distm]) #distances are saved in meters 
        tr.stats.distance = distm 
    st.sort(keys=['distance'])
    fig0 = plt.figure()
    st.plot(type="section",plot_dx=20e3, 
      time_down=True, linewidth=.75, grid_linewidth=.25,
      show=False, fig=fig0)
    ax0 = fig0.axes[0]
    transform = blended_transform_factory(ax0.transData, ax0.transAxes)
    for tr in st:
       ax0.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,
           va="bottom", ha="center", transform=transform, zorder=10)
    text = (str(vel) + 'km/sec')
    ax0.text(0.85, 0.10, text, transform=ax0.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')        
    fig0.savefig(plot_name + '.png')   

def stackPhaseWeighted(data):
    from scipy.signal import hilbert
    try:
        from scipy.fftpack import next_fast_len
    except ImportError:  # scipy < 0.18
        next_fast_len = next_pow_2
    npts = np.shape(data)[1]
    nfft = next_fast_len(npts)
    anal_sig = hilbert(data, N=nfft)[:, :npts]
    norm_anal_sig = anal_sig / np.abs(anal_sig)
    phase_stack = np.abs(np.mean(norm_anal_sig, axis=0)) ** stack_type[1]
    stack = np.mean(data, axis=0) * phase_stack
    return stack

