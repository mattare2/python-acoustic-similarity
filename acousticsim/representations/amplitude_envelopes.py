from numpy import pi,exp,log,abs,sum,sqrt,array, hanning, arange, zeros,cos,ceil,mean

from scipy.signal import filtfilt,butter,hilbert,decimate, resample

from acousticsim.representations.base import Representation
from acousticsim.representations.helper import preproc,make_erb_cfs,nextpow2,fftfilt


def window_envelopes(env,sr, win_len, time_step):
    nperseg = int(win_len*sr)
    nperstep = int(time_step*sr)
    window = hanning(nperseg+2)[1:nperseg+1]


    indices = arange(int(nperseg/2), x.shape[0] - int(nperseg/2) + 1, nperstep)
    num_samps, num_bands = env.shape
    num_frames = len(indices)
    rep = zeros((num_frames,num_bands))
    for k in range(num_frames):
        for b in range(num_bands):
            rep[k,b] = sum(env[indices[i]-int(nperseg/2):indices[i]+int(nperseg/2),b])
    return rep

class Envelopes(Representation):
    def __init__(self,filepath,freq_lims,num_bands, attributes = None):
        Representation.__init__(self, filepath,freq_lims, attributes)

        self._num_bands = num_bands

        self.process()


    def process(self, mode = 'downsample', debug = False):
        """Generate amplitude envelopes from a full path to a .wav, following
        Lewandowski (2012).

        Parameters
        ----------
        filename : str
            Full path to .wav file to process.
        freq_lims : tuple
            Minimum and maximum frequencies in Hertz to use.
        num_bands : int
            Number of frequency bands to use.
        win_len : float, optional
            Window length in seconds for using windows. By default, the
            envelopes are resampled to 120 Hz instead of windowed.
        time_step : float
            Time step in seconds for windowing. By default, the
            envelopes are resampled to 120 Hz instead of windowed.

        Returns
        -------
        2D array
            Amplitude envelopes over time.  If using windowing, the first
            dimension is the time in frames, but by default the first
            dimension is time in samples with a 120 Hz sampling rate.
            The second dimension is the amplitude envelope bands.

        """
        self._sr, proc = preproc(self._filepath,alpha=0.97)

        proc = proc / 32768 #hack!! for 16-bit pcm
        proc = proc/sqrt(mean(proc**2))*0.03;
        bandLo = [ self._freq_lims[0]*exp(log(
                                    self._freq_lims[1]/self._freq_lims[0]
                                    )/self._num_bands)**x
                                    for x in range(self._num_bands)]
        bandHi = [ self._freq_lims[0]*exp(log(
                                    self._freq_lims[1]/self._freq_lims[0]
                                    )/self._num_bands)**(x+1)
                                    for x in range(self._num_bands)]

        envs = []
        for i in range(self._num_bands):
            b, a = butter(2,(bandLo[i]/(self._sr/2),bandHi[i]/(self._sr/2)), btype = 'bandpass')
            env = filtfilt(b,a,proc)
            env = abs(hilbert(env))
            if mode == 'downsample':
                #env = resample(env,int(ceil(len(env)/int(ceil(self._sr/120)))))
                print(int(ceil(self._sr/120)))
                env = decimate(env,int(ceil(self._sr/120)))
            envs.append(env)
        envs = array(envs).T
        if mode == 'downsample':
            self._sr = 120
        self._rep = dict()
        for i in range(envs.shape[0]):
            self._rep[i/self._sr] = envs[i,:]
        #Don't know if this is the best way to do it
        if debug:
            return proc
