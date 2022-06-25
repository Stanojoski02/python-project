
from nltk.tokenize import sent_tokenize
import re
import csv
import os

# Input data must be in txt format as well as output.
# Then you get a csv file with the same name
data_input = ""
data_output = ""

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
                                    j = j.replace("'","")
                                    if len(j.split())>1:
                                        string = ""
                                        for o in j.split():
                                            if "!" in o or "?" in o or "." in o:
                                                o += "\n"
                                            string += f" {o}"
                                        k.write(f"{string.strip()}\n")
        print(f"The sentences are correctly collected from the file {input_file}")
    except:
        raise Exception
sentance_extractor(data_input,data_output)
