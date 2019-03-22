import os

path = os.path.abspath("preprocessed_files")
dirs = os.listdir( path )
count = 0
sentence_duration = []
duration = []
phoneme_duration = {}
somma = 0
dict_average = 0
for i in dirs:
    if i.split(".")[1] == "PHN":
        f = open(os.path.join(path,i),"r")
        rows = f.readlines()
        for i in range(len(rows)):
            start_time = int(rows[i].split(" ")[0])
            end_time = int(rows[i].split(" ")[1])
            phoneme = rows[i].split(" ")[2].split("\n")[0]
            if phoneme not in phoneme_duration.keys():
                phoneme_duration[phoneme] = []
            else:
                phoneme_duration[phoneme].append(end_time-start_time)
            duration.append(end_time-start_time)

            if i == len(rows)-1:
                sentence_duration.append(end_time)
for e in phoneme_duration:
    phoneme_duration[e] = int(sum(phoneme_duration[e])/len(phoneme_duration[e]))
    somma = somma + phoneme_duration[e]
dict_average = somma/len(phoneme_duration)
print(f"Durata media pesata in base alla frequenza di ogni fonema: {int(dict_average)}")
print(f"Durata media di tutti i fonemi: {int(sum(duration)/len(duration))}")
print(f"Durata media di tutte le frasi: {int(sum(sentence_duration)/len(sentence_duration))}")
