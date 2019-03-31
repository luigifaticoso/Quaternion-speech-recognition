"""
import os
import shutil
import numpy as np
from scikits.audiolab import Sndfile
import python_speech_features as sf

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
	
    # the number of filters in the filterbank, default 26
    numfilt = 40 #40

	# the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
    winlen = 0.025
	
    # the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
    winstep = 0.01
	
    # use  first or first+second order derivation
    grad = 2

	#number of elements for each set of quaternions
    N_SPLIT = 400

    dir_name = "Quaternion_" + str(N_SPLIT) + "_Lamush"
    # tree = "./drive/My Drive/COLAB Neural/preprocessed_files_with_dict" + dir_name
    tree = "/home/franci/Desktop/NN/Quaternion-speech-recognition/" + dir_name
    
    if os.path.isdir(tree):
        shutil.rmtree(tree)
    os.makedirs(dir_name)
    path_to_quats = os.path.abspath(dir_name)

    train_file = os.path.join(path_to_quats,"TRAIN_BIG_PEZZO_DI_DATA" + "_processed.data")
    dev_file = os.path.join(path_to_quats,"DEV_BIG_PEZZO_DI_DATA" + "_processed.data")
    test_file = os.path.join(path_to_quats,"TEST_BIG_PEZZO_DI_DATA" + "_processed.data")

    if os.path.isfile(train_file):
        os.remove(train_file)
    if os.path.isfile(dev_file):
        os.remove(dev_file)
    if os.path.isfile(test_file):
        os.remove(test_file)
    
    count = 0 
    
    path_to_prep_files = os.path.abspath("preprocessed_files_with_dict")
    dir = os.listdir(path_to_prep_files)

    for path_dict in dir:
        print("Analizzo la cartella " + str(path_dict))
        # tutti i file nella cartella
        dir_dict = os.listdir(path_to_prep_files + "/" + str(path_dict))

        for file in dir_dict:
            if file.split(".")[1] == "WAV":
                p = path_to_prep_files + "/" + str(path_dict) + "/" + file
                f = Sndfile(p, 'r')
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
                # ff = open(file_to_create, "w")

                ff = open(train_file, "w")
                fd = open(dev_file, "w")
                ft = open(test_file, "w")
                n = 1
                item = 0
                print("Creo il quaternione")
                # quats_dict = make_quaternion(mat)
                quats = make_quaternion(mat)
                print('Appendo la classe del dialetto al quaternione')
                dictionary ='\t' + dict_list[path_dict]
                # quats_dict.append(dictionary)
                quats_length = len(quats)

                if count > ((len(dir_dict)*90)/100):
                        while (item < quats_length):
                        if item == N_SPLIT * n:
                            fd.write(dictionary)
                            fd.write("\n")
                            n = n + 1
                        quat = quats[item]
                        for i in range(len(quat)):
                            if i == 3:
                                fd.write(str(quat[i]) + " ")
                            else:
                                fd.write(str(quat[i]) + ",")
                        item = item + 1
                    x = int((n*N_SPLIT) - quats_length)
                    for i in range(x):
                        if i < x-1:
                            fd.write("0,0,0,0 ")
                        else:
                            fd.write("0,0,0,0")
                elif count>((len(dir_dict)*70)/100):
                        while (item < quats_length):
                        if item == N_SPLIT * n:
                            ft.write(dictionary)
                            ft.write("\n")
                            n = n + 1
                        quat = quats[item]
                        for i in range(len(quat)):
                            if i == 3:
                                ft.write(str(quat[i]) + " ")
                            else:
                                ft.write(str(quat[i]) + ",")
                        item = item + 1
                    x = int((n*N_SPLIT) - quats_length)
                    for i in range(x):
                        if i < x-1:
                            ft.write("0,0,0,0 ")
                        else:
                            ft.write("0,0,0,0")
                else:    
                    while (item < quats_length):
                        if item == N_SPLIT * n:
                            ff.write(dictionary)
                            ff.write("\n")
                            n = n + 1
                        quat = quats[item]
                        for i in range(len(quat)):
                            if i == 3:
                                ff.write(str(quat[i]) + " ")
                            else:
                                ff.write(str(quat[i]) + ",")
                        item = item + 1
                    x = int((n*N_SPLIT) - quats_length)
                    for i in range(x):
                        if i < x-1:
                            ff.write("0,0,0,0 ")
                        else:
                            ff.write("0,0,0,0")
    count += 1
"""
######################################################################
#                               COLAB                                #
import os
import shutil
import numpy as np
from scikits.audiolab import Sndfile
import python_speech_features as sf

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
	
    # the number of filters in the filterbank, default 26
    numfilt = 40 #40

	# the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
    winlen = 0.025
	
    # the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
    winstep = 0.01
	
    # use  first or first+second order derivation
    grad = 2

	#number of elements for each set of quaternions
    N_SPLIT = 400
    #./drive/My Drive/COLAB Neural/
    dir_name = "Quaternion_" + str(N_SPLIT) + "_Lamush"
    tree = dir_name
    
    #tree = "/home/franci/Desktop/NN/Quaternion-speech-recognition/" + dir_name
    
    if os.path.isdir(tree):
        shutil.rmtree(tree)
    os.makedirs(dir_name)
    path_to_quats = os.path.abspath(dir_name)

    train_file = os.path.join(path_to_quats,"TRAIN" + "_processed.data")
    dev_file = os.path.join(path_to_quats,"DEV" + "_processed.data")
    test_file = os.path.join(path_to_quats,"TEST" + "_processed.data")

    if os.path.isfile(train_file):
        os.remove(train_file)
    if os.path.isfile(dev_file):
        os.remove(dev_file)
    if os.path.isfile(test_file):
        os.remove(test_file)
    
    #count = 0 
    
    path_to_prep_files = os.path.abspath("preprocessed_files_with_dict/")
    dir = os.listdir(path_to_prep_files)
    
    ff = open(train_file, "w")
    fd = open(dev_file, "w")
    ft = open(test_file, "w")
         
    for path_dict in dir:
        print("Analizzo la cartella " + str(path_dict))
        # tutti i file nella cartella
        dir_dict = os.listdir(path_to_prep_files + "/" + str(path_dict))
        count = 0
        for file in dir_dict:
            if file.split(".")[1] == "WAV":
                p = path_to_prep_files + "/" + str(path_dict) + "/" + file
                f = Sndfile(p, 'r')
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
                
                #file_to_create = path_to_quats + "/" + file.split(".")[0] + "_processed.data"
                # ff = open(file_to_create, "w")

                """
                ff = open(train_file, "w")
                fd = open(dev_file, "w")
                ft = open(test_file, "w")
                """
                
                n = 1
                item = 0
                print("Creo il quaternione")
                # quats_dict = make_quaternion(mat)
                quats = make_quaternion(mat)
                print('Appendo la classe del dialetto al quaternione')
                dictionary ='\t' + dict_list[path_dict]
                # quats_dict.append(dictionary)
                quats_length = len(quats)
                count += 1
                print('Quantita file nella cartella ' + path_dict + ': ' + str(len(dir_dict)) + ' '+ str(count))
                if count > (((len(dir_dict)/4)*90)/100):
                  print("Creo DEV_FILE "+ str(count))
                  while (item < quats_length):
                    if item == N_SPLIT * n:
                        fd.write(dictionary)
                        fd.write("\n")
                        n = n + 1
                    quat = quats[item]
                    for i in range(len(quat)):
                        if i == 3:
                            fd.write(str(quat[i]) + " ")
                        else:
                            fd.write(str(quat[i]) + ",")
                        item = item + 1
                  x = int((n*N_SPLIT) - quats_length)
                  for i in range(x):
                      if i < x-1:
                          fd.write("0,0,0,0 ")
                      else:
                          fd.write("0,0,0,0")
                elif count>(((len(dir_dict)/4)*70)/100):
                  print("Creo TEST_FILE " + str(count))
                  while (item < quats_length):
                        if item == N_SPLIT * n:
                            ft.write(dictionary)
                            ft.write("\n")
                            n = n + 1
                        quat = quats[item]
                        for i in range(len(quat)):
                            if i == 3:
                                ft.write(str(quat[i]) + " ")
                            else:
                                ft.write(str(quat[i]) + ",")
                        item = item + 1
                  x = int((n*N_SPLIT) - quats_length)
                  for i in range(x):
                      if i < x-1:
                          ft.write("0,0,0,0 ")
                      else:
                          ft.write("0,0,0,0")
                else:
                  print("Creo TRAIN_FILE "+ str(count))
                  while (item < quats_length):
                      if item == N_SPLIT * n:
                          ff.write(dictionary)
                          ff.write("\n")
                          n = n + 1
                      quat = quats[item]
                      for i in range(len(quat)):
                          if i == 3:
                              ff.write(str(quat[i]) + " ")
                          else:
                              ff.write(str(quat[i]) + ",")
                      item = item + 1
                  x = int((n*N_SPLIT) - quats_length)
                  for i in range(x):
                      if i < x-1:
                          ff.write("0,0,0,0 ")
                      else:
                          ff.write("0,0,0,0")
    #count = 0
    ff.close()
    ft.close()
    fd.close()

""""
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
	
    # the number of filters in the filterbank, default 26
    numfilt = 40 #40

	# the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
    winlen = 0.025
	
    # the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
    winstep = 0.01
	
    # use  first or first+second order derivation
    grad = 2

	#number of elements for each set of quaternions
    N_SPLIT = 400

    dir_name = "./drive/My Drive/COLAB Neural/Quaternion_" + str(N_SPLIT) + "_Lamush"
    tree = "./drive/My Drive/COLAB Neural/" + dir_name
#     tree = "/home/franci/Desktop/NN/Quaternion-speech-recognition/" + dir_name
    if os.path.isdir(tree):
        shutil.rmtree(tree)
    
    os.makedirs(dir_name)
    path_to_quats = os.path.abspath(dir_name)
    
    path_to_prep_files = os.path.abspath("./drive/My Drive/COLAB Neural/preprocessed_files_with_dict/")
    dir = os.listdir(path_to_prep_files)

    for path_dict in dir:
        print("Analizzo la cartella " + str(path_dict))
        dir_dict = os.listdir(path_to_prep_files + "/" + str(path_dict))

        for file in dir_dict:
            if file.split(".")[1] == "WAV":
                p = path_to_prep_files + "/" + str(path_dict) + "/" + file
                f = Sndfile(p, 'r')
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
                print("Creo il quaternione")
                # quats_dict = make_quaternion(mat)
                quats = make_quaternion(mat)
                print('Appendo la classe del dialetto al quaternione')
                dictionary ='\t' + dict_list[path_dict]
                # quats_dict.append(dictionary)
                quats_length = len(quats)

                while (item < quats_length):
                    if item == N_SPLIT * n:
                        ff.write(dictionary)
                        ff.write("\n")
                        n = n + 1
                    quat = quats[item]
                    for i in range(len(quat)):
                        if i == 3:
                            ff.write(str(quat[i]) + " ")
                        else:
                            ff.write(str(quat[i]) + ",")
                    item = item + 1
                x = int((n*N_SPLIT) - quats_length)
                for i in range(x):
                    if i < x-1:
                        ff.write("0,0,0,0 ")
                    else:
                        ff.write("0,0,0,0")
""""