from nltk.tokenize import sent_tokenize
import re
import csv
import os

def sentance_extractor(input_file ,extracted_sentance_file):
    try:
        with open(input_file, "r") as d:
            c = []
            data = d.read()
            data = sent_tokenize(data)
            sen = []
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
                        if len(j.split()) >= 3:
                            if "_" not in j:
                                if j[0].isalpha():
                                    j = re.sub('<[^>]+>', '', j)
                                    j = j.replace("  ", "")
                                    j = j.replace("   ", "")
                                    j = j.replace("'","")
                                    if len(j.split())>2:
                                        string = ""
                                        for o in j.split():
                                            if "!" in o or "?" in o or "." in o:
                                                o += "\n"
                                            string += f" {o}"
                                        # k.write(f"{string.strip()}\n")
                                        if len(string.strip().split()) > 3 and not ".at" in string:
                                            # print(string.strip())
                                            sen.append(string.strip())


        print(f"The sentences are correctly collected from the file {input_file}")
        return sen
    except:
        raise Exception

def new_func(input_, output_):
    with open(input_,"r")as d:
        data = d.readlines()
        from_to = []
        for i in data:
            a=0
            text = ""
            if "From:" in i or "Von:" in i:
                print("From:")
                from_to.append("From: " + i.strip().replace("   ","").replace("From:","").strip()+"\n")
            if "An:" in i or "To:" in i:
                print("\nTo:")
                from_to.append("To: " + i.strip().replace("  ","").replace("To:","").strip()+"\n")
        txt = ""
        with open(output_,"a")as new_d:
            for i in from_to:
                txt += (i+"\n")
            for i in sentance_extractor("email.txt", "data.txt"):
                txt += (i+"\n")
        print(txt)
            

new_func("email.txt", "data.txt")
