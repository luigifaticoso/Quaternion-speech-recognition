#!/usr/bin/env python

# from python_speech_features import mfcc
# from python_speech_features import delta
# from python_speech_features import logfbank
# from python_speech_features import get_filterbanks
# import scipy.io.wavfile as wav

# (rate,sig) = wav.read("SA1.wav")
# mfcc_feat = mfcc(sig,rate)
# d_mfcc_feat = delta(mfcc_feat, 2)
# filterbanks = get_filterbanks(sig,rate)
# fbank_feat = logfbank(sig,rate)
# delta_feat = delta(fbank_feat,2)
# delta_delta_feat = delta(delta_feat,2)

# # print(fbank_feat[1:3])
# # print(delta_feat[1:3])
# # print(delta_delta_feat[1:3])
# print(filterbanks)


import numpy as np
from scikits.audiolab import Sndfile
import python_speech_features as sf


def get_features(filename, numcep, numfilt, winlen, winstep, grad):

    f = Sndfile(filename, 'r')

    frames = f.nframes
    samplerate = f.samplerate
    data = f.read_frames(frames)
    data = np.asarray(data)
    print("DATA")
    print(data)
    print(data.shape)

    #calc mfcc
    feat_raw,energy = sf.fbank(data, samplerate,winlen,winstep, nfilt=numfilt)
    print("FEAT_RAW")
    print(feat_raw)
    print(feat_raw.shape)
    print("ENERGY")
    print(energy)
    print(energy.shape)
    feat = np.log(feat_raw)
    feat = sf.dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
    feat = sf.lifter(feat,L=22)
    feat = np.asarray(feat)
    print("FEAT after log and dct")
    print(feat)
    print(feat.shape)

    #calc log energy
    log_energy = np.log(energy) #np.log( np.sum(feat_raw**2, axis=1) )
    log_energy = log_energy.reshape([log_energy.shape[0],1])
    print("LOG_ENERGY")
    print(log_energy)
    print(log_energy.shape)

    mat = ( feat - np.mean(feat, axis=0) ) / (0.5 * np.std(feat, axis=0))
    mat = np.concatenate((mat, log_energy), axis=1)
    print("MAT before gradients")
    print(mat)
    print(mat.shape)

    #calc first order derivatives
    if grad >= 1:
        gradf = np.gradient(mat)[0]
	print("GRADF")
    	print(gradf)
    	print(gradf.shape)
        mat = np.concatenate((mat, gradf), axis=1)
	print("MAT with 1st derivate")
   	print(mat)
    	print(mat.shape)

    #calc second order derivatives
    if grad == 2:
        grad2f = np.gradient(gradf)[0]
	print("GRAD2F")
    	print(grad2f)
    	print(grad2f.shape)
        mat = np.concatenate((mat, grad2f), axis=1)
	print("MAT with 2nd derivate")
    	print(mat)
    	print(mat.shape)


    return mat, frames, samplerate


####################################

#Raw Vectors in form of Quaternion
def print_matrix_to_quaterniorn(matt):
  final_quat = list()
  for row in range(41):
    for col in range(41):
      quaternion = [0,matt[row][col],matt[row+41][col+41],matt[row+82][col+82]]
      final_quat.append(quaternion)
  return final_quat
####################################

# pre process parameters

# Mel-Frequency Cepstrum Coefficients, default 12
numcep=40 #40
# the number of filters in the filterbank, default 26.
numfilt =40 #40

# the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
winlen = 0.025
# the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
winstep = 0.01
# use  first or first+second order derivation
grad = 2

mat, frames1, samplerate1 = get_features("./drive/My Drive/COLAB Neural/SA1.WAV",numcep, numfilt, winlen, winstep, grad)

#Vettori riga di 'mat'
mat2 = print_matrix_to_quaterniorn(mat)
print(mat2)


#print(mat1)
#print(mat1.shape)
