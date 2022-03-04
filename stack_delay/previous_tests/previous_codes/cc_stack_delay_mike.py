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
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
from matplotlib.transforms import blended_transform_factory

########################################
#INPUTS
name = "BA_2021_Aug9"
#name = "Taan_Fjord"
#s1 = UTCDateTime("2015-10-18 05:19:00") #  Taan Fjord
#s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
s1= UTCDateTime("2021-08-09 07:45:47") # 2021 August landslide seen at BAE 07:46:37
#evlat=60.175 #Taan Fjord
#evlon=-141.187 #Taan Fjord
#evlat=61.153 #BA October 5 2020
#evlon=-148.163 #BA October 5 2020

evlat=61.242 #BA August 9 2021
evlon=-147.94 #BA August 9 2021
vel = [i for i in np.arange(2.5,6.0,0.1)]
print("Velocities being tested (km/sec):")
print(vel)
distlim = 1.0
print("Distance limit for stations to be included (in degrees)")
print(distlim)
trimtime = 50
starttime = (60*2)
endtime = 60*5
ststackvel = Stream() #stacked streams for different velocities
stack_power = np.empty((0, 100))
stack_env_power = np.empty((0, 100))
nov = len(vel) #number of velocities to be tested 
########################################
inv = client.get_stations(network = "AK", station="*", channel="BHZ", starttime=s1, endtime=s1+endtime)
net = inv[0]
nos = len(net) #number of stations in the network

for v in range (nov):
    print(vel[v])
    stprev = Stream() #stream to stack
    st = Stream() #initial stream
    stcorr = Stream() #stream to stack
    distance = np.empty((0, 100))
    traveltime = np.empty((0,100))
    for s in range(nos):
      stalat=net[s].latitude
      stalon=net[s].longitude
      dist=client_distaz.distaz(stalat,stalon,evlat,evlon) 
      distdeg = dist['distance']
      distm = dist['distancemeters']
      tt = np.divide(float(distm)/1000,float(vel[v])) #calculate the traveltime
      if distdeg < distlim and distdeg > 0.01:
         try:
            stprev += client.get_waveforms(network="AK", station=net[s].code, location="*", channel="BHZ", starttime=s1-starttime, endtime=s1+endtime, attach_response=True) #call waveforms that fit the distance criteria, perhaps this step can be avoided in next runs. 
            st += client.get_waveforms(network="AK", station=net[s].code, location="*", channel="BHZ", starttime=s1+tt-starttime, endtime=s1+tt+endtime, attach_response=True) #call waveforms that fit the distance criteria, perhaps this step can be avoided in next runs. 
         except FDSNNoDataException: #not sure why there is an error like this but this is the way around:
            print('No data available for request. Skipping this station: ' + net[s].code)
            continue
         distance = np.append(distance, [distm]) #distances are saved in meters
         traveltime = np.append(traveltime, [tt]) #save to traveltime table
      else: #ignore the stations at further distances > distlim
      	 continue
#    stprev.sort(keys=['starttime']) #not sure if this is needed?
    noss = len(st) #number of stations in the stream
    for t in range(noss): 
       stprev[t].stats.distance = distance[t]
       st[t].stats.distance = distance[t]
    print(stprev)
    stprev.detrend("linear")
    stprev.detrend("demean")
    stprev.taper(max_percentage=0.05, type='cosine')
    stprev.filter('bandpass', freqmin=0.01, freqmax=0.05)
    st.sort(keys=['starttime']) #not sure if this is needed?
    print(st)
    st.detrend("linear")
    st.detrend("demean")
    st.taper(max_percentage=0.05, type='cosine')
    st.filter('bandpass', freqmin=0.01, freqmax=0.05)
    st.remove_response(output='DISP')
    text = (str(vel[v]) + 'km/sec')
    fig0 = plt.figure()
    stprev.plot(type="section",plot_dx=20e3, recordstart=trimtime, recordlength=(starttime+endtime-trimtime),
         time_down=True, linewidth=1.0, grid_linewidth=.25,
         show=False, fig=fig0)
    ax = fig0.axes[0]
    transform = blended_transform_factory(ax.transData, ax.transAxes)
    for trprev in stprev:
        ax.text(trprev.stats.distance / 1e3, 1.0, trprev.stats.station, rotation=270,
                va="bottom", ha="center", transform=transform, zorder=10)
   # ax.text(0.85, 0.15, text, transform=ax.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
    fig0.savefig(name + '_ttprev_rec_sctn_' + str(vel[v]) + '_kmsec_mike.png')
    fig1 = plt.figure()
    st.plot(type="section",plot_dx=20e3, recordstart=trimtime, recordlength=(starttime+endtime-trimtime),
      time_down=True, linewidth=.75, grid_linewidth=.25,
      show=False, fig=fig1)
    ax1 = fig1.axes[0]
    transform = blended_transform_factory(ax1.transData, ax1.transAxes)
    for tr in st:
       ax1.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,
           va="bottom", ha="center", transform=transform, zorder=10)
    ax1.text(0.85, 0.10, text, transform=ax1.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
    fig1.savefig(name + '_ttcorr_rec_sctn_' + str(vel[v]) + '_kmsec_mike.png')
    st.normalize() #normalizing all traces separately to their respective abs maximum
    ststack = st.stack(npts_tol=1) #stack traces
    maxpower = np.max(np.abs(ststack[0].data)) #max of the abs value of the stack
    stack_power = np.append(stack_power, [maxpower]) #put maxpowers into an array
    ststackenv = obspy.signal.filter.envelope(ststack[0].data) #calculate env of each stack 
    maxenvpower = np.max(np.abs(ststackenv)) #max of abs value of env 
    stack_env_power = np.append(stack_env_power, [maxenvpower]) #put maxenvpowers into an array
    ststackvel += ststack #save stacked streams for different velocities
    
   #stack streams for each velocity
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.01, hspace=0.50) # set the spacing between axes. 
    fig3 = plt.figure(figsize=(8, 8))
    ax3 = fig3.add_subplot(gs[0])
    ax3.plot(ststack[0].times(), ststack[0].data, "k-", linewidth=0.8, label='stream')
    ax3.plot(ststack[0].times(), ststackenv, 'k:')
    text = (str(vel[v]) + 'km/sec')
    ax3.text(0.85, 0.90, text, transform=ax3.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
    ax3.set_ylabel('Displacement (m)')
    ax3.set_xlabel('Time (sec)')
    ax3.set_xlim(xmin=0)
  # fig3.autofmt_xdate()
    fig3.savefig(name + '_stack_' + str(vel[v]) + '_kmsec_disp_mike.png')
    ststack.write(name + '_stack_' + str(vel[v]) + '_kmsec_mike.mseed', format="MSEED")  

########################################
#FIGURES
#print(ststackvel)
#plot all stacked waveforms onto one axes, and their envelopes: 
fig4 = plt.figure(figsize=(8, 8))
nosv = len(ststackvel) #number of stacks for different velocities
for s in range(nosv):
    tr = ststackvel[s]
    trenv = obspy.signal.filter.envelope(tr.data)
    ax4 = fig4.add_subplot(2, 1, 1)
    ax4.plot(tr.times(), tr.data, linewidth=0.8, label=str(vel[s]) + ' km/sec')
    ax5 = fig4.add_subplot(2, 1, 2)
    ax5.plot(tr.times(), trenv.data, linewidth=0.8)
#    ax1.set_xlim(timevector[0], timevector[-1]) 
#    ax1.set_ylim(ymin=-500, ymax=500)
    ax4.set_ylabel('Displacement (m)')
    ax5.set_ylabel('Envelope')
    ax4.legend()
    ax4.set_xlim(xmin=0)
    ax5.set_xlim(xmin=0)
ax4.set_title(name)
ax5.set_xlabel('Time (sec)')
fig4.autofmt_xdate()
fig4.savefig(name + '_stack_all_velocities_mike.png')

#plot the max power from the stream and envelopes vs. velocity: 

fig5 = plt.figure(figsize=(8, 8))
ax6 =  fig5.add_subplot(2, 1, 1)
ax6.scatter(vel, stack_power, marker='x')
ax6.set_ylabel('Max of the abs value from each stack')
ax6.set_xlabel('Displacement (m)')
ax6.set_title(name)
#ax6.set_xlim(xmin=vel[0], xmax=vel[-1])
ax6.set_ylim(ymin=0.0)
ax7 = fig5.add_subplot(2, 1, 2)
ax7.scatter(vel, stack_env_power,  marker='x')
ax7.set_ylabel('Max of the env from each stack')
ax7.set_xlabel('Displacement (m)')
ax7.set_ylim(ymin=0.0)
#ax7.set_xlim(xmin=vel[0], xmax=vel[-1])
fig5.savefig(name + '_stack_all_power_mike.png')
########################################