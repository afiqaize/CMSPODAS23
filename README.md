# CMSPODAS23
This repo is for the EGamma long-exercise of the CMS Physics object & data analysis school [CMSPODAS2023](https://indico.desy.de/event/38207). The exercise focuses on:
### Produce ntuples
Based on the [NANOAOD framework](https://github.com/cms-nanoAOD/nanoAOD-tools.git). CMSSW environment and packages should be set up firstly as follows:<br>

``cmsrel CMSSW_10_6_29``<br>
``cd CMSSW_10_6_29/src``<br>
``cmsenv``<br>
``git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools``<br>
``git clone https://github.com/AnYpku/CMSPODAS23.git``<br>
``scram b``<br>
``cd ntuples``<br>

Ntuple tree contains electron branches could be produced by running:<br>
``python run_egamma_producer.py -f filename -y year``<br>

In order to realize the energy change step by step, the energy branches in the intermediate state are also saved.
### Energy calibration
A brief introduction and exercise in ``reco_and_energy_corr/exercise-1.ipynb``<br>

### Reconstruction
A detailed introduction in slides

### Energy regression and correction
Using the ntuple tree produced in the first step, we could draw some histograms to do comparisons and fitting.<br>
Some functions are prepared in the ``EGammaTools/`` and can call via:<br>

``root -l``<br>
``gSystem->Load("libCMSPODAS23EgammaTools.so")``<br>

Functions we may need and the usages are:<br>
1. Compare the prompt and nonprompt electron distributions:<br> ``hist = HistFuncs::compSigBkg(sigTree,bkgTree,nbins,low,high,"branchName","common selection","sig selection","bkg selection",normlization flag)``<br>
2. Make histograms:<br> ``hist = HistFuncs::makeHist(tree,nbins,low,high,"branchName","selection")``
3. Fit functions containing ``makeDCBFit``, ``makeCBFit``, and ``makeCruijffFit`` could call via:<br>
``ResFitter fitter;``<br>``fit = fitter.makeDCBFit(hist,0.5,1.5);``<br>``fit.plot->Draw()`` (if necessary)<br>

Exercises in ``reco_and_energy_corr/exercise-2.ipynb`` and ``reco_and_energy_corr/exercise-2.md`` (run exercise-2.md in the root command line environment through terminal)<br>

### Identification
A brief introduction in slides and Jupyternotebook<br>
Exercises in ``egamma_id/exercise-3.ipynb``<br>

### Tag& Probe method
A brief introduction in slides and Jupyternotebook<br>
Exercise in ``Tnp/exercise-4.ipynb``<br>

### MVA ID training
A brief introduction in slides and Jupyternotebook<br>
Exercise in ``MVA/exercise-5.ipynb``<br>
