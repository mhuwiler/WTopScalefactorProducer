#!/bin/bash


export FILE_NAMES="root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19_ext1-v1/40000/78A348A5-D9AD-CB44-9F60-651F7A9E48ED.root root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19_ext1-v1/40000/99F5AF3E-4C47-C84A-AA2F-BA32359476EF.root"
export GC_SCRATCH="./LOCALTEST"

export GC_TASK_ID="Testjob"

export DATASETPATH="DatasetName"

export GC_JOB_ID="10"

./executable.sh

