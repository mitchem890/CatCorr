#This program will take in multiple _ts.1D from xcp-engine and create a Concatenated Time series then it will correlate the timeseries using the Pearson Correlation
#It takes 2 required arguments: inputFiles which is a list of space seperated files. and outDir which is where the files will be places

import argparse
import os
from CatCorr.CatCorrFunc import *

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--inputFiles', '-i', nargs='+', help='Space separated of the list of timeseries you would like to'
                    ' concatenate and correlate. These files will have the extension of *_ts.1D', required=True)
parser.add_argument('--outputDir', '-o', help='Where your output will be located', required=True)


args = parser.parse_args()
inputFiles = args.inputFiles
outputDir = args.outputDir

for file in inputFiles:
    if not os.path.exists(file):
        print('Could not find file: ' + file + '\nPlease Check')
        exit()

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

#filename = "/home/mitchell/Desktop/sub-150423_ses-wave1bas_task-Rest_schaefer400_ts.1D"
input_file_basenames = []
for file in inputFiles:
    input_file_basenames.append(os.path.basename(file))

concatenated_timeseries = f"{remove_empty_prefix(longest_substring_finder(input_file_basenames))}" \
                          f"_{get_parcellation(input_file_basenames[0])}_ts.1D"
outCat = os.path.join(outputDir, concatenated_timeseries)
print("Concatenated Time Series: " + outCat)
append(inputFiles, outCat)
transposed_timeseries = transpose(outCat)

correlated_name = remove_empty_prefix(longest_substring_finder(input_file_basenames)) + "_"\
                          + get_parcellation(input_file_basenames[0])\
                          + ".net"
CatCorr = os.path.join(outputDir, correlated_name)
print("Correlated Concatenated Time Series: " + CatCorr)
correlate(transposed_timeseries, CatCorr)

