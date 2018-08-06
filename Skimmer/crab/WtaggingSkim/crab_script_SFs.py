#!/Usr-/bin/env python
import os,sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#from PhysicsTools.NanoAODTools.WTopScalefactorProducer.Skimmer.TTSkimmer import *
from TTSkimmer_New import * 

# NOTE : This file is configured to Process MC.
# If you want to process Data then ADD "jsonInput='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'"
# to the PostProcessor arguement below

# p=PostProcessor(".", inputFiles(),                                                                                          # --> to submit with crab, use this
# p=PostProcessor(".", inputFiles(),
#                  "nFatJet>0&&FatJet_msoftdrop>30&&FatJet_pt>200&&MET_sumEt>40&& ( (nElectron > 0 && HLT_Ele115_CaloIdVT_GsfTrkIdT) || (nMuon > 0 && HLT_Mu50))" ,"keep_and_drop.txt",
#                   modules=[TTbar_SemiLep()],provenance=True,fwkJobReport=True
#                   ,haddFileName=  '94XNanoV0-TTbar_SemiLep.root'  )

inputFiless = [
#'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims//nanoskim-JetsandLepton-SingleMuon17B-trees.root'
#'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsandLepton-Data-SingleElectron_2017B-trees.root'
#'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsAndLepton-94XMC-STtWtop5finclusiveDecaysTuneCP513TeV-powheg-pythia-trees.root'
#'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsAndLepton-94XMC-STtWantitop5finclusiveDecaysTuneCP513TeV-powheg-pythia8-trees.root'
#'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsAndLepton-94XMC-WJetsToLNuTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer17-trees.root'
'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsAndLepton-94XMC-W4JetsToLNuTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer17-trees.root'
#'root://cmseos.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsandLepton-94XMC-TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8-trees.root'
#'root://cmseos.fnal.gov//store/user/asparker/CRAB_UserFiles/nanoskim-JetsAndLepton-94XMC-TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_RunIIFall17/180605_122319/0000/nanoskim-trees_99.root'
]

p=PostProcessor(".", inputFiless,
                 "nFatJet>0&&FatJet_msoftdrop>30&&FatJet_pt>200&&MET_sumEt>40&&( (nElectron>0) ||(nMuon>0&&HLT_Mu50) )" ,"keep_and_drop.txt",
                  modules=[TTbar_SemiLep()],provenance=True,fwkJobReport=True 
                  ,haddFileName=  'WtaggingSkim_94XMC-W4JetsToLNuTuneCUETP8M1MadgraphMLMPythia_noEleTrigger_Aug6.root'  )

# (nMuon>0&&HLT_Mu50) ||(nElectron>0&&HLT_Ele115_CaloIdVT_GsfTrkIdT)
p.run()

print "DONE"
