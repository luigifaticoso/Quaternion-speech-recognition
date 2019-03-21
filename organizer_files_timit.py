import os, sys
from shutil import copy
# Open a file
os.makedirs("preprocessed_files")
preprocessed_path = path = os.path.abspath("preprocessed_files")
path = os.path.abspath("TRAIN")
dirs = os.listdir( path )
count = 0 
# This would print all the files and directories
for file in dirs:
   dialectpath = os.path.join(path,file)
   if os.path.isdir(dialectpath):
      dialectdirs = os.listdir( dialectpath )
      for e in dialectdirs:
         count += 1
         speakerpath = os.path.join(dialectpath,e)
         if os.path.isdir(speakerpath):
            speakerdirs = os.listdir( speakerpath )
            for i in speakerdirs:
               new_name = i.split(".")[0] +"_"+ str(count) +"."+ i.split(".")[1]
               os.rename(os.path.join(speakerpath,i), os.path.join(speakerpath,new_name))
               copy(os.path.join(speakerpath,new_name), preprocessed_path)

               