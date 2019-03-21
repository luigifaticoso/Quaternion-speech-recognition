import os

####################################
# pre process parameters

# Mel-Frequency Cepstrum Coefficients, default 12
numcep=40 #40
# the number of filters in the filterbank, default 26.
numfilt = 40 #40

# the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
winlen = 0.025
# the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
winstep = 0.01
# use  first or first+second order derivation
grad = 2

# TODO: for loop che loppa su tutti i file wav
filename = "SA1_1.WAV" # qui ci va il file da processare 
f = Sndfile(filename, 'r')

frames = f.nframes
samplerate = f.samplerate
data = f.read_frames(frames)
data = np.asarray(data)
print data.shape
#calc mfcc
feat_raw,energy = sf.fbank(data, samplerate,winlen,winstep, nfilt=numfilt)
feat = np.log(feat_raw)
feat = sf.dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
feat = sf.lifter(feat,L=22)
feat = np.asarray(feat)

#calc log energy
log_energy = np.log(energy) #np.log( np.sum(feat_raw**2, axis=1) )
log_energy = log_energy.reshape([log_energy.shape[0],1])

mat = ( feat - np.mean(feat, axis=0) ) / (0.5 * np.std(feat, axis=0))
mat = np.concatenate((mat, log_energy), axis=1)

#calc first order derivatives
if grad >= 1:
    gradf = np.gradient(mat)[0]
    mat = np.concatenate((mat, gradf), axis=1)

#calc second order derivatives
if grad == 2:
    grad2f = np.gradient(gradf)[0]
    mat = np.concatenate((mat, grad2f), axis=1)

# print mat, frames, samplerate

# print grad2f[0]
# print gradf[0]
# print mat[0][41:]
# print mat.shape

# creazione dei quaternioni appesi alla lista final_quat
final_quat = list()
for row in range(41):
  for col in range(41):
    quaternion = [0,mat[row][col],mat[row+41][col+41],mat[row+82][col+82]]
    final_quat.append(quaternion)
   
print final_quat


