import math
import re
from collections import Counter
import numpy

WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

def cosine_similarity_sorter(input_, output_):
    with open(input_, "r") as d:
        data = d.readlines()
        r = []
        rr = 0
        d = 0
        for i in data:
            c = []
            cosine = []
            for j in data:
                # w
                if get_cosine(text_to_vector(i),text_to_vector(j)) > 0.6 and j not in r:
                    r.append(j)
                    c.append(j)
                    cosine.append(get_cosine(text_to_vector(i),text_to_vector(j)))
                    print(rr)
                    rr+=1
            if len(c)>2:
                d += 1
                for k in range(len(c)):
                    with open(output_, "a", encoding='utf8') as ka:
                        ka.write(f"{d} - {numpy.round(cosine[k], 3)} - {c[k]}\n")
                        
input_file =""
sorted_file = ""
cosine_similarity_sorter(input_file,sorted_file)



