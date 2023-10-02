import os
import cppyy

egm_tools_base = f'{os.path.dirname(os.path.abspath(__file__))}/../../EgammaTools'
cppyy.add_include_path(f'{egm_tools_base}/interface/')

for src in ['CruijffPdf.cc', 'EGUtilFuncs.cc', 'GBRMath.cc', 'HistFuncs.cc', 'MassNtupConverter.cc', 'ResFitter.cc', 'RooDoubleCBFast.cc']:
    with open(f'{egm_tools_base}/src/{src}') as sfile:
        cppyy.cppdef(sfile.read())

from cppyy.gbl import ResFitter
from cppyy.gbl.std import vector

def makeChain(cname, flist, njob = 1, ijob = 1, verbose = 2):
    return cppyy.gbl.HistFuncs.makeChain(cname, flist, njob, ijob, verbose)

def makeHist(tree, nbin, xmin, xmax, variable, cut):
    result = cppyy.gbl.HistFuncs.makeHist(tree, nbin, xmin, xmax, variable, cut)
    return [result, np.linspace(xmin, xmax, int(nbin + 1))]

def compVars(tree, nbin, xmin, xmax, variables, cut):
    result = cppyy.gbl.HistFuncs.compVars(tree, nbin, xmin, xmax, vector[str](variables), cut)
    return [result, np.linspace(xmin, xmax, int(nbin + 1))]

def compareDataMC(h_data, h_mc, normalize):
    return cppyy.gbl.HistFuncs.compareDataMC(h_data, h_mc, normalize)
