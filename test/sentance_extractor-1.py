
def sentance_extractor(sentances):
    c = []
    data = sent_tokenize(sentances)
    for i in data:
        a = 0
        for j in i:
            if j.isdigit():
                a = 1
        if a == 0:
            if len(i.split()) > 1:
                c.append(i)
    extracted_sentance = []
    for i in c:
        for j in i.split("@"):
            j = j.replace("*", "")
            if len(j.split()) >= 2 :
                if "_" not in j:
                    if j[0].isalpha():
                        j = re.sub('<[^>]+>', '', j)
                        j = j.replace("  ", "")
                        j = j.replace("   ", "")
                        j = j.replace("'", "")
                        if len(j.split()) > 1:
                            string = ""
                            for o in j.split():
                                if "!" in o or "?" in o or "." in o:
                                    o += "\n"
                                if "<" in o or ".at" in o or ".com" in o or "@" in o or len(o) > 15:
                                    o = ""
                                if len(o) > 1:
                                    string += f" {o}"
                            if len(string.split(" ")) > 2:
                                extracted_sentance.append(f"{string.strip()}")
    return extracted_sentance
