#!/usr/bin/env python
#Dropped refs/stash@{0} (d0d28954d86639cc5dfc0eb8ac4716f46c8e86ae)

import os 
from DASTools import *
#from __future__ import division, print_function
import json
from JobBackend import *


class JobSubmissionEngine: 
	def __init__(self, args, dataset, catalogue="fileLists_NewSubmission"): 

		# why not do: self.args = args
		self.verbose = args.verbose
		self.dataset = dataset

		if (args.createlist): 
			self.MakeLocalCatalogue(catalogue, self.dataset)
			# Check if list has already been created and ask for confirmation in case of overwrite 
			print "Creating list of files " 
			# launch the list creation 

		# Setting the arguments as class attributes 
		self.output = ""
		if args.output:
			self.output = args.output
		self.dry = args.dry
		self.force = args.force
		self.gridengine = args.gridengine
		self.jobconfigfilename = args.jobfilename
		self.multiplicity = args.multiplicity
		#self.datasets = getDataset(args.dataset)
	
		# Printing the configuration 
		if self.verbose: 
			print "Created a JobSubmissionEngine class with following configuration: "
			if self.dry: 
				print "  Running in dry mode." 
			print "  Grid engine: {}".format(args.gridengine)	
			print "  Output location: {}".format(self.output)
			print "  Dataset: {}".format(self.dataset)

		self.cataloguepath=""
		self.cataloguedone=False

		# Here starts the job submission part 

		jobconfig = JobConfig() #JobConfig(self.submitdir, self.multiplicity, self.force, self.verbose)
		if args.gridengine == "HTCondor": 
			self.jobengine = HTCondorBackend(jobconfig)
		elif args.gridengine == "Slurm": 
			self.jobengine = SlurmBackend(jobconfig)
		else: 
			print "Error: The job engine backend specified is not supported: {}\nPlease specify one of the following: ('HTCondor', 'Slurm')!".format(self.gridengine)
			exit(0)

		self.PrepareJobs(catalogue, self.jobconfigfilename)

		#self.jobengine.WriteJobConfig(0)


	def MakeLocalCatalogue(self, dir, patterns): 

		if (os.path.isdir(dir)): 	# TODO: implememnt effect of parameter -f 
			response = raw_input( "\nWarning, the file catalogue '{}' already exists, do you want to recreate (overwrite!) it? (y/n): ".format(dir) )
			if response != "y" : 
				print "\nExiting, catalogue in '{}' will not be updated! ".format(dir) 
				exit(0)
		else: 
			os.mkdir(dir)

		print "\nCreating file catalogue... \n" 
		for pattern in patterns:
			#print pattern
			createLists(dir, pattern)
		print "\nFile catalogue written to: {}\n".format(dir)

	def PrepareJobs(self, catalogue, jobfilename,): 
		# try accessing the catalogue 
		dataset = self.getFileList(catalogue)

		self.jobengine.PrepareJobs(dataset, self.multiplicity)

		




	def getFileList(self, catalogue): 
		if (not os.path.isdir(catalogue)): 
			response = raw_input( "\nCatalogue '{}' does not exist, do you want to create it from DAS (requires active proxy)? (y/n): ".format(catalogue) )
			if (response != "y"): 
				print "\nExiting, no catalogue... " 
				exit(0)
			else: 
				self.MakeLocalCatalogue(catalogue, self.dataset)
		else:
			# catalogue exists 
			print "Catalogue exists! "
		
		dataset = openCatalogue(catalogue)
		#print dataset

		return dataset
		






