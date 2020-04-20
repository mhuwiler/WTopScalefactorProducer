#!/Usr-/bin/env python
import os,sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from WTopScalefactorProducer.Skimmer.skimmer import Skimmer
if len(sys.argv)<2:
  sys.stderr.write("ERROR: There are too few arguments. The script needs the following arguments: 1. output directory, 2. list of source files") 

outputDir = os.path.expandvars(sys.argv[1]) #outputDir = os.path.expandvars("$GC_SCRATCH")

infile = sys.argv[2].split(' ')


print "argv: ", sys.argv

print "infile: ", infile

print "outputDir: ", outputDir

# HLT_Mu50&&nMuon>0&&Muon_pt[0]>55.&&Muon_pfRelIso03_chg[0]<0.15&&Muon_highPtId>1&&nFatJet>0&&FatJet_pt>200

jsonfile=os.path.expandvars('$CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/python/JSON/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt')

if infile[0].find("SingleMuon")!=-1:
  channel = "mu"
  print "Processing a Single Muon dataset file..."
  p=PostProcessor(outputDir, infile, None, None, #"HLT_Mu50 && nMuon>0 && Muon_pt[0]>55. && nFatJet>0"
                    modules=[Skimmer(channel),],provenance=False,fwkJobReport=False,  
                    jsonInput=jsonfile,
                    )

elif infile[0].find("EGamma")!=-1:
  channel = "el"
  print "Processing a Single Electron dataset file..."
  p=PostProcessor(outputDir, infile, None, None, #"(event.HLT_Ele32_WPTight_Gsf || event.HLT_Ele35_WPTight_Gsf || event.HLT_Ele40_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT) && nElectron>0 && Electron_pt[0]>55. && nFatJet>0"
                    modules=[Skimmer(channel)],provenance=False,fwkJobReport=False,  
                    jsonInput=jsonfile,
                    )

else:
  print "Processing MC dataset files..."
  channel = "elmu"
  p=PostProcessor(outputDir, infile, None, None,
                    modules=[Skimmer(channel)],provenance=False,fwkJobReport=False,  
                    #jsonInput=jsonfile,
)
p.run()
print "DONE"
