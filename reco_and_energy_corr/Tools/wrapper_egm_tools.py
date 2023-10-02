import cppyy

egm_tools_base = '../../EgammaTools'
cppyy.add_include_path(f'{egm_tools_base}/interface/')

for src in ['CruijffPdf.cc', 'EGUtilFuncs.cc', 'GBRMath.cc', 'HistFuncs.cc', 'MassNtupConverter.cc', 'ResFitter.cc', 'RooDoubleCBFast.cc']:
    with open(f'{egm_tools_base}/src/{src}') as sfile:
        cppyy.cppdef(sfile.read())

from cppyy.gbl import ResFitter
makeChain = cppyy.gbl.HistFuncs.makeChain 
makeHist = cppyy.gbl.HistFuncs.makeHist 
compVars = cppyy.gbl.HistFuncs.compVars
compareDataMC = cppyy.gbl.HistFuncs.compareDataMC
