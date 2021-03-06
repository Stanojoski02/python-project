from nltk.tokenize import sent_tokenize
import re
import pandas
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
                try_data.append("\n/#/\n")
                c += 1
            try_data.append(i)
        # for i in try_data:
        #     print(i)
        str_data = " ".join(try_data)
        emails_splited = str_data.split("/#/")
        return emails_splited


def for_to(email):
    for_to_ = ["empty", "empty", "empty", "empty"]
    email = email.splitlines()
    for i in email:
        if "From:" in i or "Von:" in i:
            for_to_[0] = i.strip().replace('??????','').replace("From:", "").replace("Von:", "")
        if "An:" in i or "To:" in i:
            for_to_[1] = i.strip().replace('??????','').replace("An:", "").replace("To:", "")
        if "Sent:" in i or "Gesendet:" in i:
            for_to_[2] = i.strip().replace('??????','').replace("Sent:", "").replace("Gesendet:", "")
        if "Index:"in i:
            for_to_[3] = i.replace("Index:","")

    return for_to_


def final_func(emails):
    txt = ""
    for k in split_emails(emails):
        from_to = for_to(k)
        for i in from_to:
            if len(k) > 0:
                # print(i.strip().replace("  ",""))
                txt += f"{i.strip().replace('  ', '').replace('??????', '')}\n"
        if len(k.split()) > 0:
            # print("___________________________________")
            txt += "__________________________________\n"
        for i in sentance_extractor(k):
            if len(k) > 0:
                # print(i.strip().replace("  ",""))
                txt += f"{i.strip().replace('  ', '').replace('??????', '')}\n"
        if len(k) > 0:
            # print("\n\n")
            txt += "\n\n"
    return txt


def create_table(emails):
    db = pandas.DataFrame({"Index:": [for_to(emails[0])[3].replace("Sent:", "").replace(",", "\n").strip()],
                           "From:": [for_to(emails[0])[0].replace("From: ", "").strip()],
                           "To:": [for_to(emails[0])[1].replace("To:", "").replace(";", "\n").strip()],
                           "DateTime:": [for_to(emails[0])[2].replace("Sent:", "").replace(",", "\n").strip()],
                           })
    writer = pandas.ExcelWriter('pandas_table.xlsx', engine='xlsxwriter')
    db = db[["Index:","From:", "To:", "DateTime:"]]

    for email in emails:
        if email and email != "empty":
            print(for_to(email)[1])
            new_db = pandas.DataFrame({
                "Index:": [for_to(email)[3].strip()],
                "From:": [for_to(email)[0].replace("From: ", "").strip()],
                "To:": [for_to(email)[1].replace("To:", "").replace(";", "\n").strip()],
                "DateTime": [for_to(email)[2].replace("Sent:", "").replace(",", "\n").strip()],
                                       })
            db = pandas.concat([db, new_db], ignore_index=True, axis=0)
    db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    (max_row, max_col) = db.shape
    column_settings = [{'header': column} for column in db.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
    worksheet.set_column(0, max_col - 1, 12)
    writer.save()
    print(db)

create_table(split_emails("emails.txt"))
print(final_func("emails.txt"))
