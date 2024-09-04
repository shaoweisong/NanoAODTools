import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class METFilters(Module):
    def __init__(self,year):
        self.year = year
        self.passMETFilters = 0
        pass
    def beginJob(self):
        print("{:27}:{:7} {}".format("PassMETFilters: ", str(self.passMETFilters), " Events"))
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #self.out.branch("EventMass",  "F");
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """nanoAOD skimming is done considering the final events selection
        for the vv semileptonic final state.

        For the vv semileptonic final state we should be either one or two
        tight leptons, either one Fat jet and two small radius jet or four
        small radius jets.

        Arguments:
            event {instance of event} -- instance of event

        Returns:
            boolean -- if the event passes skimming then it returns true and
                       go to the next module else returns false and go to
                       the next event.
        """

        keepIt = True

        if passFilters(event, int(self.year)):
            self.passMETFilters += 1
        else:
            return keepIt


        return keepIt


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
METFilterModule = lambda : METFilters() #(jetSelection= lambda j : j.pt > 30)

METFilter_UL16PreVFP = lambda: METFilters(2016)
METFilter_UL16PostVFP = lambda: METFilters(2016)
METFilters_UL2017 = lambda: METFilters(2017)
METFilter_UL2018 = lambda: METFilters(2018)
def passFilters(event, year, debug=False):
    # Referece: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#2018_2017_data_and_MC_UL
    if year == 2017 or year == 2018:
        # For 2017 and 2018
        if event.Flag_goodVertices == 0:
            return False
        if debug: print("DEBUG: Flag_goodVertices passed")
        if event.Flag_globalSuperTightHalo2016Filter == 0:
            return False
        if debug: print("DEBUG: Flag_globalSuperTightHalo2016Filter passed")
        if event.Flag_HBHENoiseFilter == 0:
            return False
        if debug: print("DEBUG: Flag_HBHENoiseFilter passed")
        if event.Flag_HBHENoiseIsoFilter == 0:
            return False
        if debug: print("DEBUG: Flag_HBHENoiseIsoFilter passed")
        if event.Flag_EcalDeadCellTriggerPrimitiveFilter == 0:
            return False
        if debug: print("DEBUG: Flag_EcalDeadCellTriggerPrimitiveFilter passed")
        if event.Flag_BadPFMuonFilter == 0:
            return False
        if debug: print("DEBUG: Flag_BadPFMuonFilter passed")
        if event.Flag_BadPFMuonDzFilter == 0:
            return False
        if debug: print("DEBUG: Flag_BadPFMuonDzFilter passed")
        if event.Flag_hfNoisyHitsFilter == 0:
            return False
        if debug: print("DEBUG: Flag_hfNoisyHitsFilter passed")
        if event.Flag_BadChargedCandidateFilter == 0:
            return False
        if debug: print("DEBUG: Flag_BadChargedCandidateFilter passed")
        if event.Flag_eeBadScFilter == 0:
            return False
        if debug: print("DEBUG: Flag_eeBadScFilter passed")
        if event.Flag_ecalBadCalibFilter == 0:
            return False
        if debug: print("DEBUG: Flag_ecalBadCalibFilter passed")
        return True
    elif year == 2016 or year == "2016preVFP" or year == "2016postVFP":
        # For 2016
        if event.Flag_goodVertices == 0:
            return False
        if debug: print("DEBUG: Flag_goodVertices passed")
        if event.Flag_globalSuperTightHalo2016Filter == 0:
            return False
        if debug: print("DEBUG: Flag_globalSuperTightHalo2016Filter passed")
        if event.Flag_HBHENoiseFilter == 0:
            return False
        if debug: print("DEBUG: Flag_HBHENoiseFilter passed")
        if event.Flag_HBHENoiseIsoFilter == 0:
            return False
        if debug: print("DEBUG: Flag_HBHENoiseIsoFilter passed")
        if event.Flag_EcalDeadCellTriggerPrimitiveFilter == 0:
            return False
        if debug: print("DEBUG: Flag_EcalDeadCellTriggerPrimitiveFilter passed")
        if event.Flag_BadPFMuonFilter == 0:
            return False
        if debug: print("DEBUG: Flag_BadPFMuonFilter passed")
        if event.Flag_BadPFMuonDzFilter == 0:
            return False
        if debug: print("DEBUG: Flag_BadPFMuonDzFilter passed")
        if event.Flag_BadChargedCandidateFilter == 0:
            return False
        if debug: print("DEBUG: Flag_BadChargedCandidateFilter passed")
        if event.Flag_eeBadScFilter == 0:
            return False
        if debug: print("DEBUG: Flag_eeBadScFilter passed")
        if event.Flag_hfNoisyHitsFilter == 0:
            return False
        if debug: print("DEBUG: Flag_hfNoisyHitsFilter passed")
        return True
    else:
        print("ERROR: Invalid year: {}".format(year))
        exit(1)