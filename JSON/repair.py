import os
import json

DIRECTORY_WITH_FILES = "<-Enter the name or path of the folder with the files->"
def JSON_FIXER(DIRECTORY_WITH_FILES):
    files = os.listdir(DIRECTORY_WITH_FILES)
    counter = 0
    for rp in files:
        try:
            with open(f"{DIRECTORY_WITH_FILES}/{rp}", "r") as d:
                data = d.read().rstrip("\x00")
                newData = data.split()
                newData.reverse()
                ss = []
                g = 0
                for i in newData:
                    if (i == "}," or i == "}") and g == 0:
                        g = 1
                        if "," in i:
                            i = i.replace(",", "")
                    if g == 1:
                        ss.append(i)
                ss.reverse()
                data_for_save = " "
                for i in ss:
                    data_for_save += (" " + str(i))
                with open(f"{DIRECTORY_WITH_FILES}/{rp}", "w") as n:
                    n.write(data_for_save + "]")
                    print(counter)
                    counter+=1
        except:
            pass
JSON_FIXER(DIRECTORY_WITH_FILES)
