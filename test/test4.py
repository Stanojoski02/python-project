from nltk.tokenize import sent_tokenize
import re
import csv
import os

# Input data must be in txt format as well as output.
# Then you get a csv file with the same name
data_input = "test4.txt"
data_output = "test4-out.txt"

def sentance_extractor(input_file ,extracted_sentance_file):
    try:
        with open(input_file, "r") as d:
            c = []
            data = d.read()
            data = sent_tokenize(data)
            for i in data:
                a = 0
                for j in i:
                    if j.isdigit():
                        a = 1
                if a == 0:
                    if len(i.split())>1:
                        c.append(i)
            with open(extracted_sentance_file, "w")as k:
                for i in c:
                    for j in i.split("@"):
                        j = j.replace("*","")
                        if( len( j.split()) >= 3):
                            if "_" not in j:
                                if j[0].isalpha():
                                    j = re.sub('<[^>]+>', '', j)
                                    j = j.replace("  ", "")
                                    j = j.replace("   ", "")
                                    if len(j.split())>1:
                                        k.write(f"{j.strip()}\n")
        print(f"The sentences are correctly collected from the file {input_file}")
    except:
        raise Exception

def jaccard_similarity(x, y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)

def jaccard_similarity_sorter(_input,out):
    try:
        with open(_input, "r") as d:
            data = d.readlines()
            new_d = []
            for s in range(len(data) - 1):
                dd = []
                mm = []
                ssa = 0.1
                bopojapan = 0.2
                for i in data:
                    if jaccard_similarity(data[s].split(), i.split()) > bopojapan and i != data[s]:
                        print(jaccard_similarity(data[s].split(), i.split()))
                        if i not in dd:
                            if bopojapan < 0.8:
                                bopojapan += 0.035
                            else:
                                bopojapan = ssa
                                ssa += 1
                            dd.append(i)
                            mm.append(jaccard_similarity(data[s].split(), i.split()))
                if dd not in new_d:
                    new_d.append(dd)

            print("_              _                   _")
            grm = 0
            new_list = []
            for i in new_d:
                if len(i) > 2:
                    grm += 1
                    for j in i:
                        if grm < 20000:
                            if j not in new_list:
                                new_list.append(j)
            for i in new_list:
                print(i)
            p = 0
            with open(out, "w") as gg:
                writer = csv.writer(gg)
                c = []
                for i in new_list:
                    if p % 2 == 0:
                        c = i.split()
                    if i.split() != c and p % 2 != 0:
                        writer.writerow([p, i])
                        p += 1
                    else:
                        writer.writerow([p, i.strip()])
                        p += 1
                        print(p)
    except:
        print("The file you entered does not exist")


# Input data must be in txt format as well as output.
# Then you get a csv file with the same name

def sentance_extractor_and_jaccard_similarity_sorter(_input,out):
    txt_file = out
    sentance_extractor(_input,out)
    jaccard_similarity_sorter(out,out.replace(".txt",".csv"))
    os.remove(txt_file)

#We can use each function separately
#but we can use them together

sentance_extractor_and_jaccard_similarity_sorter(data_input,data_output)
