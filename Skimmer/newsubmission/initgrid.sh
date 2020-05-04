export X509_USER_PROXY=${HOME}/private/x509_voms
voms-proxy-init  --voms cms --valid 200:00:00
export PATH=$PATH:$CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/grid-control:$CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/grid-control/scripts
