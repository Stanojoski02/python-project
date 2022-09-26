import spacy
from nltk.tokenize import sent_tokenize
import string
import pandas
import math
import re
from collections import Counter
import pylev

nlp = spacy.load("en_core_web_sm")

from math import sqrt, pow, exp


def squared_sum(x):
    """ return 3 rounded square rooted value """

    return round(sqrt(sum([a * a for a in x])), 3)


def euclidean_distance(x, y):
    """ return euclidean distance between two lists """

    return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))


WORD = re.compile(r"\w+")


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


def cleaning(text):
    exclude = set(string.punctuation)
    exclude.remove('@')

    # remove new line and digits with regular expression
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\d', '', text)

    # remove patterns matching url format
    url_pattern = r'((http|ftp|https):\/\/)?[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&amp;:/\+#]*[\w\-\@?^=%&amp;/\+#])?'
    text = re.sub(url_pattern, ' ', text)

    # remove non-ascii characters, all below the ordinal coding of 8000 are allowed, so times all emojis gone
    text = ''.join(character for character in text if ord(character) < 8000)

    # remove punctuations # unfortunately the @ sign goes with it, so explicitly remove the @ sign from the
    # exclude list
    text = ''.join(character for character in text if character not in exclude)

    # standardize white space
    text = re.sub(r'\s+', ' ', text)

    # drop capitalization
    text = text.lower()
    # now remove all twitter usernames, they have the structure @username,
    # so explicitly leave the @ above to identify the usernames
    text = re.sub('@[^\s]+', '', text)

    # remove white space, this is the last step, because after removing the
    # usernames there are often empty characters left
    text = text.strip()

    return text


def sentence_extractor(string_):
    sentences_list = []
    data = sent_tokenize(string_)
    for sentence in data:
        txt = ""
        sentence = re.sub('<[^>]+>', '', sentence).strip()
        if "Von:" not in sentence and \
                "An:" not in sentence and \
                "From:" not in sentence and \
                "Web:" not in sentence and \
                len(sentence.split()) < 30:
            for word in sentence.split():
                if word[0].isalpha() and \
                        ("@" not in word) and \
                        (".com" not in word) and \
                        ("http" not in word) and \
                        ("www" not in word) and \
                        len(word) < 24:
                    pass
                else:
                    word = ""
                txt += " {}".format(word).replace(":", "")
        if txt and len(txt.split()) > 2 and (txt[-1] == "!" or txt[-1] == "." or txt[-1] == "?"):
            txt = cleaning(txt)
            sentences_list.append(txt.strip())
    return sentences_list


def sentence_formatting(_input, _output):
    with open(_input, "r", encoding="charmap") as data:
        data_lines = data.readlines()
        for line in data_lines:
            for i in sentence_extractor(line.split(",")[4]):
                doc = nlp(str(i))
                propn = 0
                verb = 0
                adj = 0
                noun = 0
                for token in doc:
                    if token.pos_ == "PROPN":
                        propn += 1
                    elif token.pos_ == "VERB":
                        verb += 1
                    elif token.pos_ == "ADJ":
                        adj += 1
                    elif token.pos_ == "NOUN":
                        noun += 1
                finished_line = f"" \
                                f"DateTime: {line.split(',')[0]}," \
                                f" From: {line.split(',')[1]}," \
                                f" To: {line.split(',')[2]}," \
                                f" Sentence:  {i.strip()}," \
                                f" PROPN: {propn}," \
                                f" VERB: {verb}," \
                                f" ADJ: {adj}," \
                                f" NOUN: {noun}\n"
                print(finished_line)
                with open(_output, "a", encoding="charmap") as a:
                    a.write(finished_line)


def grouping_sentences(_input, _output):
    sen = []
    with open(_input, "r", encoding="charmap") as d:
        data_lines = d.readlines()
        group = 0
        for line in data_lines:
            sentences = []
            for line_2 in data_lines:
                if jaccard_similarity(line.split(",")[3].split(), line_2.split(",")[3].split()) > 0.2:
                    if line_2.split(',')[3] not in sen:
                        try:
                            sentences.append(f""
                                             f"{jaccard_similarity(line.split(',')[3].split(), line_2.split(',')[3].split())},"
                                             f"{get_cosine(text_to_vector(line.split(',')[3]), text_to_vector(line_2.split(',')[3]))},"
                                             f"{pylev.levenshtein(line.split(',')[3].split(), line_2.split(',')[3].split())},"
                                             f"{euclidean_distance(nlp(line.split(',')[3]).vector, nlp(line_2.split(',')[3]).vector)},"
                                             f"{line_2}\n")
                            sen.append(line_2.split(',')[3])
                        except:
                            pass
            if len(sentences) > 1:
                for sentence in sentences:
                    with open(_output, "a", encoding="charmap") as writer:
                        writer.write(sentence)


def grouping_sentences_in_excel(input_, output_):
    with open(input_, "r", encoding="charmap") as d:
        sentences = d.readlines()
        print(sentences[0].split(",")[1])
        emails = [sentences[0].split(",")[5].replace('"', "").replace("From:", "").replace('"', "").strip().lower(),
                  sentences[0].split(",")[6].replace('"', "").replace("To:", "").replace('"', '').strip().lower()]
        db = pandas.DataFrame({
            "date":
                [sentences[0].split(",")[4].replace('"', "").replace("DateTime:", "")],
            "from": [
                emails.index(
                    sentences[0].split(",")[5].replace('"', "").replace("From:", "").replace('"', "").strip().lower()
                )
            ],
            "to": [
                emails.index(
                    sentences[0].split(",")[6].replace('"', "").replace("To:", "").replace('"', '').strip().lower()
                )
            ],
            "sentence": [sentences[0].split(",")[7].replace("Sentence:", "").strip()],
            "propn": [sentences[0].split(",")[8].replace("PROPN:", "")],
            "verb": [sentences[0].split(",")[9].replace("VERB:", "")],
            "adj": [sentences[0].split(",")[10].replace("ADJ:", "")],
            "noun": [sentences[0].split(",")[11].replace("NOUN:", "")],
            "jaccard_similarity": [sentences[0].split(",")[0]],
            "cosine_similarity": [sentences[0].split(",")[1]],
            "levenshtein_distance": [sentences[0].split(",")[2]],
            "euclidean_distance":[sentences[0].split(",")[3]]

        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[
            [
                "date", "from",
                "to", "sentence", "propn",
                "verb", "adj", "noun",
                "jaccard_similarity", "cosine_similarity",
                "levenshtein_distance", "euclidean_distance"
             ]
        ]
        num = 0
        for sentence in sentences:
            try:
                if sentences[0] != sentence:
                    email_1 = sentence.split(",")[5].replace('"', "").replace("From:", "").replace('"',
                                                                                                   '').strip().lower()
                    if ";" in email_1:
                        email_1 = email_1.split(';')[0].strip()
                    email_2 = sentence.split(",")[6].replace('"', "").replace("To:", "").replace('"',
                                                                                                 '').strip().lower()
                    if ";" in email_2:
                        email_2 = email_2.split(';')[0].strip()
                    if email_1 not in emails:
                        emails.append(email_1)
                    if email_2 not in emails:
                        emails.append(email_2)
                    new_db = pandas.DataFrame({
                        "date": [sentence.split(",")[4].replace('"', "").replace("DateTime:", "")],
                        "from": [
                            emails.index(email_1)
                        ],
                        "to": [
                            emails.index(email_2)
                        ],
                        "sentence": [sentence.split(",")[7].replace("Sentence:", "").strip()],
                        "propn": [sentence.split(",")[8].replace("PROPN:", "")],
                        "verb": [sentence.split(",")[9].replace("VERB:", "")],
                        "adj": [sentence.split(",")[10].replace("ADJ:", "")],
                        "noun": [sentence.split(",")[11].replace("NOUN:", "")],
                        "jaccard_similarity": [sentence.split(",")[0]],
                        "cosine_similarity": [sentence.split(",")[1]],
                        "levenshtein_distance": [sentence.split(",")[2]],
                        "euclidean_distance": [sentence.split(",")[3]]

                    })
                    db = pandas.concat([db, new_db], ignore_index=True, axis=0)
                    print(num)
                    num += 1
            except:
                pass
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()

        db_2 = pandas.DataFrame({
            "index": [emails.index(emails[0])],
            "email": [emails[0]]
        })
        new_writer = pandas.ExcelWriter("emails_index.xlsx", engine='xlsxwriter')
        db_2 = db_2[
            ["index", "email"]
        ]
        num = 0
        for email in emails:
            try:
                new_db_2 = pandas.DataFrame({
                    "index": [emails.index(email)],
                    "email": [email]
                })
                db_2 = pandas.concat([db_2, new_db_2], ignore_index=True, axis=0)
                print(num)
                num += 1
            except:
                pass
        db_2.to_excel(new_writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = new_writer.sheets['Sheet1']
        (max_row, max_col) = db_2.shape
        column_settings = [{'header': column} for column in db_2.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        new_writer.save()


def final_function(_input, _output):
    sentence_formatting(_input, "file.txt")
    grouping_sentences("file.txt", "sentence_in_groups.txt")
    grouping_sentences_in_excel("sentence_in_groups.txt", _output)
