import os
from collections import OrderedDict

from src.TextWriter import TextWriter

# FUNCTIONS

def skip_lines(f_handle, n):
    for i in range(0, n):
        f_handle.readline()


# Read input file
filename_in = 'NB'
input_file = open('input/gui/'+filename_in+'.txt')

# NAIVE BAYES

# Get header info
input_file.readline()
input_file.readline()
scheme = input_file.readline().split(':')[1].strip()
data = OrderedDict()
data['algo_name'] = scheme.split('.')[-1]
input_file.readline()
data['total_instances'] = input_file.readline().split(':')[1].strip()
data['total_attributes'] = input_file.readline().split(':')[1].strip()
input_file.readline()
input_file.readline()

# Get to the results
while True:
    line = input_file.readline()
    if not line:
        break
    line_parts = line.split(':')
    # Train time
    if line_parts and line_parts[0].strip() == 'Time taken to build model':
        data['train_time'] = line_parts[1].strip().split(' ')[0]
    # Test time
    if line_parts and line_parts[0].strip() == 'Time taken to test model on training split':
        data['test_time'] = line_parts[1].strip().split(' ')[0]
        break

# Summary
skip_lines(input_file, 3)
correctly = ' '.join(input_file.readline().strip().split())
data['accuracy'] = correctly.split(' ')[-2]
skip_lines(input_file, 8)
total_n_of_inst = ' '.join(input_file.readline().strip().split())
data['test_instances'] = total_n_of_inst.split(' ')[-1]

# Detailed Accuracy By Class
skip_lines(input_file, 6)
weighted_avg = ' '.join(input_file.readline().strip().split())
weighted_avg = weighted_avg.replace(',', '.')
wa_stats = weighted_avg.split(' ')
data['tp_rate'] = wa_stats[2]
data['fp_rate'] = wa_stats[3]
data['precision'] = wa_stats[4]
data['recall'] = wa_stats[5]
data['f_measure'] = wa_stats[6]

input_file.close()

# Add data to output file
text_writer = TextWriter('output')
header_list = data.keys()
data_list = data.values()

res_filename = filename_in+'_results'

# If the results file does not exist, create it and write header to it.
if not os.path.isfile('output/'+res_filename+'.csv'):
    text_writer.write_file(res_filename, [header_list])

# Write results
text_writer.write_file(res_filename, [data_list])
