import os
import shutil
import numpy as np
from scikits.audiolab import Sndfile
import python_speech_features as sf


# creazione dei quaternioni appesi alla lista final_quat
def make_quaternion(mat):
	#print(mat.shape)
	res = []
	for row in range(len(mat)):
		for j in range(41):
			quat = [0,mat[row][j],mat[row][j+41],mat[row][j+82]]
			res.append(quat)

	return res

if __name__ == '__main__':


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

	#number of elements for each set of quaternions
	N_SPLIT = 100

	dir_name = "Quaternion_" + str(N_SPLIT)
	tree = "/home/franci/Desktop/NN/Quaternion-speech-recognition/" + dir_name

	if os.path.isdir(tree):
		shutil.rmtree(tree)

	os.makedirs("Quaternion_" + str(N_SPLIT))
	path_to_quats = os.path.abspath("Quaternion_" + str(N_SPLIT))

	path_to_prep_files = os.path.abspath("preprocessed_files")
	dir = os.listdir( path_to_prep_files )

	for file in dir:				# loop su tutti i file *.WAV
		if file.split(".")[1] == "WAV":
			f = Sndfile(os.path.join(path_to_prep_files, file), 'r')

			frames = f.nframes
			samplerate = f.samplerate
			data = f.read_frames(frames)
			data = np.asarray(data)
			#print(data.shape)

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

			file_to_create = path_to_quats + "/" + file.split(".")[0] + "_processed.data"
			ff = open(file_to_create, "w")

			n = 1
			item = 0
			quats = make_quaternion(mat)
			quats_length = len(quats)
			while (item < quats_length):
				if item == N_SPLIT * n:
					ff.write("\n")
					n = n + 1
				quat = quats[item]
				for i in range(len(quat)):
					if i == 3:
						ff.write(str(quat[i]) + " ")
					else:
						ff.write(str(quat[i]) + ",")
				item = item + 1

			x = int(quats_length / N_SPLIT)
			for i in range(x):
				if i < x-1:
					ff.write("0,0,0,0 ")
				else:
					ff.write("0,0,0,0")



# print mat, frames, samplerate

# print grad2f[0]
# print gradf[0]
# print mat[0][41:]
# print mat.shape
