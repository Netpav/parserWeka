import glob
# import parse_cli_MOA_result_LearnModel
# import parse_cli_MOA_result_EvalTT
# import parse_cli_result
# import parse_cli_result_Param
import subprocess
import os
import sys

import parse_cli_result

for name in glob.glob('input/results_TP/*'):
    print "\n *********** \n"
    print name
    print "\n *********** \n"
    # execfile("parse_cli_result.py")
    os.system('python parse_cli_result.py name')
    # print "\n *********** \n"
    # parse_cli_result_Param name
    # print "\n *********** \n"
    # parse_cli_MOA_result_EvalTT name
    # print "\n *********** \n"
    # parse_cli_MOA_result_LearnModel name
    # print "\n *********** \n"
