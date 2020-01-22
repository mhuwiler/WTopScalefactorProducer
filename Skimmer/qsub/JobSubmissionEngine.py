#!/usr/bin/env python

import os 
from DASTools import *


class JobSubmissionEngine: 
	def __init__(self, args, dataset, catalogue="fileLists_NewSubmission"): 

		self.verbose = args.verbose
		self.dataset = dataset

		if (args.createlist): 
			self.MakeLocalCatalogue(catalogue, self.dataset)
			# Check if list has already been created and ask for confirmation in case of overwrite 
			print "Creating list of files " 
			# launch the list creation 

		# Setting thee arguments as class attributes 
		self.output = ""
		if args.output:
			self.output = args.output
		self.dry = args.dry
		self.gridengine = args.gridengine
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

	def MakeLocalCatalogue(self, dir, patterns): 

		if (os.path.isdir(dir)): 
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
		
