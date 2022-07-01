from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import math
import re
from collections import Counter
import numpy
nltk.download('stopwords')


def cosine_similarity_sorter(input_, output_):
    with open(input_, "r") as d:
        data = d.readlines()
        r = []
        rr = 0
        d = 0
        for i in data:
            cc = []
            cosinee = []
            for j in data:
                X_list = word_tokenize(i)
                Y_list = word_tokenize(j)
                sw = stopwords.words('english')
                l1 = [];
                l2 = []
                X_set = {w for w in X_list if not w in sw}
                Y_set = {w for w in Y_list if not w in sw}
                rvector = X_set.union(Y_set)
                for w in rvector:
                    if w in X_set:
                        l1.append(1)  # create a vector
                    else:
                        l1.append(0)
                    if w in Y_set:
                        l2.append(1)
                    else:
                        l2.append(0)
                c = 0
                for kr in range(len(rvector)):
                    c += l1[kr] * l2[kr]
                if float((sum(l1) * sum(l2)) ** 0.5):
                    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
                else:
                    continue
                if cosine > 0.48  and j not in r:
                    r.append(j)
                    cc.append(j)
                    cosinee.append(cosine)
                    print(rr)
                    rr+=1
            if len(cc)>2:
                d += 1
                for k in range(len(cc)):
                    with open(output_, "a", encoding='utf8') as ka:
                        ka.write(f"{d} - {numpy.round(cosinee[k], 3)} - {cc[k]}\n")

input_file =""
sorted_file = ""
cosine_similarity_sorter(input_file,sorted_file)
