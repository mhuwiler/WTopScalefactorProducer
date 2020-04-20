#!/usr/bin/env python

import os 
from commands import getoutput # Deprecated, update! 
#import itertools


"""
def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))
"""

#Other possible definition
def split_seq(seq,size):
    """ Split up seq in pieces of size """
    return [seq[i:i+size] for i in range(0, len(seq), size)]

def getFileListDAS(dataset,instance="prod/global",run=-1):
  cmd='dasgoclient --limit=0 --query="file dataset=%s instance=%s"'%(dataset,instance) # maybe replace that by the python package 
#  cmd='das_client --limit=0 --query="file dataset=%s"'%(dataset,)
  #print "Executing ",cmd
  cmd_out = getoutput( cmd )
  tmpList = cmd_out.split(os.linesep)
  files = []
  for l in tmpList:
     if l.find(".root") != -1:
        files.append(l)
           
  return files 

def getDatasetNameFromPath(pattern): 
	name = pattern.split("/")[1].replace("/","") + ("-" + pattern.split("/")[2].split("-")[0] if 'Run201' in pattern else "")
	return name

"""
def getFileList(name, listDirectory):
  files = open(listDirectory+"/"+name+".txt", "r").read().splitlines()
  return files
"""

def openCatalogue(catalogue):   # opening the catalogue and getting back a dictionary of lits of files orddered by datasetname (might be replaced by a json file) 
  onlyfiles = [f for f in os.listdir(catalogue) if os.path.isfile(os.path.join(catalogue, f))]
  if (not len(onlyfiles) == len(os.listdir(catalogue))): 
    print "Error: The catalogue is corrupted! Please consider rerunning the local catalogue creation (options -r -f). "  # TODO: make sure to remove the folder in case of overwriting
    exit(0)

  dataset={}
  for filename in onlyfiles: 
    with open(os.path.join(catalogue, filename), "r") as file: 
      dataset[filename] = file.read().splitlines()

  return dataset




def createLists(listDirectory, dataset, name=""):
  """
  instance="prod/phys03"
  cmd='das_client --limit=0 --query="file dataset=%s"'%(dataset)
  print "Executing ",cmd
  cmd_out = getoutput( cmd )
  tmpList = cmd_out.split(os.linesep)
  files = []
  for l in tmpList:
     if l.find(".root") != -1:
        files.append(l)
  """
  if name=="": 
  	name = getDatasetNameFromPath(dataset)
  files = getFileListDAS(dataset)
        
  fileName = listDirectory+"/"+name+".txt"
  with open(fileName, "w") as f:
    for l in files:
        f.write("%s\n" % l)
  print "Wrote file list: ", fileName
  return