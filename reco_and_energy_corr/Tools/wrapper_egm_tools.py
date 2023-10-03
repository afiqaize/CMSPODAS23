import os
import cppyy
import uproot

egm_tools_base = f'{os.path.dirname(os.path.abspath(__file__))}/../../EgammaTools'
cppyy.add_include_path(f'{egm_tools_base}/interface/')

for src in ['CruijffPdf.cc', 'EGUtilFuncs.cc', 'GBRMath.cc', 'HistFuncs.cc', 'MassNtupConverter.cc', 'ResFitter.cc', 'RooDoubleCBFast.cc']:
    with open(f'{egm_tools_base}/src/{src}') as sfile:
        cppyy.cppdef(sfile.read())

from ROOT import TCanvas
from cppyy.gbl import ResFitter
from cppyy.gbl.std import vector

class NotebookHistogram(object):
    canvas = None
    fitter = None

    def __init__(self, histogram):
        self.histogram = histogram
        self.uproot = None

    def make_canvas(self, fn):
        def fn_using_canvas(self, *args, **kwargs):
            if self.__class__.canvas is None:
                self.__class__.canvas = TCanvas()
            return fn(self, *args, **kwargs)
        return fn_using_canvas

    @make_canvas
    def draw(self, option = None):
        self.__class__.canvas.cd()
        self.histogram.Draw()
        self.__class__.canvas.Draw()

    def make_uproot(self, fn):
        def fn_using_uproot(self, *args, **kwargs):
            if self.uproot is None:
                self.uproot = uproot.pyrootfrom_pyroot(self..histogram)
            return fn(self, *args, **kwargs)
        return fn_using_uproot

    @make_uproot
    def axis(self, *args, **kwargs):
        return self.uproot.axis(*args, **kwargs)

    @make_uproot
    def counts(self, *args, **kwargs):
        return self.uproot.counts(*args, **kwargs)

    @make_uproot
    def errors(self, *args, **kwargs):
        return self.uproot.errors(*args, **kwargs)

    @classmethod
    def reset(cls, x):
        del cls.canvas
        cls.canvas = None
        del cls.fitter
        cls.fitter = None

def makeChain(cname, flist, njob = 1, ijob = 1, verbose = 2):
    return cppyy.gbl.HistFuncs.makeChain(cname, flist, njob, ijob, verbose)

def makeHist(tree, nbin, xmin, xmax, variable, cut):
    return NotebookHistogram(cppyy.gbl.HistFuncs.makeHist(tree, nbin, xmin, xmax, variable, cut))

def compVars(tree, nbin, xmin, xmax, variables, cut):
    return NotebookHistogram(cppyy.gbl.HistFuncs.compVars(tree, nbin, xmin, xmax, vector[str](variables), cut))

def compareDataMC(h_data, h_mc, normalize):
    return NotebookHistogram(cppyy.gbl.HistFuncs.compareDataMC(h_data.histogram, h_mc.histogram, normalize))
