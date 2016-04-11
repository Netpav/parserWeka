import os
from collections import OrderedDict

from src.TextWriter import TextWriter

# FUNCTIONS

def skip_lines(f_handle, n):
    for i in range(0, n):
        f_handle.readline()

def get_summary(line_in):
    """
    Process Error on training split -- get accuracy and n. of test instances.
    :param line_in:
    :return:
    """
    correctly = ' '.join(line_in.strip().split())
    accuracy = correctly.split(' ')[-2]
    skip_lines(input_file, 13)
    total_n_of_inst = ' '.join(input_file.readline().strip().split())
    test_instances = total_n_of_inst.split(' ')[-1]

    return accuracy, test_instances

def get_accuracy_by_class(line_in):
    """
    Process Detailed Accuracy By Class -- get metrics.
    :param line_in:
    :return:
    """
    weighted_avg = ' '.join(line_in.strip().split())
    weighted_avg = weighted_avg.replace(',', '.')
    wa_stats = weighted_avg.split(' ')
    # TP Rate  FP Rate  Precision  Recall   F-Measure
    return wa_stats[2], wa_stats[3], wa_stats[4], wa_stats[5], wa_stats[6]

# CLI PARSING

# Read input file
algo_name = 'HT'
filename_in = 'HT'
input_file = open('input/cli/'+filename_in+'.txt')

# Prepare variables
data = OrderedDict()
data['algo_name'] = algo_name

# Get options - only for HT
if algo_name == 'HT':
    input_file.readline()
    data['options'] = input_file.readline().split(':')[1].strip()

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
    if line_parts and (line_parts[0].strip() == 'Time taken to test model on training split' or
                       line_parts[0].strip() == 'Time taken to test model on training data'):
        data['test_time'] = line_parts[1].strip().split(' ')[0]
        break

# Error on training split
skip_lines(input_file, 3)
data['accuracy'], data['test_instances'] = get_summary(input_file.readline())


# Detailed Accuracy By Class
skip_lines(input_file, 7)
data['tp_rate'], data['fp_rate'], data['precision'], data['recall'], data['f_measure'] = \
        get_accuracy_by_class(input_file.readline())

# Only for HT - Stratified cross-validation
if algo_name == 'HT':
    skip_lines(input_file, 12)
    data['cros_accuracy'], data['cros_test_instances'] = get_summary(input_file.readline())
    skip_lines(input_file, 7)
    data['cros_tp_rate'], data['cros_fp_rate'], data['cros_precision'], data['cros_recall'], data['cros_f_measure'] = \
        get_accuracy_by_class(input_file.readline())

# Close file
input_file.close()

print data

# Add data to output file.
text_writer = TextWriter('output')
header_list = data.keys()
data_list = data.values()

res_filename = filename_in+'_results'

# If the results file does not exist, create it and write header to it.
if not os.path.isfile('output/'+res_filename+'.csv'):
    text_writer.write_file(res_filename, [header_list])

# Write results.
text_writer.write_file(res_filename, [data_list])
