import os
import numpy as np

path = os.path.abspath("preprocessed_files")
dirs = os.listdir( path )
count = 0
sentence_duration = []
duration = []
phoneme_duration = {}
phoneme_duration_STD = {}
somma = 0
deviations = []
dict_average = 0
phoneme_list = list()
phoneme_duration_median = {}
median_calc = []
for i in dirs:
    if i.split(".")[1] == "PHN":
        f = open(os.path.join(path,i),"r")
        rows = f.readlines()
        for i in range(len(rows)):
            start_time = int(rows[i].split(" ")[0])
            end_time = int(rows[i].split(" ")[1])
            phoneme = rows[i].split(" ")[2].split("\n")[0]
            phoneme_list.append(phoneme)
            if phoneme not in phoneme_duration.keys():
                phoneme_duration[phoneme] = []
                phoneme_duration_STD[phoneme] = []
                phoneme_duration_median[phoneme] = []
            else:
                phoneme_duration[phoneme].append(end_time-start_time)
                phoneme_duration_STD[phoneme].append(end_time-start_time)
                phoneme_duration_median[phoneme].append(end_time-start_time)
            duration.append(end_time-start_time)

            if i == len(rows)-1:
                sentence_duration.append(end_time)
for e in phoneme_duration:
    phoneme_duration[e] = int(sum(phoneme_duration[e])/len(phoneme_duration[e]))
    somma = somma + phoneme_duration[e]
dict_average = somma/len(phoneme_duration)


for e in phoneme_duration_STD:
    std_temp = np.std(np.array(phoneme_duration_STD[e]))
    deviations.append([int(std_temp)])
    
    mediana = np.median(np.array(phoneme_duration_median[e]))
    median_calc.append([int(mediana)])




stand_dev_phonems = np.std(np.array(deviations))
final_mediana = np.median(np.array(median_calc))
# stand_dev_sentences = np.std(np.array(sentence_duration)) 

unique_list = []
for el in phoneme_list:
    if el not in unique_list:
        unique_list.append(el)

print(f"Numero di fonemi singoli (senza duplicati) {len(unique_list)}")
print(f"Durata media pesata in base alla frequenza di ogni fonema: {int(dict_average)}")
print(f"Durata media di tutti i fonemi: {int(sum(duration)/len(duration))}")
print(f"Durata media di tutte le frasi: {int(sum(sentence_duration)/len(sentence_duration))}")
print(f"Scarto quadratico medio di tutti i fonemi: {int(stand_dev_phonems)}" )
print(f"Medianda di tutti i fonemi: {int(final_mediana )}" )

# Generazioni classi fonemi per dataset_classifier
for i in range(len(unique_list)):
    fonema_class = f"'{unique_list[i]}' : '"
    for j in range(len(unique_list)):
        if i == j:
            fonema_class+="1,1,1,1 "
        else:
            fonema_class+="0,0,0,0 "
    
    fonema_class+="',"
    print(fonema_class)
        

