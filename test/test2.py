import re
import text2emotion

_input = ""
output = ""

def cleaner(data_input, data_output):
    with open(data_input, "r", encoding="utf8") as d:
        # Da gi podelam so , sekoj red
        data = d.readlines()
        data = [i.strip(",") for i in data]
        fin = []
        c = 0
        for i in data:
            h = []
            i = i.split(",")
            for j in i:
                if i[0] != j and i[2] != j:
                    #delete all text between <text>
                    j = re.sub(r'<.+>', '', j)
                    #delete all numbers
                    j = re.sub("\d+", "", j)
                    j = j.replace("\t", "")
                    #delete all urls
                    j = re.sub(r'http\S+', '', j)
                    #delete all
                    j = re.sub(r'[A-Za-z0-9]*@[A-Za-z]*\.?[A-Za-z0-9]*', "", j)
                    j = j.replace('"', "")
                    j = j.replace("+", "")
                    j = j.replace("-", "")
                    j = j.replace("+", "")
                    j = j.replace("t/", "")
                    j = j.replace("  ", " ")
                    j = re.sub("www.", "", j)
                    j = re.sub(".com", "", j)
                    j = j.strip()
                    j = j.replace("? ? ?", "")
                    j = j.replace("�", "")
                    j = j.replace("__", "")
                    j = re.sub(r"\([^()]*\)", "", j)
                    j = j.replace("\xad", "")
                    j = j.replace("***SPAM***", "")
                    for sk in j.split(" "):
                        if len(sk)>26 or "=" in sk:
                            j = ""
                    if "/O=EXCHANGELABS/OU=EXCHANGE" in j.split(' ') or "sbs" in j.split(" ") or "Re:" in j.split(" ") or "m." in j.split(" ")or "AW:" in j.split(" ") or "RE:" in j.split(" ") or ":" in j.split()or "TECHWAVE" in j.split() or "Attached" in j.split()or "Scanner" in j.split() or  "Tel:" in j.split(" ")or "Üdvözlettel:" in j.split(" ") or "xforefrontprvs:" in j.split(" ") or "|" in j.split(" "):
                        j = ""
                    if len(j) < 5:
                        j = ""
                    if j != "":
                        content = text2emotion.get_emotion(j)
                        if content['Surprise'] > 0.5 or content['Angry'] > 0.5 or content['Happy'] > 0.5 or content["Fear"] > 0.5 or content['Sad'] > 0.5:
                            j = j.split(".")
                            for gre in j:
                                content = text2emotion.get_emotion(gre)
                                if content['Surprise'] > 0.5 or content['Angry'] > 0.5 or content['Happy'] > 0.5 or content["Fear"] > 0.5 or content['Sad'] > 0.5:
                                    if len(gre.split())>1:
                                        h.append(gre)
                            print(c)
                            c += 1
                elif i[0] == j:
                    h.append(j)
            if h not in fin and len(h) >= 2:
                fin.append(h)
        gm = []
        sg = []
        pp = 0
        with open(data_output, "w") as gl:
            pp+=1
            if pp % 2 == 0:
                sg = i
            for i in fin:
                if len(i) > 1:
                    for j in i:
                        if j not in gm and j not in sg:
                            gl.write(f"{j.replace('   ','')}, ")
                    gm = i
                    gl.write("\n")
cleaner(_input, output)







