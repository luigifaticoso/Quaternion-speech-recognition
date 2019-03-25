import os, sys
from shutil import copy
import errno
# Open a file
os.makedirs("preprocessed_files")
preprocessed_path = path = os.path.abspath("preprocessed_files")
path = os.path.abspath("TRAIN")
dirs = os.listdir( path )
count = 0 
# This would print all the files and directories
for i in dirs:
   dialectpath = os.path.join(path,i)
   print(i)
   if i != '.DS_Store':
      os.makedirs(i)
      if os.path.isdir(dialectpath):
         dialectdirs = os.listdir( dialectpath )
         for e in dialectdirs:
            count += 1
            speakerpath = os.path.join(dialectpath,e)
            if os.path.isdir(speakerpath):
               #tutti gli elementi di questa cartella
               speakerdirs = os.listdir(speakerpath)
               for i in speakerdirs:
                  dialect_name = dialectpath[(len(dialectpath)-3):(len(dialectpath))]
                  path2 = "preprocessed_files/" + dialect_name
                  # path3 = "/Users/antoniolomuscio/Downloads/preprocessed_files/" + dialectpath[(len(dialectpath)-3):(len(dialectpath))]

                  if not os.path.isdir(path2):
                     print("Creo la cartella\n")
                     os.makedirs(path2)
                     new_name = i.split(".")[0] +"_"+ str(count) +"."+ i.split(".")[1]
                     os.rename(os.path.join(speakerpath,i), os.path.join(speakerpath,new_name))
                     print(f"Ecco il path: {str(speakerpath )}\n" )
                     copy(os.path.join(speakerpath,new_name), path2)
                  else:
                     print(f"Processo: {str(dialect_name)}")
                     new_name = i.split(".")[0] +"_"+ str(count) +"."+ i.split(".")[1]
                     os.rename(os.path.join(speakerpath,i), os.path.join(speakerpath,new_name))
                     copy(os.path.join(speakerpath,new_name), path2)

               