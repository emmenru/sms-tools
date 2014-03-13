import numpy as np
import matplotlib.pyplot as plt
import sys, os, time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../software/utilFunctions/'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../software/utilFunctions_C/'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../software/models/'))

import stftAnal
import sineModelAnal as SA
import sineTracking as ST
import waveIO as WIO

(fs, x) = WIO.wavread(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../sounds/speech-male.wav'))
start = 1.25
end = 1.79
x1 = x[start*fs:end*fs]
w = np.hamming(801)
N = 2048
H = 200
t = -70
minSineDur = 0
maxnSines = 150
freqDevOffset = 10
freqDevSlope = 0.001
mX, pX = stftAnal.stftAnal(x1, fs, w, N, H)
tfreq, tmag, tphase = SA.sineModelAnal(x1, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)

maxplotfreq = 800.0
maxplotbin = int(N*maxplotfreq/fs)
numFrames = int(mX[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)                             
binFreq = np.arange(maxplotbin+1)*float(fs)/N                         
plt.pcolormesh(frmTime, binFreq, np.transpose(mX[:,:maxplotbin+1]))
plt.autoscale(tight=True)
  
tracks = tfreq*np.less(tfreq, maxplotfreq)
tracks[tracks<=0] = np.nan
plt.plot(frmTime, tracks, 'x', color='k')
plt.autoscale(tight=True)
plt.title('peaks on spectrogram (speech-male.wav)')
plt.show()