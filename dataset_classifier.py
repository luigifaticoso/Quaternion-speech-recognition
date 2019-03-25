import os

path = "files_for_neural_gigi"
preprocessed_path = os.path.abspath(path)
if not os.path.isdir(preprocessed_path):
    os.makedirs(preprocessed_path)

path_to_preprocess = os.path.abspath('Quaternion_100')

processed_audio_list = os.listdir(path_to_preprocess)

for audio in processed_audio_list:
    # apriamo l'audio processato e mettiamo i quaternioni in una lista
    f = open(os.path.abspath(os.path.join(path_to_preprocess,audio)), "r+")
    rows_quaternion = f.readlines()

    # pulisco i quaternioni rimuovendo i leading e trailing whitespace
    stripped_list_row_quaternion = list(map(str.strip, rows_quaternion))

    # Divido i quaternioni in base allo spazio e ho una lista quaternions composta da quaternioni
    quaternions = []
    for i in range(len(stripped_list_row_quaternion)):
        array_tmp = stripped_list_row_quaternion[i].split(" ")
        for e in array_tmp:
            quaternions.append(e)
        stripped_list_row_quaternion[i] = quaternions
        quaternions = []

    
    #apro il file PHN associato
    path_to_phn = audio.split("_")[0] +"_"+ audio.split("_")[1] + ".PHN" 
    path_to_phn = os.path.join(os.path.abspath("preprocessed_files"),path_to_phn)

    f_phn = open(path_to_phn,'r')
    stripped_list_phn = list(map(str.strip, f_phn.readlines()))

    sentence_duration = int(stripped_list_phn[len(stripped_list_phn)-1].split(" ")[1])
    quaternion_index = 1
    last_quat_less = 0
    for phn in stripped_list_phn:
        split_phn = phn.split(" ")
        start_time = split_phn[0]
        end_time = split_phn[1]
        phonema = split_phn[2]
        duration = int(end_time) - int(start_time)
        
        ratio_duration = sentence_duration/duration
        percentage_phn_duration = 100/ratio_duration

        #ora vado a trovare la percentuale di quel fonema in termini di quaternioni
        row_dimension = len(stripped_list_row_quaternion[0])
        len_audio_quaternion = len(stripped_list_row_quaternion) * row_dimension
        n_quaternions_phn = int((len_audio_quaternion * percentage_phn_duration)/100)

        while(n_quaternions_phn>0):

            if n_quaternions_phn > row_dimension - last_quat_less:
                n_quaternions_phn -= row_dimension - last_quat_less
                last_quat_less = 0

                # TODO: segnare che quella riga è quel phonema
                # stripped_list_row_quaternion[quaternion_index]

                print(f"la riga {quaternion_index} è il fonema {phonema}")
                quaternion_index += 1

            elif n_quaternions_phn > 50:

                last_quat_less = n_quaternions_phn
                n_quaternions_phn -= n_quaternions_phn
                print(f"la riga {quaternion_index} è il fonema {phonema}")

            elif n_quaternions_phn <= 50:
                
                last_quat_less = n_quaternions_phn
                n_quaternions_phn -= n_quaternions_phn
    print(audio)
        
            


        




    