import os

path = os.path.abspath("preprocessed_files")
dirs = os.listdir( path )
for i in dirs:
    if i.split(".")[1] == "PHN":
        print(i)