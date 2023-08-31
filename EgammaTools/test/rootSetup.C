{
  gStyle->SetOptStat(0);
  gSystem->Load("libCMSPODAS23EgammaTools.so");
  //suppressing noisy fits
  RooMsgService::instance().setGlobalKillBelow(RooFit::FATAL); 
  RooMsgService::instance().setSilentMode(true);
  gErrorIgnoreLevel = kError;
  
}
