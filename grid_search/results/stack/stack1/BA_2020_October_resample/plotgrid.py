from obspy.clients.fdsn import Client
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy import UTCDateTime
from obspy.clients.fdsn.header import FDSNNoDataException
from obspy import read
import numpy as np
from numpy import loadtxt
import pandas as pd
from obspy import Stream
from obspy import Trace
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter
import datetime
import matplotlib.dates as mdates

def plotGrid(lonlatgridfile,stacked_strengthfile):
    fig, (ax1) = plt.subplots(1,1)
    lonlatgrid = np.load(lonlatgridfile)
    stacked_strength = np.load(stacked_strengthfile)
    yy= lonlatgrid[0]
    xx= lonlatgrid[1]
    #plt.plot(xx, yy, marker='.', color='k', linestyle='none')
    #plt.show()
    maxamp = abs(stacked_strength).max()/2         # these two lines just adjust the color scale
    print(abs(stacked_strength).max())
    minamp = 0
 #  #t, f = np.meshgrid(st[0].times("matplotlib"), freqs)
#    im1 = ax1.pcolormesh(xx,yy, np.transpose(stacked_strength),shading='nearest')
    im1 = ax1.pcolormesh(xx,yy, stacked_strength,shading='nearest')
    ax111 = fig.add_axes([0.92, 0.11, 0.01, 0.77])
    fig.colorbar(im1, cax=ax111)    
    #ax1.set_ylabel('freq. (Hz)')
    #ax1.set_xlim(timevector[0], timevector[-1])
    #ax1.set_ylim(freqs[-1], freqs[0])
    #ax1.xaxis.set_major_formatter(date_format)
    #ax1.xaxis_date()
    #ax1.axes.xaxis.set_ticklabels([])
    #ax2.set_xlabel("Time [UTC]" )
    #ax1.text(0.01, 0.88, text, transform=ax2.transAxes, fontsize=10, fontweight='bold', color='white')
    fig.savefig('stacked_strength_map', bbox_inches='tight')

    