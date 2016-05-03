import os
import sys
from collections import OrderedDict

from src.TextWriter import TextWriter


# FUNCTIONS

def skip_lines(f_handle, n):
    for i in range(0, n):
        f_handle.readline()


# def get_accuracy_by_class(line_in):
#     """
#     Process Detailed Accuracy By Class -- get metrics.
#     :param line_in:
#     :return:
#     """
#     weighted_avg = ' '.join(line_in.strip().split())
#     weighted_avg = weighted_avg.replace(',', '.')
#     wa_stats = weighted_avg.split(' ')
#     # TP Rate  FP Rate  Precision  Recall   F-Measure
#     return wa_stats[2], wa_stats[3], wa_stats[4], wa_stats[5], wa_stats[6]

# CLI PARSING

# RUN: python parse_cli_result.py <full path to file>

# Read argument - input file
if len(sys.argv) == 1:
    exit('You must enter full path to input file.')
path_to_file = sys.argv[1]
try:
    input_file = open(path_to_file)
except IOError:
    exit('File ' + path_to_file + ' does not exist or could not be read.')

# Read input file
# filename_in = 'HT'
# input_file = open('input/cli/'+filename_in+'.txt')

# Prepare variables
data = OrderedDict()
filename = os.path.basename(path_to_file).split('.')[0]
# name type algorithms e.g. HT
nameAlgo = os.path.basename(path_to_file).split('_')[2]
nameModel = os.path.basename(path_to_file).split('_')[3]

# Find out algorithm name
#input_file.readline()

name_line = input_file.readline().strip()

data['file_name'] = filename
if nameAlgo =='HT':
    algo_name = 'HoeffdingTree'
elif nameAlgo =='HTopt':
    algo_name = 'HoeffdingOptionTree'
elif nameAlgo =='HTadapt':
    algo_name = 'HoeffdingAdaptiveTree'
elif nameAlgo =='J48':
    algo_name = 'J48'
else:
    exit('Unsupported algorithm result.')

data['algo_name'] = algo_name

#input_file.readline()
#Get to the results
# Results file - one for every document type.
# For every file, there is for every classifier one row in following format:
header_str = 'learning evaluation instances,evaluation time (cpu seconds),model cost (RAM-Hours),classified instances,classifications correct (percent),Kappa Statistic (percent),Kappa Temporal Statistic (percent),Kappa M Statistic (percent),model training instances,model serialized size (bytes),tree size (nodes),tree size (leaves),active learning leaves,tree depth,active leaf byte size estimate,inactive leaf byte size estimate,byte size estimate overhead'
header_list = header_str.split(',')
#print header_list[1]
#data['learning evaluation instances'] = header_list[0]

while True:
    line = input_file.readline()
    if not line:
        break
    line_parts = line.strip().split(',')
    for a in range(0,len(line_parts)):
        data[header_list[a]]= line_parts[a]
#         for i in range(0,len(header_list)):
#             data[header_list[i]]= line_parts[a]

# Close file
input_file.close()

print data

# Add data to output file.
text_writer = TextWriter('output')
header_list = data.keys()
data_list = data.values()

res_filename = algo_name + nameModel+ '_results'

# If the results file does not exist, create it and write header to it.
if not os.path.isfile('output/' + res_filename + '.csv'):
    text_writer.write_file(res_filename, [header_list])

# Write results.
text_writer.write_file(res_filename, [data_list])



