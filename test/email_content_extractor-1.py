from nltk.tokenize import sent_tokenize
import re

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
            if (len(j.split()) >= 3):
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
                                    o=""
                                if len(o) > 1:
                                    string += f" {o}"
                            if len(string.split(" ")) > 2:
                                extracted_sentance.append(f"{string.strip()}")
    return extracted_sentance

def split_emails(input_):
    with open(input_, "r") as d:
        data = d.readlines()
        try_data =[]
        for i in data:
            if "From:" in i or "Von:" in i:
                try_data.append("\n/#/\n")
            try_data.append(i)
        # for i in try_data:
        #     print(i)
        str_data = " ".join(try_data)
        emails_splited = str_data.split("/#/")
        return emails_splited





def for_to(email):
    for_to_ = []
    email = email.splitlines()
    for i in email:
        if "From:" in i or "Von:" in i:
            for_to_.append(i.strip())
        if "An:" in i or "To:" in i:
            for_to_.append(i.strip())
    return for_to_


def final_func(emails):
    txt = ""
    for k in split_emails(emails):
        from_to = for_to(k)
        for i in from_to:
            if len(k) > 0:
                # print(i.strip().replace("  ",""))
                txt += f"{i.strip().replace('  ','').replace('ï»¿','')}\n"
        if len(k.split())>0:
            # print("___________________________________")
            txt += "__________________________________\n"
        for i in sentance_extractor(k):
            if len(k) > 0:
                # print(i.strip().replace("  ",""))
                txt += f"{i.strip().replace('  ', '').replace('ï»¿','')}\n"
        if len(k)>0:
            # print("\n\n")
            txt += "\n\n"
    return txt



