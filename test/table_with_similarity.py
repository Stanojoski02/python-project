import re
import pandas
import dateparser
import numpy
from collections import Counter
import math
from main import sent_tokenize


WORD = re.compile(r"\w+")


def sentence_extractor(string):
    sentences_list = []
    data = sent_tokenize(string)
    for sentence in data:
        txt = ""
        sentence = re.sub('<[^>]+>', '', sentence).strip()
        if "Von:" not in sentence and\
                "An:" not in sentence and\
                "From:" not in sentence and\
                "Web:" not in sentence and\
                len(sentence.split()) < 30:
            for word in sentence.split():
                if (word[0].isalpha() or word[0].isdigit()) and\
                        ("@" not in word) and\
                        (".com" not in word) and\
                        ("http" not in word) and\
                        ("www" not in word):
                    pass
                else:
                    word = ""
                txt += " {}".format(word).replace(":", "")
        if txt and len(txt.split()) > 2:
            print(txt.strip())
            sentences_list.append(txt.strip())
    return sentences_list


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


def jaccard_similarity(x, y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


def from_to_excel(input_, output_):
    with open(input_, "r", encoding='utf8') as d:
        data = d.readlines()
        index = 0
        db = pandas.DataFrame({
            "email_index": [index],
            "from": [data[0].split(",")[1]],
            "to": [" ".join(re.findall(r'[\w\.-]+@[\w\.-]+', data[0].split(",")[2])).lower().replace(" ", "")],
            "date_time": [dateparser.parse(data[0].split(",")[0])]
        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[["email_index", "from", "to", "date_time"]]

        for email in data:
            try:
                em_to = " ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[2])[0]).lower().replace(" ", "")
                if "-" in em_to:
                    em_to = em_to.split("-")[1]
            except:
                raise print(" ")

            if email != data[0]:
                new_db = pandas.DataFrame({
                    "email_index": [index],
                    "from": [", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower()],
                    "to": [em_to],
                    "date_time": [dateparser.parse(email.split(",")[0])]
                })
                index += 1
                print(index)
                db = pandas.concat([db, new_db], ignore_index=True, axis=0)
                if not ", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower():
                    print(email.split(",")[1])
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()
        print(db)


def from_to_excel(input_, output_):
    with open(input_, "r", encoding='utf8') as d:
        data = d.readlines()
        index = 0
        db = pandas.DataFrame({
            "email_index": [index],
            "from": [data[0].split(",")[1]],
            "to": [" ".join(re.findall(r'[\w\.-]+@[\w\.-]+', data[0].split(",")[2])).lower().replace(" ", "")],
            "date_time": [dateparser.parse(data[0].split(",")[0])]
        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[["email_index", "from", "to", "date_time"]]

        for email in data:
            em_to = ""
            try:
                em_to = " ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[2])[0]).lower().replace(" ", "")
                if "-" in em_to:
                    em_to = em_to.split("-")[1]

            except:
                print("bojan")

            if email != data[0]:
                new_db = pandas.DataFrame({
                    "email_index": [index],
                    "from": [", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower()],
                    "to": [em_to],
                    "date_time": [dateparser.parse(email.split(",")[0])]
                })
                index += 1
                print(index)
                db = pandas.concat([db, new_db], ignore_index=True, axis=0)
                if not ", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower():
                    print(email.split(",")[1])
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()
        print(db)


def email_sentences_with_index(emails):
    # This function, from a list containing email addresses,
    # divides them into a list,
    # extracts their sentences
    txt = ""
    email_index = 0
    for k in emails:
        k = " ".join(k.split('","')[4:])
        for i in sentence_extractor(k):
            if len(k) > 0:
                txt += f"{email_index} - {i.strip()}".replace("\n", "")
                txt += "\n"
        email_index += 1
    return txt


def similarity_sorter(data_input, data_out):
    # sorts the sentences into groups according to their
    # similarity and shows the similarity to 3 decimal places
    group = 0
    try:
        with open(data_input, "r", encoding='utf8') as dd:
            data = dd.readlines()
            c = 0
            ca = []
            for i in data:
                g = 0
                r = []
                jaccard_ = []
                cosine_ = []
                for j in data:
                    if jaccard_similarity(i.split("-")[1].split(), j.split("-")[1].split()) > 0.2:
                        if g == 0:
                            c += 1
                            g += 1
                        print(f"{c} - {j}")
                        if j not in r and j.split("-")[1] not in ca:
                            # if i not in r:
                            #     r.append(i)
                            samo = 0
                            for ui in r:
                                if ui.split() == j.split():
                                    samo = 1
                            if samo == 0:
                                r.append(j)
                                ca.append(j.split("-")[1])
                                jaccard_.append(jaccard_similarity(i.split(), j.split()))
                                cosine_.append(get_cosine(text_to_vector(i), text_to_vector(j)))
                try:
                    if len(r) >= 2:
                        with open(data_out, "a", encoding='utf8') as d:
                            for num in range(len(r)):
                                d.write(
                                    f"{group} - {numpy.round(jaccard_[num], 3)} - {numpy.round(cosine_[num], 3)} -"
                                    f" {r[num]}")
                        group += 1
                #         q = group
                except:
                    raise Exception
    except:
        raise Exception


def create_table_with_sentence(input_, output_):
    with open(input_, "r", encoding='utf8') as d:
        data = d.readlines()
        db = pandas.DataFrame({
            "similarity_group": [data[0].split("-")[0]],
            "email_index": [data[0].split("-")[3]],
            "JaccardSimilarity": [data[0].split("-")[1]],
            "CosineSimilarity": [data[0].split("-")[2]],
            "sentence": [
                ''.join(filter(lambda x: not x.isdigit(), data[0])).replace("-", "").strip().replace(".",
                                                                                                     "").strip()]
        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[["similarity_group", "email_index", "JaccardSimilarity", "CosineSimilarity", "sentence"]]

        for sentence in data:
            new_db = pandas.DataFrame({
                "similarity_group": [sentence.split("-")[0]],
                "email_index": [sentence.split("-")[3]],
                "JaccardSimilarity": [sentence.split("-")[1]],
                "CosineSimilarity": [sentence.split("-")[2]],
                "sentence": [
                    ''.join(filter(lambda x: not x.isdigit(), sentence)).replace("-", "").strip().replace(".",
                                                                                                          "").strip()]
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


def sentence_with_email_index(input_file):
    # This function write the sentences
    # that have the index of their email into a.txt file
    with open(input_file, "r", encoding="utf8") as d:
        data = d.readlines()
        with open("sentence_with_email_index.txt", "w", encoding='utf8') as dd:
            dd.write(email_sentences_with_index(data))


def final_function(input_file):
    sentence_with_email_index(input_file)
    similarity_sorter("sentence_with_email_index.txt", "sorted_sentence.txt")
    create_table_with_sentence("sorted_sentence.txt", "table_with_sentence_and_similarity.xlsx")
    from_to_excel(input_file, "from_to_table.xlsx")
