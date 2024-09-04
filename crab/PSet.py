# this fake PSET is needed for local test and for crab to figure the output
# filename you do not need to edit it unless you want to do a local test using
# a different input file than the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(),
    # lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
    '/eos/cms/store/group/phys_b2g/shsong/nanoAODnTuples/nanoAOD_Mar2024/UL2017_HHSLsignal/UL2017/GluGluToRadionToHHTo2G2WTo2G2Q1L1Nu_M-500/D45DF4DC-941E-3742-BDB3-B87D065F4E60.root'  # you can change only this line
]
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule",
                                  fileName=cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
