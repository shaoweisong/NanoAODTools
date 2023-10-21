#!/bin/bash
echo "Starting job on " `date`
echo "Running on: `uname -a`"
echo "System software: `cat /etc/redhat-release`"
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "copy cmssw tar file from store area"
tar czf /eos/user/s/shsong/Nanoaodtool/CMSSW_10_6_20.tgz --exclude=/afs/cern.ch/user/s/shsong/CMSSW_10_6_20/src/auxiliaries /afs/cern.ch/user/s/shsong/CMSSW_10_6_20/
cp czf /eos/user/s/shsong/Nanoaodtool/CMSSW_10_6_20.tgz .

tar -xf CMSSW_10_6_20.tgz
rm CMSSW_10_6_20.tgz
cd CMSSW_10_6_20/src/PhysicsTools/NanoAODTools/scripts/
rm *.root
scramv1 b ProjectRename
eval `scram runtime -sh`
sed -i "s/ifRunningOnCondor = .*/ifRunningOnCondor = True/g" nano_postproc.py
sed -i "s/testfile = .*/testfile = \"/eos/user/z/zhenxuan/customized_NanoAOD/UL17/UL17_R_gghh_M-250/out_UL17_R_gghh_M-250_C63EC9186331_350650_561.root\"/g" nano_postproc.py
echo "========================================="
echo "cat nano_postproc.py"
echo "..."
cat nano_postproc.py
echo "..."
echo "========================================="
python nano_postproc.py /eos/user/s/shsong/Nanoaodtool/test/ /eos/user/z/zhenxuan/customized_NanoAOD/UL17/UL17_R_gghh_M-250/out_UL17_R_gghh_M-250_C63EC9186331_350650_561.root -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertainties2017AK4PuppiAll -I PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer muonScaleRes2017
echo "====> List root files : " 
ls *.root
echo "====> copying *.root file to stores area..." 
if ls *_Skim.root 1> /dev/null 2>&1; then
    echo "File *_Skim.root exists. Copy this."
    echo "cp *_Skim.root /eos/user/s/shsong/Nanoaodtool/test/"
    cp  *_Skim.root /eos/user/s/shsong/Nanoaodtool/test/
else
    echo "file *_Skim.root does not exists, so copy *.root file."
    echo "cp *.root /eos/user/s/shsong/Nanoaodtool/test/"
    cp  *.root /eos/user/s/shsong/Nanoaodtool/test/
fi
rm *.root
cd ${_CONDOR_SCRATCH_DIR}
