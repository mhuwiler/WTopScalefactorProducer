import Dataset
import getGCDataset


if __name__ == "__main__":
   datasets = Dataset.getDataset("TT")
   for dataset in datasets:
	getGCDataset.main(dataset, "prod/global", "root://cms-xrd-global.cern.ch/", "./catalogue", "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8") 
 
