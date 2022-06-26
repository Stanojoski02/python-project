import numpy
def jaccard_similarity(x, y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)
def sorter(data_input, data_out):
    r = []
    q = 0
    try:
        with open(data_input,"r")as d:
            data = d.readlines()
            c=0
            gg=0
            ca = []
            for i in data:
                g = 0
                r = []
                jaccard_ = []
                for j in data:
                    if(jaccard_similarity(i.split(),j.split())>0.3):
                        if g==0:
                            c+=1
                            g+=1
                        print(f"{c} - {j}")
                        if j.replace("'","") not in r and j.replace("'","") not in ca:
                            # if i not in r:
                            #     r.append(i)
                            samo = 0
                            for ui in r:
                                if ui.split() == j.split():
                                    samo = 1
                            if samo == 0:
                                r.append(j)
                                ca.append(j)
                                jaccard_.append(jaccard_similarity(i.split(),j.split()))
                try:
                    if len(r)>=2:
                        with open(data_out, "a") as d:
                            for sas in range(len(r)):
                                d.write(f"{q} - {numpy.round(jaccard_[sas], 3)} - {r[sas]}")
                        q+=1
                except:
                    print("The file in which the data is to be entered was not found")
    except:
        print("The file that needs to sort sentences has not been found")

input_file ="ne_znam.txt"
sorted_file = "KakoEbojan.txt"



sorter(input_file,sorted_file)
