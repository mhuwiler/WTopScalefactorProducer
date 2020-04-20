#!/usr/bin/env python
import os, glob, sys
from commands import getoutput
import re
import datetime
import subprocess
import itertools
from DASTools import *
from Dataset import getDataset
import argparse
from JobSubmissionEngine import JobSubmissionEngine

now = datetime.datetime.now()
timestamp =  now.strftime("%Y_%m_%d")
queue = "all.q"
#queue = "long.q"
#queue = "short.q"
nfilesperjob = 1

listDirectory = "fileLists_Autumn18_v5/"







def CreateHTCondorFile(submitfilename, argumentfilename, queuename="testmatch"): # 1 week: nextweek, 3 days: testmatch
  print "Making HTCondor submit file... "
  # Setting the parameters in the model file
  with open("./submitfileslibrary/SubmitCondor.sh", 'r') as submitfilemodel:
    submitfile = open(submitfilename, 'w')
    submitfile.write(submitfilemodel.read().replace("[executable]", "executablecondor.sh").replace("[arguments]", argumentfilename).replace("[queue]", queuename))
    submitfile.close()
  os.system("cp ./submitfileslibrary/executablecondor.sh . ")



def createJobs(jobfile, f, outfolder,name,nchunks, gridEngine):
  infiles = []
  for files in f:
    infiles.append("root://cms-xrd-global.cern.ch/"+files)
  if gridEngine == "HTCondor": 
    cmd = '%s %s %s %i, %s \n'%(','.join(infiles), outfolder,name,nchunks, outfolder)
  else: 
    cmd = 'python qsub_script_SFs.py %s %s %s %i \n'%(','.join(infiles), outfolder,name,nchunks)

  #CreateHTCondorFile(submitfilename, os.path.basename(jobfile.name))
  #print cmd
  jobfile.write(cmd)
  return 1

def submitJobs(jobList, nchunks, outfolder, submitfilename, gridEngine):
    print 'Reading joblist'
    jobListName = jobList
    #print jobList
#    subCmd = 'qsub -t 1-%s -o logs nafbatch_runner_GEN.sh %s' %(nchunks,jobListName)
   #subCmd = 'qsub -q %s -t 1-%s -o %s/logs/ %s %s' %(queue,nchunks,outfolder,submitfilename,jobListName)
    if gridEngine=="HTCondor": 
      subCmd = 'condor_submit {}'.format(submitfilename)
    elif gridEngine=="Slurm":
      subCmd = 'sbatch --array=1-%d %s %s' %(nchunks, submitfilename, jobListName)

    print 'Going to submit', nchunks, 'jobs with', subCmd
    #os.system(subCmd)

    return 1


if __name__ == "__main__":


  parser = argparse.ArgumentParser(description='Job submission engine')

  parser.add_argument('dataset', default = None, help="Which dataset to produce [mandatory]")
  parser.add_argument('-c','--createlist', action = 'store_true', help = 'Create file list from CMS DAS')
  parser.add_argument('-d','--dry', action = 'store_true', help = 'Run in dry mode (create but do not submit jobs)')
  parser.add_argument('-b','--batch', action = 'store_true', help = 'run in batch mode (no printout) ')
  parser.add_argument('-o', '--output', action = 'store', type=str, dest='output', default="", help = 'Where to store the output')
  parser.add_argument('-s', '--batchsystem', action='store', type=str, dest='gridengine', default="HTCondor", help = 'Which grid engine runs as backend (e.g. HTCondor, Slurm, SGD)')
  parser.add_argument('-v', '--verbose', action='store_true', help = 'Give a lot of output (verbose)')
  parser.add_argument('-j', '--jobconfig', action='store', type=str, dest='jobfilename', default="", help = "The name of the json config file for the job. ")
  parser.add_argument('-f', '--force', action='store_true', help="Force overwriting (the catalogue or job config file)")
  parser.add_argument('-m', '--multiplicity', action='store', type=int, default=10, help="Number of files per job")

  args = parser.parse_args() 

  debug=True 


  gridengine = args.gridengine #"HTCondor" #"HTCondor", "SGD"

  out = "Skimmed_%s/"%timestamp
  
  if gridengine=="SGD": 
    submitFileName = 'psibatch_runner.sh'
  elif gridengine=="HTCondor":
    submitFileName = 'SubmitCondorProd.sh' #'psibatch_runner.sh'
  elif gridengine=="Slurm": 
    submitFileName = "SlurmSubmit.sh" #'psibatch_runner.sh'

  createlists = False


  
  patterns = getDataset(args.dataset)
  
  if debug: 
    if args.output:
      out = args.output
      print 'Output goes here: ', out
    else: 
      print "Using default output folder: ", out
    
    if (args.createlist): 
      print "Creating list of files " 

    if args.dry: 
      print "Running in dry mode. " 

    print "Grid engine: {}".format(args.gridengine)
      
    
  
  try: os.stat(out)
  except: os.mkdir(out)


  engine = JobSubmissionEngine(args, patterns)


  
  if createlists:
      for pattern in patterns:
        name = getDatasetNameFromPath(pattern)
        createLists(pattern, name)
  else:

    numberOfJobs = 0
    argumentfilename = "arguments.txt"
    with open(argumentfilename, "w") as file: # Emptying argument file for condor 
      pass

    for pattern in patterns:
      name = getDatasetNameFromPath(pattern)
      try:
        files = getFileList(name)
      except:
        exit()
        files = getFileListDAS(pattern)
      
  #    print "FILELIST = ", files
      print "creating job file " ,'joblist%s.txt'%name
      if gridengine=="HTCondor": 
        jobList = argumentfilename #'joblist%s.txt'%name
        writeopt = "a"
      else: 
        jobList = 'joblist%s.txt'%name
        writeopt = "w"
      jobs = open(jobList, writeopt)
      nChunks = 0
      outfolder = out+name
      try: os.stat(outfolder)
      except: os.mkdir(outfolder)
      try: os.stat(outfolder+'/logs/')
      except: os.mkdir(outfolder+'/logs/')
      
      filelists = list(split_seq(files, nfilesperjob))

      if gridengine == "HTCondor": 
        CreateHTCondorFile(submitFileName, jobList)
      elif gridengine == "Slurm": 
        os.system("cp ./submitfileslibrary/SlurmSubmit.sh . ") # TODO: set this in thee function 
      
      print "Creating", len(filelists), "jobs each with files:", [len(x) for x in filelists]
      for f in filelists:
        #print "FILES = ",f
        createJobs(jobs, f,outfolder,name,nChunks, gridengine)
        nChunks = nChunks+1

        numberOfJobs+=1
      
      jobs.close()

      with open("jobCount.txt", "w") as jobCountFile: # putting this here (with w) so that it writes the correct total number of jobs submitted even if the script doesn't run until the end.
        print numberOfJobs
        jobCountFile.write("{0}".format(numberOfJobs))

  #    submit = raw_input("Do you also want to submit the jobs to the batch system? [y/n]")
      submit = 'y'
      if submit == 'y' or submit=='Y':
        submitJobs(jobList,nChunks, outfolder, submitFileName, gridengine)
      else:
        print "Not submitting jobs"
    
    
    
  
