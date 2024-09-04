#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.common.ggTemporaryScale import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.METFilters import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.LHEScaleWeightProducer import LHEScaleWeightProducer

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
import sys
JobNumber = sys.argv[1]
Jobyear = sys.argv[2]

if Jobyear == "2018":
    p = PostProcessor("/eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_Nano/hzg/"+Jobyear+"/"+JobNumber,
                    inputFiles(),
                    modules=[jmeCorrections_mc_2018(),jmeCorrections_mc_fatjet_2018(),gammaSF_UL18(),puWeight_UL2018(),muonScaleRes2018(),METFilters_UL2018()],
                    provenance=True,
                    fwkJobReport=True,
                    jsonInput=runsAndLumis())
    p.run()
elif Jobyear == "2017":
    p = PostProcessor("/eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_Nano/hzg/"+Jobyear+"/"+JobNumber,
                    inputFiles(),
                    modules=[jmeCorrections_mc_2017(),jmeCorrections_mc_fatjet_2017(),gammaSF_UL17(),Prefcorr_2017(),puWeight_UL2017(),muonScaleRes2017(),METFilters_UL2017()],
                    provenance=True,
                    fwkJobReport=True,
                    jsonInput=runsAndLumis())
    p.run()
elif Jobyear == "2016preVFP":
    p = PostProcessor("/eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_Nano/hzg/"+Jobyear+"/"+JobNumber,
                    inputFiles(),
                    modules=[jmeCorrections_mc_2016pre(),jmeCorrections_mc_fatjet_2016pre(),gammaSF_UL16PreVFP(),Prefcorr_2016(),puWeight_UL2016(),muonScaleRes2016_UL16PreVFP(),METFilter_UL16PreVFP()],
                    provenance=True,
                    fwkJobReport=True,
                    jsonInput=runsAndLumis())
    p.run()
elif Jobyear == "2016postVFP":
    p = PostProcessor("/eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_Nano/hzg/"+Jobyear+"/"+JobNumber,
                    inputFiles(),
                    modules=[jmeCorrections_mc_2016post(),jmeCorrections_mc_fatjet_2016post(),gammaSF_UL16PostVFP(),Prefcorr_2016(),puWeight_UL2016(),muonScaleRes2016_UL16PostVFP(),METFilter_UL16PostVFP()],
                    provenance=True,
                    fwkJobReport=True,
                    jsonInput=runsAndLumis())
    p.run()
print("DONE")


print("DONE")