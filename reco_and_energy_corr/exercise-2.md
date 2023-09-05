### Q1: Draw the distributions of the supercluster energy, seed cluster energy, and pin from GSF track<br>
Branch name: ``ele_SCRawEn`` (Refined SC), ``ele_SeedRawEn``, and ``ele_GsdTrkPInn``<br>
Load library<br>
``root -l``<br>
``gSystem->Load("libCMSPODAS23EgammaTools.so")``<br>

Define tree<br>
``treeMC = HistFuncs::makeChain("Events","dir/+name*.root",10)``;<br>

Draw histograms<br>
``hist1 = HistFuncs::makeHist(treeMC,100,0,1,"ele_SCRaw","ele_is_promt==1 && ele_pt>20")``<br>
``hist2 = ...``<br>

### Q2: Use the variable ``ele_SCRawEn`` to see the resolution distribution (divided by eleGen_pt) in different η regions and fit it with different functions (functions ``makeDCBFit`` and ``makeCruijffFit``)<br>
``hist = HistFuncs::makeHist(treeMC,100,0,1,"ele_SCRaw/eleGen_Pt","ele_is_promt==1 && ele_pt>20")``<br>
``ResFitter fitter;``<br>
``fitResDCB = fitter.makeDCBFit(hist,0.5,1.5)``<br>
``fitResDCB.plot->Draw()``<br>
``....``<br>
What do you observe? Why the mean value is not very close to 1?<br>

### Q3: Draw the occupancy plot of η and φ for electrons in ECAL<br>
``tree->Draw("ele_phi:ele_eta:","ele_SCRawEn/eleGen_pt<0.9 && ele_is_prompt==1 && eleGen_pt>20")``
What does this occupancy plot mean?

