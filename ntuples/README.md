# CMSPODAS23
### environment and package set up
``cmsrel CMSSW_10_6_29``<br>
``cd CMSSW_10_6_29/src``<br>
``cmsenv``<br>
``git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools``<br>
``git clone https://github.com/AnYpku/CMSPODAS23.git``<br>
``scram b``<br>
``cd -``<br>
``cd ntuples/``<br>
Set Grid Certificate<br>
``python run_egamma_producer.py -f root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/100000/13D0AD97-6B32-CB4C-BA87-5E37BA4CF20E.root -y 2018 -init 0 -n 1000``<br>
Check the output file<br>
