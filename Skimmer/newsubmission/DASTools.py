#!/usr/bin/env python

import os 
from commands import getoutput # Deprecated, update! 
import subprocess

import json

import argparse
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

# Two different versions (Korbinian's version below, adapted) maybe converge to chose a single one
def queryGOClient(name, querytype="file", datatype="dataset", dbs_instance="prod/global", json = False):
    query = querytype+" "+datatype+"="+name+" instance="+dbs_instance
    cmd = 'dasgoclient -query="%s"' % query
    if json:
       cmd += " -json" 
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    a = proc.communicate()
    return a[0]

def parseGOquery(queryoutput): 

    tmpList = querryoutput[0].split(os.linesep)
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



# Legacy lists of the files in the dataset (used a.o. for slurm jobs) 
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


def GenerateGCDatasetFiles(DASName, output, prefix="root://cms-xrd-global.cern.ch/", overwritename=None, instance="prod/global"):

    # Make a query
    datasetfiles = queryGOClient(DASName, querytype="file", datatype="dataset", dbs_instance=instance, json=True) #json format to have all info (e.g. sample size, ...) 
    datasetfiles = datasetfiles.replace("[\n","")
    datasetfiles = datasetfiles.replace("\n]\n","")

    allJSONs = []
    for j in datasetfiles.split(" ,"):
        allJSONs.append(json.loads(j))

    outputLines = []
    for j in allJSONs:
        outputLines.append(prefix+str(j["file"][0]["name"])+" = "+str(j["file"][0]["nevents"]))

    datasetname = DASName.split("/")[1]+DASName.split("/")[2] if overwritename is None else overwritename # TODO: shere we take the sample name and the version, because for data the run (A, B, C, D) is in the version

    # Make folder to write the GC conf file 
    if not os.path.exists(output):
        os.makedirs(output)

    # Write lines to file      
    filename = output+"/"+datasetname+".txt"
    with open(filename, "w") as f:
        f.write("["+datasetname+"]\n")
        for line in outputLines:
            f.write(line+"\n") 

    return filename


    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="collect crab_nano output and make dataset .txt files")
    parser.add_argument("--name" , required=True, help="DAS dataset name", type=str)
    parser.add_argument("--outpath", default=".", help="path to store dataset .txt files", type=str)
    parser.add_argument("--prefix", default="root://cms-xrd-global.cern.ch/", help="server prefix to add to rootfiles", type=str)
    parser.add_argument("--dbs",action = "store", help = "DAS dbs for the query",type=str,required = False, default = "prod/global")
    parser.add_argument("--DSName", action="store", help="Passed variable will be used as file and dataset name. Otherwise DAS name will be used",default=None)
    args = parser.parse_args()

 
    main(args.name, args.dbs, args.prefix, args.outpath, args.DSName)
