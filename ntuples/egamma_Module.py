import os, sys
import math
import ROOT
from math import sin, cos, sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

_rootLeafType2rootBranchType = {
    'UChar_t': 'b',
    'Char_t': 'B',
    'UInt_t': 'i',
    'Int_t': 'I',
    'Float_t': 'F',
    'Double_t': 'D',
    'ULong64_t': 'l',
    'Long64_t': 'L',
    'Bool_t': 'O'
}

class egamma_Producer(Module):
    def __init__(self,isdata=False):
        self.isdata=isdata
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

#        branches = ['pt','eta','phi','charge',
#                    'cutBased','SigmaIEtaIEtaFull5x5','dEtaSeedAtVtx',
#                    'dPhiAtVtx','HoverE','PFChIso','PFNeuIso',
#                    'PFPhoIso','EoverP','MissHits','r9',
#                    'SCRawEn','SeedRawEn','SeedRawEn',
#                    'SCEn','EcalEn','En','CalibEn',
#		    'GsfTrkPInn','GsfTrkPOut',
#                    'GenEn','GenPt','GenEta','GenPhi']


       # Find list of activated branches in input tree
        _brlist_in = inputTree.GetListOfBranches()
        branches_in = set(
            [_brlist_in.At(i) for i in range(_brlist_in.GetEntries())])
        branches_in = [
            x for x in branches_in if inputTree.GetBranchStatus(x.GetName())
        ]
        # Find list of activated branches in output tree
        _brlist_out = wrappedOutputTree._tree.GetListOfBranches()
        branches_out = set(
            [_brlist_out.At(i) for i in range(_brlist_out.GetEntries())])
        branches_out = [
            x for x in branches_out
            if wrappedOutputTree._tree.GetBranchStatus(x.GetName())]
        # Use both
        branches = branches_in + branches_out
        self.isdata = not bool(inputTree.GetBranch("nGenPart"))

        # Only keep branches with right collection name
        self.brlist_ele, self.branchType_ele = self.filterBranchNames(branches, 'Electron')

        # Create output branches
        self.out = wrappedOutputTree

        # electron
        for br in self.brlist_ele:
            self.out.branch("%s_%s" % ('ele', br),
                            _rootLeafType2rootBranchType[self.branchType_ele[br]],
                            lenVar="nele")
        self.out.branch('gen_weight','F')
        self.out.branch('mass','F')
        if not self.isdata:
            self.out.branch("ele_is_prompt", "O", lenVar="nele")
        self.out.branch('eleGen_mass','F',lenVar="nele")
        self.out.branch('eleGen_pt','F',lenVar="nele")
        self.out.branch('eleGen_eta','F',lenVar="nele")
        self.out.branch('eleGen_phi','F',lenVar="nele")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
	pass

    def filterBranchNames(self, branches, collection):
        out = []
        branchType = {}
        for br in branches:
            name = br.GetName()
            if not name.startswith(collection + '_'):
                continue
            out.append(name.replace(collection + '_', ''))
            branchType[out[-1]] = br.FindLeaf(br.GetName()).GetTypeName()
        return out, branchType

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)
        else:    
            self.out.fillBranch("gen_weight",0)

        electrons = Collection(event, "Electron")
	if hasattr(event, 'nGenPart'):
           genparts = Collection(event, "GenPart")

	electrons_select = []
	electron_pass=0
        for i,lep in enumerate(electrons):
            if electrons[i].pt < 10:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
		electrons_select.append(lep)
                electron_pass += 1

        if len(electrons_select)<1:
           return False
       
        for i in self.brlist_ele:
            self.out.fillBranch('ele_' + i, [iobj[i] for iobj in electrons_select])
 
        if electron_pass>1:
           self.out.fillBranch('mass', (electrons_select[0].p4()+electrons_select[1].p4()).M())
        else:
           self.out.fillBranch('mass', 0)


        isprompt_mask = (1 << 0) #isPrompt used for lepton
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct used for lepton
        
	ele_is_real = []
        genElectrons_select = []
        for j, lep in enumerate(electrons_select):
            is_real_flag = False
            if hasattr(event, 'nGenPart'):
                for i in range(0,len(genparts)):
		   if genparts[i].pt > 5 and abs(genparts[i].pdgId) == abs(lep.pdgId) and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(lep.eta,lep.phi,genparts[i].eta,genparts[i].phi) < 0.3:
	               is_real_flag = True
                       genElectrons_select.append(genparts[i])
                       break 
	        ele_is_real.append(is_real_flag)
            else:
		ele_is_real = [False] * len(electrons_select)
         
        self.out.fillBranch("ele_is_prompt", ele_is_real)

        for i in ['mass','pt','eta','phi']:
            self.out.fillBranch('eleGen_' + i, [iobj[i] for iobj in genElectrons_select])

        return True

egamma_Module = lambda: egamma_Producer()
