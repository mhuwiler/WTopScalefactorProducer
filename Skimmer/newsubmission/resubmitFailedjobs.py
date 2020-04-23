#!/usr/bin/env python

import os
import sys
import glob
import ROOT 
import subprocess
import pandas as pd


directory = "production/Wtagging/"

readprefix = "/pnfs/psi.ch/cms/trivcat/store/user/mhuwiler/" # prefix to storage element in read access 
writeprefix = "root://t3dcachedb03.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mhuwiler/" # prefix to storage element for xrootd and gfal commands 

configfile = "productionTTnosdmasscut.conf"

directorySubStructure = "/*/*.root" # What directory structure the job writes 

dryrun = True 

verbose = True

# Getting the job name from GC using the config file 
jobconfiguration = os.popen("go.py "+configfile+ " --help-conf").read().split("\n")
jobnameline = [line for line in jobconfiguration if "Current task ID" in line]
jobname = jobnameline[0].replace("Current task ID: ", "")

databasename = configfile.replace(".conf", "_jobresults.csv")

try: 
	jobstatus = pd.read_csv(databasename, index_col=0)
	iteration = jobstatus["Iteration"].max()
        if (not dryrun): iteration+=1
	if (verbose): print "Opened existing database:", databasename

except: 
	jobstatus = pd.DataFrame(columns=["OutputFileName", "isFile", "isOpen", "isValid", "treeFilled", "isBroken", "DatasetName", "JobNum", "Iteration"])
	iteration = 1
	if (verbose): print "Created database from scratch", databasename

if (verbose): print "Checking job:", jobname, " iteration:", iteration

# Listing the files that were written to the destination 
listoffiles = glob.glob(readprefix+directory+jobname+directorySubStructure) # in order to use wildcards not supported in os.listdir 

#print listoffiles # Works so far 

alljobs = []
failedjobs = []

for filename in listoffiles: 
	strippedFileName = filename.replace(readprefix, "")
	xrdfilename = writeprefix+strippedFileName
	datasetname = strippedFileName.split("/")[-2]
	lastChunck = strippedFileName.split("/")[-1]
	#print lastChunck
	jobNum=int(lastChunck.replace("job_", "").replace("_out.root", ""))

	if (verbose) : 
		print "\tFilename:", filename
		print "\tStripped filename:", strippedFileName
		print "\tXROOTD file name:", xrdfilename
		print "\tDataset Name:", datasetname
		print "\tJob number:", jobNum

	isOpen = False
	isValid = False
	treeFilled = False
	isFile = os.path.isfile(filename)
	if isFile: 
		file = ROOT.TFile.Open(xrdfilename, "r")
		isOpen = file.IsOpen()
		if isOpen: 
			isValid = (file.GetListOfKeys().Contains("Runs") and file.GetListOfKeys().Contains("Events"))
			
			if isValid: 
				tree = file.Get("Events")
				treeFilled = (tree.GetEntries() > 1)
		file.Close()

	isBroken = not (isFile and isOpen and isValid and treeFilled)

	print isBroken, isFile, isOpen, isValid, treeFilled

	alljobs.append(jobNum)

	jobstatus = jobstatus.append({"OutputFileName": filename, "isFile":int(isFile), "isOpen":int(isOpen), "isValid":int(isValid), "treeFilled":int(treeFilled), "isBroken":int(isBroken), "DatasetName":datasetname, "JobNum":jobNum, "Iteration":iteration}, ignore_index=True)

	if (isBroken): 
		failedjobs.append(jobNum)

		rmCommand = "LD_LIBRARY_PATH='' PYTHONPATH='' gfal-rm "+xrdfilename # fixes to make gfal-rm compatible with CMSSW current version 
		if (verbose): print "rm command:", rmCommand
		if not dryrun: os.system(rmCommand)

		resetCommand = "nohup go.py "+configfile+" --reset id:{} > /dev/null 2>&1 &".format(jobNum) # nohup to run it in parallel in background and setting output to null
		#resetCommand = ["nohup go.py", configfile, "--reset", "id:{}".format(jobNum)]
		if (verbose): print "reset command:", resetCommand
		if not dryrun: os.system(resetCommand) #subprocess.Popen(resetCommand, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)


print failedjobs
print jobstatus
if (not dryrun): jobstatus.to_csv(databasename)

print failedjobs

totalNumOfJobs = max(alljobs)
print "Missing output file for jobs: "
for index in range(0, totalNumOfJobs): 
	if index not in alljobs: 
		print "\tMissing output file for job:", index





