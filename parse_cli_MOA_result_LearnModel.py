import os
import sys
from collections import OrderedDict

from src.TextWriter import TextWriter

# CLI PARSING
#  Modification for LearnModel
# RUN: python parse_cli_MOA_result.py <full path to file>

# Read argument - input file
if len(sys.argv) == 1:
    exit('You must enter full path to input file.')
path_to_file = sys.argv[1]
try:
    input_file = open(path_to_file)
except IOError:
    exit('File ' + path_to_file + ' does not exist or could not be read.')

# Prepare variables
data = OrderedDict()
filename = os.path.basename(path_to_file).split('.')[0]
nameAlgo = os.path.basename(path_to_file).split('_')[-2]
nameModel = os.path.basename(path_to_file).split('_')[-1]

#  split number of documents
Num = os.path.basename(path_to_file).split('_')[1]
data['Num'] = Num
# Find out file name + algo name
name_line = input_file.readline().strip()
data['file_name'] = filename

if nameAlgo == 'HT':
    algo_name = 'HoeffdingTree'
elif nameAlgo == 'HTopt':
    algo_name = 'HoeffdingOptionTree'
elif nameAlgo == 'HTadapt':
    algo_name = 'HoeffdingAdaptiveTree'
elif nameAlgo == 'adaptHTopt':
    algo_name = 'AdaptiveHoeffdingOptionTree'
elif nameAlgo == 'J48':
    algo_name = 'J48'
else:
    exit('Unsupported algorithm result.')
# Set algo name
data['algo_name'] = algo_name
#  =================  Special version of loading ===============================#
# if name_line[0:11] == 'Model type:':
#     data['model_type'] = name_line.split(':')[1].strip()
#     if data['model_type'] == 'moa.classifiers.trees.HoeffdingTree':
#         algo_name = 'HoeffdingTree'
#         data['algo_name'] = algo_name
#     elif data['model_type'] == 'moa.classifiers.trees.HoeffdingAdaptiveTree':
#         algo_name = 'HoeffdingAdaptiveTree'
#         data['algo_name'] = algo_name
#     elif data['model_type'] == 'moa.classifiers.trees.HoeffdingOptionTree':
#         algo_name = 'HoeffdingOptionTree'
#         data['algo_name'] = algo_name
# elif name_line == 'J48 pruned tree':
#     # moa.classifiers.meta.WEKAClassifier
#     algo_name = 'J48'
#     data['algo_name'] = algo_name
# else:
#     exit('Unsupported algorithm result.')
if nameModel == "learnModel":
    if nameAlgo == 'J48':
        print "J48"
        while True:
            line = input_file.readline()
            if not line:
                break
            line_parts = line.split(':')
            # Train time
            if line_parts and line_parts[0].strip() == 'Number of Leaves':
                data['number_of_leaves'] = line_parts[1].strip().split(' ')[0]
            elif line_parts and (line_parts[0].strip() == 'Size of the tree'):
                data['size_of_tree'] = line_parts[1].strip().split(' ')[0]


    else:
        while True:
            line = input_file.readline()
            if not line:
                break
            line_parts = line.split('=')

            # Test tree parts
            # if line_parts and (line_parts[0].strip() == 'model training instances'):
            #     data['model training instances'] = line_parts[1].strip().split(' ')[0]
            if line_parts and (line_parts[0].strip() == 'model serialized size (bytes)'):
                data['model serialized size (bytes)'] = line_parts[1].strip().split(' ')[0]
            elif line_parts and (line_parts[0].strip() == 'tree size (nodes)'):
                data['tree size (nodes)'] = line_parts[1].strip().split(' ')[0]
            elif line_parts and (line_parts[0].strip() == 'tree size (leaves)'):
                data['tree size (leaves)'] = line_parts[1].strip().split(' ')[0]
            elif line_parts and (line_parts[0].strip() == 'active learning leaves'):
                data['active learning leaves '] = line_parts[1].strip().split(' ')[0]
            elif line_parts and (line_parts[0].strip() == 'tree depth'):
                data['tree depth'] = line_parts[1].strip().split(' ')[0]
            elif line_parts and (line_parts[0].strip() == 'maximum prediction paths used'):
                data['maximum prediction paths used'] = line_parts[1].strip().split(' ')[0]
else:
    exit('Unsupported model result.')  # Get to the results

 # Close file
input_file.close()

print data

# Add data to output file.
text_writer = TextWriter('output')
header_list = data.keys()
data_list = data.values()

# Result nameFile
res_filename = algo_name + '' + nameModel + '_results'

# If the results file does not exist, create it and write header to it.
if not os.path.isfile('output/' + res_filename + '.csv'):
    text_writer.write_file(res_filename, [header_list])

# Write results.
text_writer.write_file(res_filename, [data_list])

