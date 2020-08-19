import csv
from scipy.stats import pearsonr


#Find the longest Substring between multiple strings
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
    if string[-1] == '-':
        string = string[:string.rfind('_')]

    return string


def get_parcellation(string):
    return string[string[:string.rfind('_')].rfind('_')+1:].split('_')[0]


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

