from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.signal.cross_correlation import correlation_detector

# LOAD WAVEFORM DATA. DO A LITTLE PRE-PROCESSING
tday = UTCDateTime("2021-08-09 07:45") #landslide 1
ls1 = UTCDateTime("2021-10-17 21:19") #landslide 2

event_name = "master_event"
print('grabbing waveforms for ' + tday.strftime("%Y%m%d"))
template = client.get_waveforms("AK", "KNK", "*", "BHZ", tday, tday+360, attach_response=True)
template.filter('bandpass', freqmin=0.01, freqmax=0.05)
template.plot()


pick = UTCDateTime('2021-08-09T07:45:40.00')
template.trim(pick, pick + 150)

stream = client.get_waveforms("AK", "KNK", "*", "BHZ", ls1, ls1+360, attach_response=True)
stream.filter('bandpass', freqmin=0.01, freqmax=0.05)
height = 0.3  # similarity threshold
distance = 10  # distance between detections in seconds
detections, sims = correlation_detector(stream, template, height, distance, plot=stream)

print(detections)