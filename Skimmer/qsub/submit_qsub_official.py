#!/usr/bin/env python
import os, glob, sys
from commands import getoutput
import re
import datetime
import subprocess
import itertools

now = datetime.datetime.now()
timestamp =  now.strftime("%Y_%m_%d")
queue = "all.q"
#queue = "long.q"
#queue = "short.q"
nfilesperjob = 5

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))
        
def getFileListDAS(dataset,instance="prod/phys03",run=-1):
  cmd='das_client --limit=0 --query="file dataset=%s instance=%s"'%(dataset,instance)
#  cmd='das_client --limit=0 --query="file dataset=%s"'%(dataset,)
  print "Executing ",cmd
  cmd_out = getoutput( cmd )
  tmpList = cmd_out.split(os.linesep)
  files = []
  for l in tmpList:
     if l.find(".root") != -1:
        files.append(l)
           
  return files 

def getFileList(name):
  files = open("fileLists/"+name+".txt", "r").read().splitlines()
  return files

def createLists(dataset, name):
  cmd='das_client --limit=0 --query="file dataset=%s"'%(dataset,)
  print "Executing ",cmd
  cmd_out = getoutput( cmd )
  tmpList = cmd_out.split(os.linesep)
  files = []
  for l in tmpList:
     if l.find(".root") != -1:
        files.append(l)
        
  fileName = "fileLists/"+name+".txt"
  with open(fileName, "w") as f:
    for l in files:
        f.write("%s\n" % l)
  print "Wrote file list", fileName
  return




def createJobs(f, outfolder,name,nchunks):
  infiles = []
  for files in f:
    infiles.append("root://cms-xrd-global.cern.ch/"+files)
  cmd = 'python qsub_script_SFs.py %s %s %s %i \n'%(','.join(infiles), outfolder,name,nchunks)
  #print cmd
  jobs.write(cmd)
  return 1

def submitJobs(jobList, nchunks, outfolder, batchSystem):
    print 'Reading joblist'
    jobListName = jobList
    #print jobList
#    subCmd = 'qsub -t 1-%s -o logs nafbatch_runner_GEN.sh %s' %(nchunks,jobListName)
    subCmd = 'qsub -q %s -t 1-%s -o %s/logs/ %s %s' %(queue,nchunks,outfolder,batchSystem,jobListName)
    print 'Going to submit', nchunks, 'jobs with', subCmd
    os.system(subCmd)

    return 1


if __name__ == "__main__":
  out = "Skimmed_%s/"%timestamp
  batchSystem = 'psibatch_runner.sh'
  createlists = False

  patternsData  = [
    "/SingleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD", #241608232
    "/SingleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD", #119918017
    "/SingleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD", #110032072
    "/SingleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD", #506468530
  ]
  patternsTT    = [
    "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM", #43732445
    "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM", #9000000
  ]
  patternsST    = [
    "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM", #4955102
    "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM", #5635539
    "/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM", #5982064
    "/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #3675910
    "/ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #6898000
    "/ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #2953000
  ]
  patternsVV    = [
    "/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #5054286
#    "/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM", #8782525
    "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #27582164
    "/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #19086373
    "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #27757211
  ]
  patternsWJets = [ #/WJetsToLNu_HT*/*Fall17NanoAODv4*Nano14Dec2018*/NANOAODSIM
    "/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #35778081
    "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #21250517
    "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #14313274
    "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #21709087
    "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #20432728
    "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #20258624
    "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", #21495421
  ]
  
  patterns = []
  if len(sys.argv) > 1:
    if sys.argv[1].find("data")!=-1:  patterns = patternsData  
    if sys.argv[1].find("TT")!=-1:    patterns = patternsTT    
    if sys.argv[1].find("ST")!=-1:    patterns = patternsST    
    if sys.argv[1].find("VV")!=-1:    patterns = patternsVV    
    if sys.argv[1].find("WJets")!=-1: patterns = patternsWJets 
    if sys.argv[1].find("ALL")!=-1:   patterns = patternsTT+patternsST+patternsVV+patternsWJets+patternsData
  
    print 'Location of input files',  patterns
  else:
    print "No location given, give folder with files"
    exit(0)
  
  if len(sys.argv) > 2:
    if sys.argv[2].find("-c")!=-1: createlists = True
    else:
      out = sys.argv[2]
      print 'Output goes here: ', out
  else:
    print "Using default output folder: ", out
  
  try: os.stat(out)
  except: os.mkdir(out)
  
  if createlists:
      for pattern in patterns:
        name = pattern.split("/")[1].replace("/","") + ("-" + pattern.split("/")[2].split("-")[0] if 'Run201' in pattern else "")
        createLists(pattern, name)
  
  for pattern in patterns:
    name = pattern.split("/")[1].replace("/","") + ("-" + pattern.split("/")[2].split("-")[0] if 'Run201' in pattern else "")
    try:
      files = getFileList(name)
    except:
      exit()
      files = getFileListDAS(pattern)
    
#    print "FILELIST = ", files
    print "creating job file " ,'joblist%s.txt'%name
    jobList = 'joblist%s.txt'%name
    jobs = open(jobList, 'w')
    nChunks = 0
    outfolder = out+name
    try: os.stat(outfolder)
    except: os.mkdir(outfolder)
    try: os.stat(outfolder+'/logs/')
    except: os.mkdir(outfolder+'/logs/')
    
    filelists = list(split_seq(files, nfilesperjob))
    
    print "Creating", len(filelists), "jobs each with files:", [len(x) for x in filelists]
    for f in filelists:
      #print "FILES = ",f
      createJobs(f,outfolder,name,nChunks)
      nChunks = nChunks+1
    
    jobs.close()
#    submit = raw_input("Do you also want to submit the jobs to the batch system? [y/n]")
    submit = 'y'
    if submit == 'y' or submit=='Y':
      submitJobs(jobList,nChunks, outfolder, batchSystem)
    else:
      print "Not submitting jobs"
    
    
    
  
