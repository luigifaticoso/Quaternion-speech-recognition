#!/usr/bin/env python

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

(rate,sig) = wav.read("SA1.wav")
# mfcc_feat = mfcc(sig,rate)
# d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat,energy = logfbank(sig,rate)
d_fbank = delta(fbank_feat,40)

print(len(energy))
