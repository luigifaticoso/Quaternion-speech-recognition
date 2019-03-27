# import os
# import shutil
# import numpy as np
# from scikits.audiolab import Sndfile
# import python_speech_features as sf

# dict_list = {'DR1': "1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
#             'DR2': "0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
#             'DR3': "0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
#             'DR4': "0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
#             'DR5': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0", 
#             'DR6': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0", 
#             'DR7': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0", 
#             'DR8': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1" 
#             }
# dirlist = ['DR1', 'DR2', 'DR3', 'DR4', 'DR5', 'DR6', 'DR7', 'DR8']

# # creazione dei quaternioni appesi alla lista final_quat
# def make_quaternion(mat):
# 	#print(mat.shape)
# 	res = []
# 	for row in range(len(mat)):
# 		for j in range(41):
# 			quat = [0,mat[row][j],mat[row][j+41],mat[row][j+82]]
# 			res.append(quat)

# 	return res

# if __name__ == '__main__':
#     ####################################
# 	# pre process parameters

# 	# Mel-Frequency Cepstrum Coefficients, default 12
# 	numcep=40 #40
# 	# the number of filters in the filterbank, default 26.
# 	numfilt = 40 #40

# 	# the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
# 	winlen = 0.025
# 	# the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
# 	winstep = 0.01
# 	# use  first or first+second order derivation
# 	grad = 2

# 	#number of elements for each set of quaternions
# 	N_SPLIT = 400

# 	dir_name = "Quaternion_DICT_" + str(N_SPLIT)
# 	tree = "/home/franci/Desktop/NN/Quaternion-speech-recognition/" + dir_name

# 	if os.path.isdir(tree):
# 		shutil.rmtree(tree)

# 	os.makedirs("Quaternion_DICT_" + str(N_SPLIT))
# 	path_to_quats = os.path.abspath("Quaternion_" + str(N_SPLIT))

# 	path_to_prep_files = os.path.abspath("preprocessed_files_with_dict")
# 	dir = os.listdir(path_to_prep_files)
    
#     for path_dict in dir:
#         print(f'Analizzo la cartella {str(path_dict)}')
#         dir_dict = os.listdir(path_to_prep_files + '/' + str(path_dict))

#         for file in dir_dict:				# loop su tutti i file *.WAV
#             if file.split(".")[1] == "WAV":
#                 f = Sndfile(os.path.join(dir_dict, file), 'r')

#                 frames = f.nframes
#                 samplerate = f.samplerate
#                 data = f.read_frames(frames)
#                 data = np.asarray(data)
#                 #print(data.shape)

#                 #calc mfcc
#                 feat_raw,energy = sf.fbank(data, samplerate,winlen,winstep, nfilt=numfilt)
#                 feat = np.log(feat_raw)
#                 feat = sf.dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
#                 feat = sf.lifter(feat,L=22)
#                 feat = np.asarray(feat)

#                 #calc log energy
#                 log_energy = np.log(energy) #np.log( np.sum(feat_raw**2, axis=1) )
#                 log_energy = log_energy.reshape([log_energy.shape[0],1])

#                 mat = ( feat - np.mean(feat, axis=0) ) / (0.5 * np.std(feat, axis=0))
#                 mat = np.concatenate((mat, log_energy), axis=1)

#                 #calc first order derivatives
#                 if grad >= 1:
#                     gradf = np.gradient(mat)[0]
#                     mat = np.concatenate((mat, gradf), axis=1)

#                 #calc second order derivatives
#                 if grad == 2:
#                     grad2f = np.gradient(gradf)[0]
#                     mat = np.concatenate((mat, grad2f), axis=1)

#                 file_to_create = path_to_quats + "/" + file.split(".")[0] + "_processed.data"
#                 ff = open(file_to_create, "w")

#                 n = 1
#                 item = 0
#                 print("Creo il quaternione")
#                 # quats_dict = make_quaternion(mat)
#                 quats = make_quaternion(mat)

#                 print('Appendo la classe del dialetto al quaternione')
#                 dictionary = '\t' + dict_list[path_dict]
#                 # quats_dict.append(dictionary)
                
#                 quats_length = len(quats)

#                 while (item < quats_length):
#                     if item == N_SPLIT * n:
#                         ff.write(dictionary)
#                         ff.write("\n")
#                         n = n + 1
#                     quat = quats[item]
#                     for i in range(len(quats_length)):
#                         if i == 3:
#                             ff.write(str(quat[i]) + " ")
#                         else:
#                             ff.write(str(quat[i]) + ",")
#                     item = item + 1
                

#                 x = int((n*N_SPLIT) - quats_length)
#                 for i in range(x):
#                     if i < x-1:
#                         ff.write("0,0,0,0 ")
#                     else:
#                         ff.write("0,0,0,0")



# # print mat, frames, samplerate

# # print grad2f[0]
# # print gradf[0]
# # print mat[0][41:]
# # print mat.shape
#                 # for i in dirlist:
#                 #     print(f'Path: {int(i)}')
#                 #     #if i is os.listdir(i):
#                 #     if os.path.isdir(i):
#                 #         quats = make_quaternion(mat)
#                 #         dictionary = '  ' + dict_list[i]
                
#                 #         quats.append(dictionary)
#                 #         quats_length = len(quats)
#                 #         while (item < quats_length):
#                 #             if item == N_SPLIT * n:
#                 #                 ff.write("\n")
#                 #                 n = n + 1
#                 #             quat = quats[item]
#                 #             for i in range(len(quat)):
#                 #                 if i == 3:
#                 #                     ff.write(str(quat[i]) + " ")
#                 #                 else:
#                 #                     ff.write(str(quat[i]) + ",")
#                 #             item = item + 1
                        

#                 #         x = int((n*N_SPLIT) - quats_length)
#                 #         for i in range(x):
#                 #             if i < x-1:
#                 #                 ff.write("0,0,0,0 ")
#                 #             else:
#                 #                 ff.write("0,0,0,0")
dict_list = {'DR1': "1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
            'DR2': "0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
            'DR3': "0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
            'DR4': "0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0", 
            'DR5': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0 0,0,0,0", 
            'DR6': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0 0,0,0,0", 
            'DR7': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1 0,0,0,0", 
            'DR8': "0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 0,0,0,0 1,1,1,1" 
            }
dirlist = ['DR1', 'DR2', 'DR3', 'DR4', 'DR5', 'DR6', 'DR7', 'DR8']

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
  N_SPLIT = 400
  dir_name = "Quaternion_DICT_" + str(N_SPLIT)
#   tree = "./drive/My Drive/COLAB Neural/preprocessed_files_with_dict/" + dir_name
  tree = "/home/franci/Desktop/NN/Quaternion-speech-recognition/" + dir_name
#   if os.path.isdir(tree):
#       shutil.rmtree(tree)
#   os.makedirs("drive/My Drive/COLAB Neural/Quaternion_DICT_" + str(N_SPLIT))
  os.makedirs("Quaternion_DICT_" + str(N_SPLIT))
  
  path_to_quats = os.path.abspath("Quaternion_" + str(N_SPLIT))

  path_to_prep_files = os.path.abspath("preprocessed_files_with_dict")
  dir = os.listdir(path_to_prep_files)

  for path_dict in dir:
    print("Analizzo la cartella\n" + str(path_dict))
    dir_dict = os.listdir(path_to_prep_files + '/' + str(path_dict) + '/')

    for file in dir_dict:
      print("Mi trovo in for file in dir_dict\n"+ str(dir_dict) + "\n")
      print(file + "\n")
      if file.split(".")[1] == "WAV":
        print('Split\n')
        p = path_to_prep_files + '/' + str(path_dict) + '/'
        f = Sndfile(os.path.join(p, file), 'r')
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
        print('\nOra mi trovo in path_to quats: \n'+str(p) + '\n')
        file_to_create = p + file.split(".")[0] + "_processed.data"
        print('Mi trovo dopo file_to_create: '+ str(file_to_create) + '\n')
        ff = open(file_to_create, "w")
        n = 1
        item = 0
        print("Creo il quaternione")
        # quats_dict = make_quaternion(mat)
        quats = make_quaternion(mat)
        print('Appendo la classe del dialetto al quaternione')
        
        dictionary ='\t' + dict_list[path_dict]
        # quats_dict.append(dictionary)
        quats_length = len(quats)
        print(str(quats_length) + '\n')

        while (item < quats_length):
            if item == N_SPLIT * n:
                ff.write(dictionary)
                ff.write("\n")
                n = n + 1
            quat = quats[item]
            print('Ok')
            for i in range(len(quats)):
                if i == 3:
                  print('OK2')
                  ff.write(str(quats[i]) + " ")
                else:
                  ff.write(str(quats[i]) + ",")
            item = item + 1
        x = int((n*N_SPLIT) - quats_length)
        for i in range(x):
            if i < x-1:
                ff.write("0,0,0,0 ")
            else:
                ff.write("0,0,0,0")