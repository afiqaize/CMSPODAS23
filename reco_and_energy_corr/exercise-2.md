## Exercise 2.1
### Q1.1: Draw the distributions of the supercluster energy, seed cluster energy, and pin from GSF track<br>
Branch name: ``eleSCRawEn`` (Refined SC), ``eleSeedRawEn``, and ``eleGsfTrkPInn``<br>

Load library<br>
``root -l``<br>
``gSystem->Load("libCMSPODAS23EgammaTools.so")``<br>

Define tree<br>
we have files saved in ``/eos/user/y/yian/Ntuples_CMSPODAS/0000/`` and skimming files in ``/eos/user/y/yian/Ntuples_CMSPODAS/GGNtupSkimmed/``with all fakes removal<br>
``tree = HistFuncs::makeChain("ggNtuplizer/EventTree","/eos/user/y/yian/Ntuples_CMSPODAS/0000/*.root",10)``;<br>

Draw histograms<br>
``hist1 = HistFuncs::makeHist(tree,100,10,200,"eleSCRawEn","eleGenEn>10")``<br>
``hist2 = ...``<br>

### Q1.2: Use the variable ``eleSCRawEn`` to see the resolution distribution (divided by eleGenEn) in different η regions and fit it with different functions (functions ``makeDCBFit`` and ``makeCruijffFit``)<br>
``hist = HistFuncs::makeHist(tree,100,0,2,"eleSCRawEn/eleGenEn","eleGenEn>0 && eleGenEn>30 && eleGenEn<40 && abs(eleSCEta)<1.4442")``<br>
``ResFitter fitter;``<br>
``fitResDCB = fitter.makeDCBFit(hist,0.5,1.5)``<br>
``fitResDCB.plot->Draw()``<br>
``....``<br>
What do you observe? Why the mean value is not very close to 1?<br>

### Q1.3: Draw the occupancy plot of ``η`` and ``φ`` for electrons in ECAL<br>
``tree->Draw("eleSCPhi:eleSCEta:","eleSCRawEn/eleGenEn<0.9 && eleGenEn>20")``<br>
What does this occupancy plot mean?<br>



## Exercise 2.2

Open the notebook exercise-2.ipynb to see the regression effect from the simulation generating events by random seeds.

### Q2.1 Correct the ele_SCRawEn/ele_GenEn with the mean value got in the fit of Q1.2 and repeat the fit<br>
``histCorr = HistFuncs::makeHist(tree,100,0,2,"eleSCRawEn/eleGenEn/0.961","eleGenEn>0 && eleGenEn>30 && eleGenEn<40 && abs(eleSCEta)<1.4442")``<br>
``ResFitter fitter;``<br>
``fitResDCB = fitter.makeDCBFit(histCorr,0.5,1.5)``<br>
``fitResDCB.plot->Draw()``<br>
``....``<br>

### Q2.2 Draw distributions of ``eleSCRawEn``, ``eleSCEn``, ``eleEcalEn``, and ``ele_En``<br>
``hist = HistFuncs::compVars(tree,100,20,200,{"eleSCRawEn","eleSCEn"},"eleGenEn>20")``<br>
``....``<br>
Give explanations<br>

### Q2.3 When eleGenEn ranges from ``(10, 20)``, ``(20, 30)``, ``(30, 40)``, and ``(40, 50)``, fit the resolution distributions of ``eleSCEn/eleGenEn``, ``eleGsfTrkPInn/eleGenEn``, and ``eleEn/eleGenEn``<br>
``histCorr1 = HistFuncs::makeHist(tree,100,0,2,"eleSCEn/eleGenEn","eleGenEn>10 && eleGenEn<20 && abs(eleSCEta)<1.4442")``<br>
``ResFitter fitter;``<br>
``fitResDCB = fitter.makeDCBFit(histCorr1,0.5,1.5)``<br>
``fitResDCB.plot->Draw()``<br>
``histCorr2 = ...``<br>
``histCorr3 = ...``<br>
What do you observe from the variations of the resolution with ECAL or tracker?<br>

### Q2.4 Compare the Z mass distribution after the energy regression<br>
The $mass$ is the branch ``mass`` in the ntuple trees. We could use ntuple trees in ``/eos/cms/store/group/phys_egamma/CMSPOS2019/ntuples/GGMassNtup/dyJets_94X_massTreeV2.root`` and  the ID requirements could be applied as ``(ele1IDbit&0x4)!=0 && (ele2IDbit&0x4)!=0``, the histograms can be obtained as:<br>
``dy2017Tree = HistFuncs::makeChain("EventMassTree","/eos/cms/store/group/phys_egamma/CMSPOS2019/ntuples/GGMassNtup/dyJets_94X_massTreeV2.root");``<br>
``data2017Tree = ...``
``MCHist = HistFuncs::makeHist(dy2017Tree,100,50,120,"mass","(ele1IDbit&0x4)!=0 && (ele2IDbit&0x4)!=0 && ele1Pt>25 && ele2Pt>25")``<br>
``dataHist = ...``<br>
``mcHist->SetTitle(";m(ee) [GeV];#events")``<br>
``HistFuncs::compareDataMC(dataHist,mcHist,true)``<br>
What do you observe? Why is it?

## Exercise 2.3

### Q3.1 Draw the Z mass distribution after the residual energy correction<br>
$$mass_{corr} =mass \times \sqrt{\frac{ele1CaliEn}{ele1En}\times\frac{ele2CaliEn}{ele2En}}$$<br>
``hmass_corr = HistFuncs::makeHist(tree,100,50,120,"mass*sqrt(ele1CalibEn/ele1En*ele2CalibEn/ele2En)","(ele1IDbit&0x4)!=0 && (ele2IDbit&0x4)!=0 && ele1Pt>25 && ele2Pt>25")``<br>
