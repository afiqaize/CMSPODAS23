## Exercise 2.1
### Q1.1: Draw the distributions of the supercluster energy, seed cluster energy, and pin from GSF track<br>
Branch name: ``ele_SCRawEn`` (Refined SC), ``ele_SeedRawEn``, and ``ele_GsdTrkPInn``<br>

Load library<br>
``root -l``<br>
``gSystem->Load("libCMSPODAS23EgammaTools.so")``<br>

Define tree<br>
``treeMC = HistFuncs::makeChain("Events","dir/+name*.root",10)``;<br>

Draw histograms<br>
``hist1 = HistFuncs::makeHist(treeMC,100,0,1,"ele_SCRaw","ele_is_promt==1 && ele_pt>20")``<br>
``hist2 = ...``<br>

### Q1.2: Use the variable ``ele_SCRawEn`` to see the resolution distribution (divided by eleGen_pt) in different η regions and fit it with different functions (functions ``makeDCBFit`` and ``makeCruijffFit``)<br>
``hist = HistFuncs::makeHist(treeMC,100,0,1,"ele_SCRaw/eleGen_Pt","ele_is_promt==1 && ele_pt>20")``<br>
``ResFitter fitter;``<br>
``fitResDCB = fitter.makeDCBFit(hist,0.5,1.5)``<br>
``fitResDCB.plot->Draw()``<br>
``....``<br>
What do you observe? Why the mean value is not very close to 1?<br>

### Q1.3: Draw the occupancy plot of ``η`` and ``φ`` for electrons in ECAL<br>
``tree->Draw("ele_phi:ele_eta:","ele_SCRawEn/eleGen_pt<0.9 && ele_is_prompt==1 && eleGen_pt>20")``<br>
What does this occupancy plot mean?<br>



## Exercise 2.2

Open the notebook exercise-2.ipynb to see the regression effect from the simulation generating events by random seeds.

### Q2.1 Correct the ele_SCRawEn/ele_GenEn with the mean value got in the fit of Q1.2 and repeat the fit<br>
``histCorr = HistFuncs::makeHist(tree,100,0,2,"eleSCRawEn/eleGen_pt/0.961","ele_is_promt==1 && ele_pt>20")``<br>
``ResFitter fitter;``<br>
``fitResDCB = fitter.makeDCBFit(histCorr,0.5,1.5)``<br>
``fitResDCB.plot->Draw()``<br>
``....``<br>

### Q2.2 Draw distributions of ``ele_SCRawEn``, ``ele_SCEn``, ``ele_EcalEn``, and ``ele_En``<br>
``hist = HistFuncs::compVars(events,100,20,200,{"ele_SCRawEn","ele_SCEn"},"ele_is_promt==1 && ele_pt>20")``<br>
``....``<br>
Give explanations<br>

### Q2.3 When eleGen_pt ranges from ``(10, 20)``, ``(20, 30)``, ``(30, 40)``, and ``(40, 50)``, fit the resolution distributions of ``ele_SCEn/eleGen_pt``, ``ele_GsdTrkPInn/eleGen_pt``, and ``ele_En/eleGen_pt``<br>
``histCorr1 = HistFuncs::makeHist(tree,100,0,2,"eleSCEn/eleGen_pt","ele_is_promt==1 && eleGen_pt>10 && eleGen_pt<20")``<br>
``ResFitter fitter;``<br>
``fitResDCB = fitter.makeDCBFit(histCorr1,0.5,1.5)``<br>
``fitResDCB.plot->Draw()``<br>
``histCorr2 = ...``<br>
``histCorr3 = ...``<br>
What do you observe from the variations of the resolution with ECAL or tracker?<br>

### Q2.4 Compare the Z mass distribution after the energy regression<br>
The mass without residual correction is not saved but could be derived from the equation:<br>
$$mass_{corr} =mass \times \sqrt{\frac{ele1CaliEn}{ele1En}\times\frac{ele2CaliEn}{ele2En}}$$<br>
$$mass =\frac{mass_{corr}}{\sqrt{\frac{ele1CaliEn}{ele1En}\times\frac{ele2CaliEn}{ele2En}}}$$<br>
The $mass_{corr}$ is the branch ``mass`` in our ntuple trees<br>
``hmass = HistFuncs::makeHist(tree,100,50,120,"mass/sqrt(ele_CaliEn[0]/ele_En[0]*ele_CaliEn[1]/ele_En[1])","ele_is_promt[0]==1 && ele_is_promt[1]==1 && nele>1")``<br>
What do you observe? Why is it?

## Exercise 2.3

### Q3.1 Draw the Z mass distribution after the residual energy correction<br>
``hmass_corr = HistFuncs::makeHist(tree,100,50,120,"mass","ele_is_promt[0]==1 && ele_is_promt[1]==1 && nele>1")``<br>
