#This program will take in multiple _ts.1D from xcp-engine and create a Concatenated Time series then it will correlate the timeseries using the Pearson Correlation
#It takes 2 required arguments: inputFiles which is a list of space seperated files. and outDir which is where the files will be places

import csv
from scipy.stats import pearsonr
import argparse
import os
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


def longest_substring_finder(stringList):

    length = len(stringList[0])
    match = ""
    for i in range(length):

        char_match = True
        for string in stringList:

            if string[i] is not stringList[0][i]:
                char_match = False

        if char_match:
            match = match + stringList[0][i]
        else:
            break

    return match


def remove_empty_prefix(string):
    if string[-1] is '-':
        string = string[:string.rfind('_')]

    return string


def get_parcellation(string):
    return string[string[:string.rfind('_')].rfind('_')+1:].split('_')[0]   #What


def append(filelist, outfile):

    for file in filelist:

        fin = open(file, "r")
        data = fin.read()
        fin.close()

        fout = open(outfile, "a")
        fout.write(data)
        fout.close()


def transpose(filename):

    index = filename.find('.1D')
    outfile = filename[:index] + '_transpose' + filename[index:]

    with open(filename) as f:
        lis = [x.split() for x in f]


    with open(outfile, 'w') as f:

        for x in zip(*lis):
            for y in x:
                f.write(y+' ')
            f.write('\n')

    return outfile


def add_net_header(filename, num_of_parcels):
    with open(filename, newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
    with open(filename, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['*Vertices ' + str(num_of_parcels)])
        w.writerow(['*Edges NA'])
        w.writerows(data)


def correlate(filename, outfile):
    num_of_parcels = 0
    with open(filename) as file1:
        with open(outfile, 'w') as f:
            for parcel_number, parcel in enumerate(file1):
                parcel = [float(i) for i in parcel.split()]
                with open(filename) as file2:
                    for row_number, row in enumerate(file2):
                        row = [float(i) for i in row.split()]
                        if row_number > parcel_number:
                            f.write(str(parcel_number + 1) + " " + str(row_number + 1) + " " + str(round(pearsonr(parcel, row)[0], 6)) + '\n')
                if (parcel_number + 1) > (num_of_parcels):
                    num_of_parcels = parcel_number + 1

    add_net_header(outfile, num_of_parcels)


#input_files = ['/home/mitchell/Desktop/sub-150423_ses-wave1bas_task-Rest_run-1_schaefer400_ts.1D',
#              '/home/mitchell/Desktop/sub-150423_ses-wave1bas_task-Rest_run-2_schaefer400_ts.1D']

#output_dir = "/my/output"

#filename = "/home/mitchell/Desktop/sub-150423_ses-wave1bas_task-Rest_schaefer400_ts.1D"
input_file_basenames = []
for file in inputFiles:
    input_file_basenames.append(os.path.basename(file))

concatenated_timeseries = remove_empty_prefix(longest_substring_finder(input_file_basenames)) + "_"\
                          + get_parcellation(input_file_basenames[0])\
                          + "_ts.1D"
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

