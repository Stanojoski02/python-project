from nltk.tokenize import sent_tokenize
import re
with open("emails Bojan.txt","r",encoding="utf8") as d:
    c = []
    data =d.read()
    data = sent_tokenize(data)
    for i in data:
        a = 0
        for j in i:
            if j.isdigit():
                a = 1
        if a==0:
            if len(i.split())>1:
                c.append(i)
    with open("test3-1.txt", "w")as k:
        for i in c:
            for j in i.split("@"):
                j = j.replace("*","")
                if(len(j.split())>=3):
                    if "_" not in j:
                        if j[0].isalpha():
                            j = re.sub('<[^>]+>', '', j)
                            j = j.replace("  ","")
                            k.write(f"{j.strip()}\n")
