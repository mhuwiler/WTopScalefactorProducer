import ROOT

import imp
import ssl
import subprocess
import os

import json
import yaml
import copy

import argparse



def queryGOClient(querytype, datatype, name, dbs_instance, json = False):
    query = querytype+" "+datatype+"="+name+" instance="+dbs_instance
    cmd = 'dasgoclient -query="%s"' % query
    if json:
       cmd += " -json" 
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    a = proc.communicate()
    return a[0]

def makeOutput(lines, output, datasetname):
    if not os.path.exists(output):
        os.makedirs(output)
        
    with open(output+"/"+datasetname+".txt", "w") as f:
        f.write("["+datasetname+"]\n")
        for line in lines:
            f.write(line+"\n") 

def main(DASName, dbs, prefix, output, overwritename=None):
    
    datasetfiles = queryGOClient("file", "dataset", DASName, dbs, json=True)
    datasetfiles = datasetfiles.replace("[\n","")
    datasetfiles = datasetfiles.replace("\n]\n","")

    allJSONs = []
    for j in datasetfiles.split(" ,"):
        allJSONs.append(json.loads(j))


    outputLines = []
    for j in allJSONs:
        outputLines.append(prefix+str(j["file"][0]["name"])+" = "+str(j["file"][0]["nevents"]))

    datasetname = DASName.split("/")[1] if overwritename is None else overwritename

    makeOutput(outputLines, output, datasetname) 
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="collect crab_nano output and make dataset .txt files")
    parser.add_argument("--name" , required=True, help="DAS dataset name", type=str)
    parser.add_argument("--outpath", default=".", help="path to store dataset .txt files", type=str)
    parser.add_argument("--prefix", default="root://cms-xrd-global.cern.ch/", help="server prefix to add to rootfiles", type=str)
    parser.add_argument("--dbs",action = "store", help = "DAS dbs for the query",type=str,required = False, default = "prod/global")
    parser.add_argument("--DSName", action="store", help="Passed variable will be used as file and dataset name. Otherwise DAS name will be used",default=None)
    args = parser.parse_args()

 
    main(args.name, args.dbs, args.prefix, args.outpath, args.DSName)

    
    
