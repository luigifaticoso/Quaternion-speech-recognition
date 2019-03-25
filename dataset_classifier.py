import os

path = "files_for_neural"
preprocessed_path = os.path.abspath(path)
if not os.path.isdir(preprocessed_path):
    os.makedirs(preprocessed_path)

path_to_preprocess = os.path.abspath('Quaternion_100')

processed_audio_list = os.listdir(path_to_preprocess)

for audio in processed_audio_list:
    # apriamo l'audio processato e mettiamo i quaternioni in una lista
    f = open(os.path.abspath(os.path.join(path_to_preprocess,audio)), "r")
    rows_quaternion = f.readlines()

    # pulisco i quaternioni rimuovendo i leading e trailing whitespace
    stripped_list_row_quaternion = list(map(str.strip, rows_quaternion))

    # Divido i quaternioni in base allo spazio e ho una lista quaternions composta da quaternioni
    quaternions = list()
    for i in stripped_list_row_quaternion:
        quaternions = i.split(" ")
    
    #apro il file PHN associato
    path_to_phn = audio.split("_")[0] +"_"+ audio.split("_")[1] + ".PHN" 
    path_to_phn = os.path.join(os.path.abspath("preprocessed_files"),path_to_phn)

    f_phn = open(path_to_phn,'r')
    stripped_list_phn = list(map(str.strip, f_phn.readlines()))

    sentence_duration = int(stripped_list_phn[len(stripped_list_phn)-1].split(" ")[1])

    for phn in stripped_list_phn:
        split_phn = phn.split(" ")
        start_time = split_phn[0]
        end_time = split_phn[1]
        phonema = split_phn[2]
        duration = int(end_time) - int(start_time)
        
        ratio_duration = sentence_duration/duration
        percentage_phn_duration = 100/ratio_duration

        #ora vado a trovare la percentuale di quel fonema in termini di quaternioni
        len_audio_quaternion = len(stripped_list_row_quaternion) * len(quaternions)
        n_quaternions_phn = (len_audio_quaternion * percentage_phn_duration)/100
        print(f"il phonema {phonema} richiede {n_quaternions_phn} quaternioni")
        




    