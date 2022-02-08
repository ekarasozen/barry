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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates


name = "taan_fjord"
s1 = UTCDateTime("2015-10-18 05:19:00") #  Taan Fjord
evlat=60.175
evlon=-141.187
vel = [i for i in np.arange(2.5,6.0,0.1)]
print("Velocities being tested (km/sec):")
print(vel)
endtime = 60*1.5
#net= "AK"
#chn = "BHZ"


st_stack_vel = Stream() #stacked streams for different velocities
stack_power = np.empty((0, 100))
stack_env_power = np.empty((0, 100))

nov = len(vel)
for v in range (nov):
#  inv = client.get_stations(network="AK", station="RKAV,SAMH,TGL", starttime=s1, endtime=s1+endtime)
   inv = client.get_stations(network = "AK", station="MESA,YAH,RKAV,CYK,BAGL,BARK,KULT,TABL,SAMH,PIN,GRNC,LOGN,BARK,ISLE,KULT,CTG,BCP,SSP,WAX,BARN,KIAG,TGL", starttime=s1, endtime=s1+endtime)
  # inv = client.get_stations(network = "AK", station="BAW,BAE,GLI,KNK,PWL", starttime=s1, endtime=s1+endtime)
   st = Stream() #initial stream
   st_corr = Stream() #stream to stack
   distance = np.empty((0, 100))
   traveltime = np.empty((0,100))
   print("Stations being called:")
   print(inv[0])
   net = inv[0]
   nos = len(net)
   for s in range(nos):
      tr = client.get_waveforms(network="AK", station=net[s].code, location="*", channel="BHZ", starttime=s1, endtime=s1+endtime, attach_response=True)
      #print(tr)
      st += tr
      stalat=net[s].latitude
      stalon=net[s].longitude
      #print(net[s],stalat,stalon)
      dist=client_distaz.distaz(stalat,stalon,evlat,evlon) #calculate the distance from the source to each of the stations
     #####TO CONTROL WHICH STATIONS TO INCLUDE BY DISTANCE
      if dist['distance'] >= 0.3:
      	 continue
      else: 
         dist=dist['distancemeters']/1000
      #print(dist)
      distance = np.append(distance, [dist])
      tt = np.divide(float(dist),float(vel[v]))
      traveltime = np.append(traveltime, [tt])
      #print(tt)
      s2=s1+tt
      trs = client.get_waveforms("AK", net[s].code, "*", "BHZ", s2, s2+endtime, attach_response=True)
      #print(trs)
      st_corr += trs
   
   #remove instrument response (and possibly integrate to displacement?)
   st.sort(keys=['starttime'])
   st.detrend("linear")
   st.detrend("demean")
   st.taper(max_percentage=0.05, type='cosine')
   st.filter('bandpass', freqmin=0.01, freqmax=0.05)
   st.remove_response(output='DISP')
   #print(st)
   st_corr.detrend("linear")
   st_corr.detrend("demean")
   st_corr.taper(max_percentage=0.05, type='cosine')
   st_corr.filter('bandpass', freqmin=0.01, freqmax=0.05)
   st_corr.remove_response(output='DISP')
   st_corr.sort(keys=['starttime']) #not sure if this is needed?
   print("These stations passed the distance criteria:")
   print(st_corr)
   
   #STACKING
   st_corr.normalize()
   st_stack = st_corr.stack()
   maxpower = np.max(np.abs(st_stack[0].data))
   stack_power = np.append(stack_power, [maxpower])
   st_stack_env = obspy.signal.filter.envelope(st_stack[0].data)
   maxenvpower = np.max(np.abs(st_stack_env))
   stack_env_power = np.append(stack_env_power, [maxenvpower])
   st_stack_vel += st_stack #stacked streams for different velocities

   #FIGURES
   #stream plot
   #fig1 = plt.figure(figsize=(8,16))
   #
   #for i in range(nos):
   #    ax1 = fig1.add_subplot(nos, 1,i+1)
   #    tr = st[i]
   #    ax1.plot(tr.times("matplotlib"), tr.data, 'k', linewidth=0.2)
   #    text = (tr.stats.station + ' ' + tr.stats.channel)
   #    ax1.text(0.85, 0.90, text, transform=ax1.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
   #    ax1.xaxis_date()
   #    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
   #    ax1.set_ylim(ymin=-250, ymax=250)
   #fig1.autofmt_xdate()
   #plt.tight_layout()
   #plt.draw()
   #fig1.autofmt_xdate()
   #fig1.savefig(name + '_before_tt_correction.png')
   
   #fig2 = plt.figure(figsize=(8,16))
   #traveltime corrected stream plot
   #for i in range(nos):
   #    ax2 = fig2.add_subplot(nos, 1,i+1)
   #    tr = st_corr[i]
   #    ax2.plot(tr.times("matplotlib"), tr.data, 'k', linewidth=0.2)
   #    text = (tr.stats.station + ' ' + tr.stats.channel)
   #    ax2.text(0.85, 0.90, text, transform=ax2.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
   #    ax2.xaxis_date()
   #    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
   #    ax2.set_ylim(ymin=-250, ymax=250)
   #fig2.autofmt_xdate()
   #plt.tight_layout()
   #plt.draw()
   #fig2.autofmt_xdate()
   #fig2.savefig(name + '_after_tt_correction_3.5kmsec.png')
   
   #stack streams for each velocity
   gs = gridspec.GridSpec(1, 1)
   gs.update(wspace=0.01, hspace=0.50) # set the spacing between axes. 
   fig3 = plt.figure(figsize=(8, 8))
   ax3 = fig3.add_subplot(gs[0])
   ax3.plot(st_stack[0].times(), st_stack[0].data, "k-", linewidth=0.8, label='stream')
   ax3.plot(st_stack[0].times(), st_stack_env, 'k:')
   text = (str(vel[v]) + 'km/sec')
   ax3.text(0.85, 0.90, text, transform=ax3.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
   ax3.set_ylabel('Displacement (m)')
   ax3.set_xlabel('Time (sec)')
   ax3.set_xlim(xmin=0, xmax=endtime)
   fig3.autofmt_xdate()
   fig3.savefig(name + '_stack_' + str(vel[v]) + '_kmsec_disp.png')
   st_stack.write(name + '_stack_' + str(vel[v]) + '_kmsec.mseed', format="MSEED")  
#print(st_stack_vel)
#print(stack_power)
#print(stack_env_power)

#plot all stacked waveforms onto one axes, and their envelopes: 
fig4 = plt.figure(figsize=(8, 8))
noss = len(st_stack_vel)
for s in range(noss):
    tr = st_stack_vel[s]
    tr_env = obspy.signal.filter.envelope(tr.data)
    ax4 = fig4.add_subplot(2, 1, 1)
    ax4.plot(tr.times(), tr.data, linewidth=0.8, label=str(vel[s]) + ' km/sec')
    ax5 = fig4.add_subplot(2, 1, 2)
    ax5.plot(tr.times(), tr_env.data, linewidth=0.8)
#    ax1.set_xlim(timevector[0], timevector[-1]) 
#    ax1.set_ylim(ymin=-500, ymax=500)
    ax4.set_ylabel('Displacement (m)')
    ax5.set_ylabel('Envelope')
    ax4.legend()
#    ax5.legend()
    ax4.set_xlim(xmin=0, xmax=endtime)
    ax5.set_xlim(xmin=0, xmax=endtime)
ax4.set_title(name)
ax5.set_xlabel('Time (sec)')
fig4.autofmt_xdate()
fig4.savefig(name + 'stack_all_velocities.png')

#plot the max power from the stream and envelopes vs. velocity: 

fig5 = plt.figure(figsize=(8, 8))
ax6 =  fig5.add_subplot(2, 1, 1)
ax6.scatter(vel, stack_power, marker='x')
ax6.set_ylabel('Max displacement value from each stack')
ax6.set_xlabel('Velocity (km/sec)')
ax6.set_title(name)
#ax6.set_xlim(xmin=vel[0], xmax=vel[-1])
ax6.set_ylim(ymin=0.5, ymax=1.3)
ax7 = fig5.add_subplot(2, 1, 2)
ax7.scatter(vel, stack_env_power,  marker='x')
ax7.set_ylabel('Max env displacement value from each stack')
ax7.set_xlabel('Velocity (km/sec)')
ax7.set_ylim(ymin=0.5, ymax=1.3)
#ax7.set_xlim(xmin=vel[0], xmax=vel[-1])
fig5.savefig(name + 'stack_all_power.png')

#trim the stack, and make the same stream/envelope plot
t1 = st_stack_vel[0].stats.starttime
st_stack_vel = st_stack_vel.trim(t1, t1+100)
t2 = st_stack_vel[0].stats.endtime

#print(st_stack_vel)
#fig6 = plt.figure(figsize=(8, 8))
#noss = len(st_stack_vel)
#for s in range(noss):
#    tr = st_stack_vel[s]
#    tr_env = obspy.signal.filter.envelope(tr.data)
#    ax8 = fig6.add_subplot(2, 1, 1)
#    ax8.plot(tr.times(), tr.data, linewidth=0.8, label=str(vel[s]) + ' km/sec')
#    ax9 = fig6.add_subplot(2, 1, 2)
#    ax9.plot(tr.times(), tr_env.data, linewidth=0.8)
##    ax1.set_xlim(timevector[0], timevector[-1]) 
##    ax1.set_ylim(ymin=-500, ymax=500)
#    ax8.set_ylabel('Displacement (m)')
#    ax9.set_ylabel('Envelope')
#    ax8.legend()
##    ax9.legend()
#    #ax8.set_xlim(xmin=0, xmax=t2)
#    #ax9.set_xlim(xmin=0, xmax=t2)
##ax8.set_title(name)
#ax9.set_xlabel('Time (sec)')
#fig6.autofmt_xdate()
#fig6.savefig(name + '_trimmed_stack_all_velocities.png')
#