"""
# How to run:
python3 condor_setup_lxplus.py
"""
import argparse
import os
import sys
import glob
import infoCreaterGit
import fileshelper
import makeTarFile
sys.path.append("Utils/.")

from color_style import style

def main(args):

    # Variables from argparse
    submission_name = args.submission_name
    use_custom_eos = args.use_custom_eos
    use_custom_eos_cmd = args.use_custom_eos_cmd
    InputFileFromWhereReadDASNames = args.input_file
    EOS_Output_path = args.eos_output_path
    condor_file_name = args.condor_file_name
    condor_queue = args.condor_queue
    condor_log_path = args.condor_log_path
    createTarFile = args.createTarFile
    useDAS = args.useDAS

    # Get top-level directory name from PWD
    TOP_LEVEL_DIR_NAME = os.path.basename(os.getcwd())

    if EOS_Output_path == "":
        # Get the username and its initial and set the path as /eos/user/<UserInitials>/<UserName>/nanoAOD_ntuples
        username = os.environ['USER']
        user_initials = username[0:1]
        EOS_Output_path = '/eos/user/'+user_initials+'/'+username+'/nanoAOD_ntuples'
    EOS_Output_path += submission_name
    condor_file_name = 'submit_condor_jobs_lnujj_'+submission_name

    # Create log files
    SumamryOfCurrentSubmission = raw_input("\n\nWrite summary for current job submission: ")
    infoLogFiles = infoCreaterGit.BasicInfoCreater('summary.dat',SumamryOfCurrentSubmission)
    infoLogFiles.generate_git_patch_and_log()

    # Get CMSSW directory path and name
    cmsswDirPath = os.environ['CMSSW_BASE']
    CMSSWRel = cmsswDirPath.split("/")[-1]

    # Create directories for storing log files and output files at EOS.
    dirsToCreate = fileshelper.FileHelper( (condor_log_path + '/condor_logs/'+submission_name).replace("//","/"), EOS_Output_path)
    output_log_path = dirsToCreate.create_log_dir_with_date()
    storeDir = dirsToCreate.create_store_area(EOS_Output_path)
    dirName = dirsToCreate.dir_name

    # create tarball of present working CMSSW base directory
    if createTarFile: os.system('rm -f CMSSW*.tgz')
    if createTarFile: makeTarFile.make_tarfile(cmsswDirPath, CMSSWRel+".tgz")
    print("copying the "+CMSSWRel+".tgz  file to eos path: "+storeDir+"\n")
    os.system('cp ' + CMSSWRel+".tgz" + ' '+storeDir+'/' + CMSSWRel+".tgz")

    

    Transfer_Input_Files = ("keep_and_drop.txt")     # FIXME: Generalise this.

    if useDAS==True:
        with open('input_data_Files/'+InputFileFromWhereReadDASNames) as in_file:
            outjdl_file = open(condor_file_name+".jdl","w")
            outjdl_file.write("+JobFlavour   = \""+condor_queue+"\"\n")
            outjdl_file.write("Executable = "+condor_file_name+".sh\n")
            outjdl_file.write("Universe = vanilla\n")
            outjdl_file.write("Notification = ERROR\n")
            outjdl_file.write("Should_Transfer_Files = YES\n")
            outjdl_file.write("WhenToTransferOutput = ON_EXIT\n")
            outjdl_file.write("Transfer_Input_Files = "+Transfer_Input_Files + ",  " + post_proc_to_run+"\n")
            outjdl_file.write("x509userproxy = $ENV(X509_USER_PROXY)\n")
            count = 0
            count_jobs = 0
            for lines in in_file:
                if lines[0] == "#": continue
                count = count +1
                #if count > 1: break
                print(style.RED +"="*51+style.RESET+"\n")
                print ("==> Sample : ",count)
                sample_name = lines.split('/')[1]
                campaign = lines.split('/')[2].split('-')[0]
                print("==> sample_name = ",sample_name)
                print("==> campaign = ",campaign)
                ########################################
                #
                #      Create output directory
                #
                ########################################
                if sample_name.find("SingleMuon") != -1 or sample_name.find("SingleElectron") != -1 or sample_name.find("EGamma") != -1 or sample_name.find("DoubleMuon") != -1 or sample_name.find("MuonEG") != -1 or sample_name.find("DoubleEG") != -1:
                    output_string = sample_name + os.sep + campaign + os.sep + dirName
                    output_path = EOS_Output_path + os.sep + output_string
                    os.system("mkdir "+EOS_Output_path + os.sep + sample_name)
                    os.system("mkdir "+EOS_Output_path + os.sep + sample_name + os.sep + campaign)
                    os.system("mkdir "+ EOS_Output_path + os.sep + sample_name + os.sep + campaign + os.sep + dirName)
                    infoLogFiles.send_git_log_and_patch_to_eos(EOS_Output_path + os.sep + sample_name + os.sep + campaign + os.sep + dirName)
                else:
                    output_string = sample_name+os.sep+dirName
                    output_path = EOS_Output_path+ os.sep + output_string
                    os.system("mkdir "+EOS_Output_path + os.sep + sample_name)
                    os.system("mkdir "+EOS_Output_path + os.sep + sample_name+os.sep+dirName)
                    infoLogFiles.send_git_log_and_patch_to_eos(EOS_Output_path + os.sep + sample_name + os.sep + dirName)
                #  print "==> output_path = ",output_path

                ########################################
                #print 'dasgoclient --query="file dataset='+lines.strip()+'"'
                #print "..."
                if use_custom_eos:
                    xrd_redirector = 'root://cms-xrd-global.cern.ch/'
                    output = os.popen(use_custom_eos_cmd + lines.strip()).read()
                else:
                    xrd_redirector = 'root://cms-xrd-global.cern.ch/'
                    output = os.popen('dasgoclient --query="file dataset='+lines.strip()+'"').read()

                count_root_files = 0
                for root_file in output.split():
                    #print "=> ",root_file
                    count_root_files+=1
                    count_jobs += 1
                    outjdl_file.write("Output = "+output_log_path+"/"+sample_name+"_$(Process).stdout\n")
                    outjdl_file.write("Error  = "+output_log_path+"/"+sample_name+"_$(Process).stdout\n")
                    outjdl_file.write("Log  = "+output_log_path+"/"+sample_name+"_$(Process).log\n")
                    outjdl_file.write("Arguments = "+(xrd_redirector+root_file).replace('/','\/')+" "+output_path+"  "+EOS_Output_path+"\n")
                    outjdl_file.write("Queue \n")
                print("Number of files: ",count_root_files)
                print("Number of jobs (till now): ",count_jobs)
            outjdl_file.close();
    else:
        with open('input_data_Files/'+InputFileFromWhereReadDASNames) as in_file:
            outjdl_file = open(condor_file_name+".jdl","w")
            outjdl_file.write("+JobFlavour   = \""+condor_queue+"\"\n")
            outjdl_file.write("Executable = "+condor_file_name+".sh\n")
            outjdl_file.write("Universe = vanilla\n")
            outjdl_file.write("Notification = ERROR\n")
            outjdl_file.write("Should_Transfer_Files = YES\n")
            outjdl_file.write("WhenToTransferOutput = ON_EXIT\n")
            outjdl_file.write("Transfer_Input_Files = "+Transfer_Input_Files + ",  " + post_proc_to_run+"\n")
            outjdl_file.write("x509userproxy = $ENV(X509_USER_PROXY)\n")
            for lines in in_file:
                if lines[0] == "#": continue
                count = count +1
                #if count > 1: break
                print(style.RED +"="*51+style.RESET+"\n")
                print ("==> Sample : ",count)
                sample_name = lines.split('/')[-1]
                if sample_name.find("data") != -1 or sample_name.find("SingleMuon") != -1 or sample_name.find("SingleElectron") != -1 or sample_name.find("EGamma") != -1 or sample_name.find("DoubleMuon") != -1 or sample_name.find("MuonEG") != -1 or sample_name.find("DoubleEG") != -1:
                    output_string = sample_name + os.sep + dirName
                    output_path = "/eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_nanoAOD/UL17data/"+sample_name + os.sep
                    os.system("mkdir /eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_nanoAOD/UL17data/"+ sample_name)
                else:
                    output_string = sample_name + os.sep + dirName
                    output_path = "/eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_nanoAOD/UL17MC/"+sample_name + os.sep
                    os.system("mkdir /eos/cms/store/group/phys_higgs/cmshgg/shsong/custom_nanoAOD/UL17MC/"+ sample_name)
                output = glob.glob(lines+os.sep+"*.root")
                count_root_files = 0
                xrd_redirector = 'root://cms-xrd-global.cern.ch/'
                for root_file in output.split():
                    #print "=> ",root_file
                    count_root_files+=1
                    count_jobs += 1
                    outjdl_file.write("Output = "+output_log_path+"/"+sample_name+"_$(Process).stdout\n")
                    outjdl_file.write("Error  = "+output_log_path+"/"+sample_name+"_$(Process).stdout\n")
                    outjdl_file.write("Log  = "+output_log_path+"/"+sample_name+"_$(Process).log\n")
                    outjdl_file.write("Arguments = "+(xrd_redirector+root_file).replace('/','\/')+" "+output_path+"  "+EOS_Output_path+"\n")
                    outjdl_file.write("Queue \n")
                print("Number of files: ",count_root_files)
                print("Number of jobs (till now): ",count_jobs)
    post_proc_to_run = "scripts/nano_postproc.py"
    command = "python "+post_proc_to_run + " " + outputdir + " "+inputfile+ " -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertainties2017AK4PuppiAll -I PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer muonScaleRes2017"
    outScript = open(condor_file_name+".sh","w");
    outScript.write('#!/bin/bash');
    outScript.write("\n"+'echo "Starting job on " `date`');
    outScript.write("\n"+'echo "Running on: `uname -a`"');
    outScript.write("\n"+'echo "System software: `cat /etc/redhat-release`"');
    outScript.write("\n"+'source /cvmfs/cms.cern.ch/cmsset_default.sh');
    outScript.write("\n"+'echo "copy cmssw tar file from store area"');
    outScript.write("\n"+'cp -s ${3}/'+CMSSWRel +'.tgz  .');
    outScript.write("\n"+'tar -xf '+ CMSSWRel +'.tgz' );
    outScript.write("\n"+'rm '+ CMSSWRel +'.tgz' );
    outScript.write("\n"+'cd ' + CMSSWRel + '/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/'+TOP_LEVEL_DIR_NAME+'/' );
    #outScript.write("\n"+'echo "====> List files : " ');
    #outScript.write("\n"+'ls -alh');
    outScript.write("\n"+'rm *.root');
    outScript.write("\n"+'scramv1 b ProjectRename');
    outScript.write("\n"+'eval `scram runtime -sh`');
    outScript.write("\n"+'sed -i "s/ifRunningOnCondor = .*/ifRunningOnCondor = True/g" '+post_proc_to_run);
    outScript.write("\n"+'sed -i "s/testfile = .*/testfile = \\"${1}\\"/g" '+post_proc_to_run);
    outScript.write("\n"+'echo "========================================="');
    outScript.write("\n"+'echo "cat nano_postproc.py"');
    outScript.write("\n"+'echo "..."');
    outScript.write("\n"+'cat nano_postproc.py');
    outScript.write("\n"+'echo "..."');
    outScript.write("\n"+'echo "========================================="');
    outScript.write("\n"+command);
    outScript.write("\n"+'echo "====> List root files : " ');
    outScript.write("\n"+'ls *.root');
    outScript.write("\n"+'echo "====> copying *.root file to stores area..." ');
    outScript.write("\n"+'if ls *_Skim.root 1> /dev/null 2>&1; then');
    outScript.write("\n"+'    echo "File *_Skim.root exists. Copy this."');
    outScript.write("\n"+'    echo "cp *_Skim.root ${2}"');
    outScript.write("\n"+'    cp  *_Skim.root ${2}');
    outScript.write("\n"+'else');
    outScript.write("\n"+'    echo "file *_Skim.root does not exists, so copy *.root file."');
    outScript.write("\n"+'    echo "cp *.root ${2}"');
    outScript.write("\n"+'    cp  *.root ${2}');
    outScript.write("\n"+'fi');
    outScript.write("\n"+'rm *.root');
    outScript.write("\n"+'cd ${_CONDOR_SCRATCH_DIR}');
    outScript.write("\n"+'rm -rf ' + CMSSWRel);
    outScript.write("\n");
    outScript.close();
    os.system("chmod 777 "+condor_file_name+".sh");

    print("\n#===> Set Proxy Using:")
    print("voms-proxy-init --voms cms --valid 168:00")
    print("\n# It is assumed that the proxy is created in file: /tmp/x509up_u48539. Update this in below two lines:")
    print("cp /tmp/x509up_u48539 ~/")
    print("export X509_USER_PROXY=~/x509up_u48539")
    print("\n#Submit jobs:")
    print("condor_submit "+condor_file_name+".jdl")
    #os.system("condor_submit "+condor_file_name+".jdl")

# Below patch is to format the help command as it is
class PreserveWhitespaceFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Condor Job Submission", formatter_class=PreserveWhitespaceFormatter)
    parser.add_argument("--submission_name", default="Run2018_v9", help="String to be changed by user.")
    parser.add_argument("--use_custom_eos", default=False, action='store_true', help="Use custom EOS.")
    parser.add_argument("--createTarFile", default=True, action='store_false', help="Use custom EOS.")
    parser.add_argument("--use_custom_eos_cmd", default='eos root://cmseos.fnal.gov find -name "*.root" /store/group/lnujj/VVjj_aQGC/custom_nanoAOD', help="Custom EOS command.")
    parser.add_argument("--useDAS", default=False, help="Use Das sample or eos sample.")
    # input_file mandatory
    parser.add_argument("--input_file", default='', required=True,  help="Input file from where to read DAS names.")
    parser.add_argument("--eos_output_path", default='', help="Initial path for operations.")
    parser.add_argument("--condor_log_path", default='./', help="Path where condor log should be saved. By default is the current working directory")
    parser.add_argument("--condor_file_name", default='submit_condor_jobs_lnujj_', help="Name for the condor file.")
    parser.add_argument("--condor_queue", default="microcentury", help="""
                        Condor queue options: (Reference: https://twiki.cern.ch/twiki/bin/view/ABPComputing/LxbatchHTCondor#Queue_Flavours)

                        name            Duration
                        ------------------------
                        espresso            20min
                        microcentury     1h
                        longlunch           2h
                        workday 8h        1nd
                        tomorrow           1d
                        testmatch          3d
                        nextweek           1w
                        """)

    parser.add_argument("--post_proc", default="post_proc.py", help="Post process script to run.")
    parser.add_argument("--transfer_input_files", default="keep_and_drop.txt", help="Files to be transferred as input.")

    args = parser.parse_args()
    main(args)