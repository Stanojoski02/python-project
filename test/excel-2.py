from nltk.tokenize import sent_tokenize
import re
import pandas
import numpy
import xlsxwriter


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
            if len(j.split()) >= 3:
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


def split_emails(input_):
    with open(input_, "r") as d:
        data = d.readlines()
        try_data = []
        c = 0
        for i in data:
            if "From:" in i or "Von:" in i:
                try_data.append(f"\nIndex: {c}\n")
                try_data.append(f"\n/#/\nf\nIndex: {c}\n")
                c += 1
            try_data.append(i)
        # for i in try_data:
        #     print(i)
        str_data = " ".join(try_data)
        emails_splited = str_data.split("/#/")
        return emails_splited


def for_to(email):
    for_to_ = ["", "", "", ""]
    email = email.splitlines()
    for i in email:
        if "From:" in i or "Von:" in i:
            for_to_[0] = i.strip().replace('ï»¿', '').replace("From:", "").replace("Von:", "")
        if "An:" in i or "To:" in i:
            for_to_[1] = i.strip().replace('ï»¿', '').replace("An:", "").replace("To:", "")
        if "Sent:" in i or "Gesendet:" in i:
            for_to_[2] = i.strip().replace('ï»¿', '').replace("Sent:", "").replace("Gesendet:", "")
        if "Index:" in i:
            for_to_[3] = i.replace("Index:", "")
    return for_to_


def email_sentences_with_index(emails):
    # This function, from a file containing email addresses,
    # divides them into a list,
    # extracts their sentences and writes them
    # into a file "sentence.txt"
    # with the index of the email they belong to
    txt = ""
    for k in split_emails(emails):
        from_to = for_to(k)
        for i in sentance_extractor(k):
            if len(k) > 0:
                # print(i.strip().replace("  ",""))
                txt += f"{from_to[3]} - {i.strip().replace('  ', '').replace('ï»¿', '')}".replace("\n", "")
                txt += "\n"
                print(f"{from_to[3]} - {i.strip().replace('  ', '').replace('ï»¿', '')}\n")
                print("_______________________")
    with open("sentence.txt", "w") as dd:
        dd.write(txt)
    return txt


def create_from_to_table(emails, output):
    db = pandas.DataFrame({"email_index": [for_to(emails[0])[3].replace("Sent:", "").replace(",", "\n").strip()],
                           "from": [for_to(emails[0])[0].replace("From: ", "").strip()],
                           "to": [for_to(emails[0])[1].replace("To:", "").replace(";", "\n").strip()],
                           "date_time": [for_to(emails[0])[2].replace("Sent:", "").replace(",", "\n").strip()],
                           })
    writer = pandas.ExcelWriter(output, engine='xlsxwriter')
    db = db[["email_index", "from", "to", "date_time"]]

    for email in emails:
        if for_to(email)[1]:
            print(for_to(email)[1])
            new_db = pandas.DataFrame({
                "email_index": [for_to(email)[3].strip()],
                "from": [for_to(email)[0].replace("From: ", "").strip()],
                "to": [for_to(email)[1].replace("To:", "").replace(";", "\n").strip()],
                "dateTime": [for_to(email)[2].replace("Sent:", "").replace(",", "\n").strip()],
            })
            db = pandas.concat([db, new_db], ignore_index=True, axis=0)
    db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
    worksheet = writer.sheets['Sheet1']
    (max_row, max_col) = db.shape
    column_settings = [{'header': column} for column in db.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
    worksheet.set_column(0, max_col - 1, 12)
    writer.save()
    print(db)


def jaccard_similarity(x, y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


def similarity_sorter(data_input, data_out):
    # sorts the sentences into groups according to their
    # similarity and shows the similarity to 3 decimal places
    q = 0
    try:
        with open(data_input, "r") as dd:
            data = dd.readlines()
            c = 0
            ca = []
            for i in data:
                g = 0
                r = []
                jaccard_ = []
                for j in data:
                    if jaccard_similarity(i.split(), j.split()) > 0.1:
                        if g == 0:
                            c += 1
                            g += 1
                        print(f"{c} - {j}")
                        if j not in r and j not in ca:
                            # if i not in r:
                            #     r.append(i)
                            samo = 0
                            for ui in r:
                                if ui.split() == j.split():
                                    samo = 1
                            if samo == 0:
                                r.append(j)
                                ca.append(j)
                                jaccard_.append(jaccard_similarity(i.split(), j.split()))
                try:
                    if len(r) >= 2:
                        with open(data_out, "a") as d:
                            for sas in range(len(r)):
                                d.write(f"{q} - {numpy.round(jaccard_[sas], 3)} - {r[sas]}")
                        q += 1
                except:
                    print("The file in which the data is to be entered was not found")
    except:
        print("The file that needs to sort sentences has not been found")


def create_table_with_sentence(input_, output_):
    with open(input_, "r") as d:
        data = d.readlines()
        db = pandas.DataFrame({
            "email_index": [data[0].split("-")[2]],
            "similarity_group": [data[0].split("-")[0]],
            "similarity": [data[0].split("-")[1]],
            "sentence": [
                ''.join(filter(lambda x: not x.isdigit(), data[0])).replace("-", "").strip().replace(".", "").strip()]
        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[["email_index", "similarity_group", "similarity", "sentence"]]

        for sentence in data:
            new_db = pandas.DataFrame({
                "email_index": [sentence.split("-")[2]],
                "similarity_group": [sentence.split("-")[0]],
                "similarity": [sentence.split("-")[1]],
                "sentence": [
                    ''.join(filter(lambda x: not x.isdigit(), sentence)).replace("-", "").replace(".", "").strip()]
            })
            db = pandas.concat([db, new_db], ignore_index=True, axis=0)
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()
        print(db)


def all_table_in_one():
    email_sentences_with_index("emails.txt")
    similarity_sorter("sentence.txt", "sorted_sentence.txt")
    create_from_to_table(split_emails("emails.txt"), "from_to_table.xlsx")
    create_table_with_sentence("sorted_sentence.txt", "table_with_sentence.xlsx")
