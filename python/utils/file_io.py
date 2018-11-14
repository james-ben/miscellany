import csv

def text_to_list(filename):
    ret_list = []
    with open(filename) as txt:
        for line in txt:
            if line is not None:
                ret_list.append(line.rstrip())
    return ret_list


def list_to_text(filename, list):
    with open(filename, 'w') as outfile:
        for line in list:
            outfile.write(line + '\n')


def csv_to_list(filename):
    ret_list = []
    with open(filename, newline='') as csvfile:
        # data = list(csv.reader(csvfile))
        reader = csv.reader(csvfile)
        for row in reader:
            # skip the empty rows
            if len(row):
                ret_list.append(row)
    return ret_list


def list_to_csv(filename, list):
    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        for string in list:
            writer.writerow([string])
