#!/usr/bin/env python

import os 
from DASTools import *


class GridBackend(object): 
	def __init__(self, jobconfig): 
		print "Constructor of GridBackend class"
		self.verbose = jobconfig.verbose
		self.xrdprefix = "root://cms-xrd-global.cern.ch/"
	def PrepareJobs(self, params): 
		#Do some stuff 
		print "Do some stuff"
	def WriteJobconfig(self, configFileName): 
		#if (not os.path.isdir(configFileName) or self.force): 
		with open(configFileName, "w") as configfile: 
			configfile.write(json.dumps(self.config, insent=4)) # json.dumps(self.StoreInfo, indent=4, sort_keys=True) indent to make it human readable
			configfile.close()

	def RunJobs(self, jobconfig): 
		# Do some stuff 
		print "Do some stuff"

class HTCondorBackend(GridBackend): 
	def __init__(self, jobconfig): 
		super().__init__(jobconfig)
		self.argfilename = "arguments.txt"

	def PrepareJobs(self, params): 
		#Do some stuff
		print "Do some stuff"


class SlurmBackend(GridBackend): 
	def __init__(self, jobconfig):
		super(SlurmBackend, self).__init__(jobconfig)
		self.exename = "python qsub_script_SFs.py"
		self.submitdir = "./submit"
		self.outfolder = "./output"
		self.submitfilename = "submitfileslibrary/SlurmSubmit.sh"
		if (not os.path.isdir(self.submitdir)): 
			os.mkdir(self.submitdir)
		if (not os.path.isdir(self.outfolder)): 
			os.mkdir(self.outfolder)

	def PrepareJobs(self, dataset, multiplicity): 
		for key, files in dataset.items(): 
			if self.verbose and False: 
				print "PrepareJobs got dataset: \n\nkey: {}\nfiles:{}".format(key, files)

			number = len(files)
			print "Number of files for dataset {}: {} ".format(key, number)
			filelists = list(split_seq(files, multiplicity))
			print "Length of file list: ", len(filelists) #=nChunks

			# check if file already exists self.submitdir+"/joblist_"+key

			argfile = open(self.submitdir+"/joblist_"+key, "w")
			for filelist in filelists: 
				print len(filelist)
				self.createJob(argfile, filelist, self.outfolder, key, len(filelists))

			argfile.close()

	def SubmitJobs(self, dataset): 
		for key, files in dataset.items(): 
			if self.verbose and False: 
				print "Going to launch jobs for dataset: \n\nkey: {}\nfiles:{}".format(key, files)

			argfilename = self.submitdir+"joblist_"+key
			submitcommand = 'sbatch {} {}'.format(self.submitfilename, argfilename)
			# submitcommand = 'sbatch --array=1-{} {} {}'.format(self.submitfilename, argfilename)
			print "Gonna submit a job with: {}".format(submitcommand)

			#os.system(submitcommand)


	def createJob(self, argfile, filelist, outfolder, name, nchunks): 
		cmd = self.generateJobCommand(filelist, outfolder, name, nchunks)
		argfile.write(cmd)

	def generateJobCommand(self, filelist, outfolder, name, nchunks): 
		inputfiles = []
		for file in filelist: 
			inputfiles.append(self.xrdprefix+file)

		cmd = '%s %s %s %s %i \n'%(self.exename, ','.join(inputfiles), outfolder, name, nchunks)

		return cmd




class JobConfig: 
	def __init__(self, submitdir="./submit", multiplicity=1, force=False, verbose=True): # TODO: remove defaults here 
		self.submitdir = submitdir
		self.multiplicity = multiplicity
		self.force = force
		self.verbose = verbose


