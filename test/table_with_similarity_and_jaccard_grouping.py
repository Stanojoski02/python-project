import re
import pandas
import dateparser
import numpy
from collections import Counter
import math
from nltk.tokenize import sent_tokenize

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
                        ("www" not in word) and\
                        len(word) < 24:
                    pass
                else:
                    word = ""
                txt += " {}".format(word).replace(":", "")
        if txt and len(txt.split()) > 2:
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
    with open(input_, "r", encoding="charmap") as d:
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
                db = pandas.concat([db, new_db], ignore_index=True, axis=0)
                # if not ", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower():
                #     print(email.split(",")[1])
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()


def from_to_excel(input_, output_):
    with open(input_, "r", encoding="charmap") as d:
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
                # print(index)
                db = pandas.concat([db, new_db], ignore_index=True, axis=0)
                # if not ", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower():
                #     print(email.split(",")[1])
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()
        # print(db)


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
        with open(data_input, "r", encoding="charmap") as dd:
            data = dd.readlines()
            c = 0
            all_sentence = []
            sentence_index = 0
            for line in data:
                g = 0
                similarity_sentence_group = []
                jaccard_ = []
                cosine_ = []
                for line_2 in data:
                    if jaccard_similarity(line.split("-")[1].split(), line_2.split("-")[1].split()) > 0.4:
                        if g == 0:
                            c += 1
                            g += 1
                        if line_2.split() not in similarity_sentence_group and line_2.split("-")[1] not in all_sentence:
                            samo = 0
                            for sentence in similarity_sentence_group:
                                if sentence.split() == line_2.split() and line_2 in all_sentence:
                                    samo = 1
                            if samo == 0:
                                similarity_sentence_group.append(line_2)
                                all_sentence.append(line_2.split("-")[1])
                                jaccard_.append(jaccard_similarity(line.split(), line_2.split()))
                                cosine_.append(get_cosine(text_to_vector(line), text_to_vector(line_2)))
                try:
                    if len(similarity_sentence_group) >= 2:
                        with open(data_out, "a", encoding="charmap") as d:
                            for num in range(len(similarity_sentence_group)):
                                d.write(
                                    f"{sentence_index} - {group} - {numpy.round(jaccard_[num], 3)} - {numpy.round(cosine_[num], 3)} -"
                                    f" {similarity_sentence_group[num]}")
                                sentence_index += 1
                        group += 1
                except:
                    raise Exception
    except:
        raise Exception


def create_table_with_sentence(input_, output_):
    with open(input_, "r", encoding="charmap") as d:
        data = d.readlines()
        db = pandas.DataFrame({
            "similarity_group": [data[0].split("-")[1]],
            "sentence_index":[data[0].split("-")[0]],
            "email_index": [data[0].split("-")[4]],
            "jaccard_similarity": [data[0].split("-")[2]],
            "cosine_similarity": [data[0].split("-")[3]],
            "sentence": [
                ''.join(filter(lambda x: not x.isdigit(), data[0])).replace("-", "").strip().replace(".",
                                                                                                     "").strip()]
        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[
            ["similarity_group", "sentence_index", "email_index", "jaccard_similarity", "cosine_similarity", "sentence"]
        ]
        num = 0
        for sentence in data:
            if sentence != data[0]:
                new_db = pandas.DataFrame({
                    "similarity_group": [sentence.split("-")[1]],
                    "sentence_index":[sentence.split("-")[0]],
                    "email_index": [sentence.split("-")[4]],
                    "jaccard_similarity": [sentence.split("-")[2]],
                    "cosine_similarity": [sentence.split("-")[3]],
                    "sentence": [
                        ''.join(filter(lambda x: not x.isdigit(), sentence)).replace("-", "").strip().replace(".",
                                                                                                              "").strip()]
                })
                db = pandas.concat([db, new_db], ignore_index=True, axis=0)
                print(num)
                num+=1
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()
        # print(db)


def sentence_with_email_index(input_file):
    # This function write the sentences
    # that have the index of their email into input_file file
    with open(input_file, "r", encoding="charmap") as d:
        data = d.readlines()
        with open("sentence_with_email_index.txt", "w", encoding="charmap" ) as dd:
            dd.write(email_sentences_with_index(data))


def final_function(input_file):
    sentence_with_email_index(input_file)
    similarity_sorter("sentence_with_email_index.txt", "sorted_sentence.txt")
    create_table_with_sentence("sorted_sentence.txt", "table_with_sentence_and_similarity22.xlsx")
    from_to_excel(input_file, "from_to_table.xlsx")


final_function("emails2.txt")
