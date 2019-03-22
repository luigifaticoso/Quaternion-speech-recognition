import os
import numpy as np


path = os.path.abspath("preprocessed_files")
dirs = os.listdir( path )
count = 0
average_sentence_duration = 0
duration = []
for i in dirs:
    if i.split(".")[1] == "PHN":
        f = open(os.path.join(path,i),"r")
        for i in f.readlines():
            start_time = int(i.split(" ")[0])
            end_time = int(i.split(" ")[1])
            phoneme = i.split(" ")[2]
            duration.append(end_time-start_time)

av = sum(duration)/len(duration)

stand_dev = np.std(np.array(duration))    


print(av)


print('STD_DEV')
print(stand_dev)