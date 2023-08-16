#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from egamma_Module import *

import argparse
import re
import optparse

parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='infile', default='', help='local file input')
parser.add_argument('-y', dest='year', default='2018', help='year of dataset')
parser.add_argument('-d', dest='isdata',action='store_true',default=False)
parser.add_argument('-n', dest='maxEntries',help='max entries to process',type = int, default=None)
parser.add_argument('-init', dest='firstEntry',help='first entry to process',type = int, default=0)
args = parser.parse_args()

print "year: ", args.year
print "dataset_name: ", args.infile

if args.infile:
   infilelist = [args.infile]
   jsoninput = None
else:
   from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
   infilelist = inputFiles()
   jsoninput = runsAndLumis() 

Modules = [countHistogramsModule(),egamma_Module()] 


if not args.isdata:
   Modules.append({'2016':puWeight_UL2016 , '2017':puWeight_UL2017 , '2018':puWeight_UL2018}[args.year]())

p=PostProcessor(".",infilelist,
                branchsel="egamma_keep_and_drop.txt",
                modules = Modules,
                provenance=True,
                justcount=False,
                noOut=False,
                fwkJobReport=False, 
                jsonInput=jsoninput, 
                outputbranchsel = "egamma_output_branch.txt",
                maxEntries=args.maxEntries,
                firstEntry=args.firstEntry)
p.run()

