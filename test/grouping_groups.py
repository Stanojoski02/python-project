import spacy
from nltk.tokenize import sent_tokenize
import string
import math
import re
from math import sqrt, pow
import sys
import sqlite3
import pandas as pd
import numpy
from tqdm import tqdm
import pylev
from collections import Counter


nlp = spacy.load("en_core_web_sm")


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
    email_num = 0
    data = pd.read_csv(_input, encoding='charmap')
    data_lines = data.values.tolist()
    line_num = 0
    print("sentence_formatting function is running")
    for line in data_lines:
        try:
            for i in sentence_extractor(line[4]):
                try:
                    if line_num % 500 == 0:
                        print(f"Formatted sentences {line_num}")
                    line_num += 1
                    doc = nlp(str(i))
                    propn = 0
                    #               propn: proper noun
                    verb = 0
                    #               verb:  Word used to describe an action
                    adj = 0
                    #               adjective: A word naming an attribute of a noun, such as sweet, red
                    noun = 0
                    #               noun: A word used to identify any of a class of people, places, or things
                    for token in doc:
                        if token.pos_ == "PROPN":
                            propn += 1
                        elif token.pos_ == "VERB":
                            verb += 1
                        elif token.pos_ == "ADJ":
                            adj += 1
                        elif token.pos_ == "NOUN":
                            noun += 1
                    finished_line = f"{email_num}," \
                                    f"DateTime: {line[0]}," \
                                    f" From: {line[1]}," \
                                    f" To: {line[2]}," \
                                    f" Sentence:  {i.strip()}," \
                                    f" PROPN: {propn}," \
                                    f" VERB: {verb}," \
                                    f" ADJ: {adj}," \
                                    f" NOUN: {noun}," \
                                    f"{line[3]}\n"
                    with open(_output, "a", encoding="charmap") as a:
                        a.write(finished_line)
                except:
                    pass
        except:
            pass
        email_num += 1


def write_sentences_in_sqlite(input_, output_):
    print("write_sentences_in_sqlite function is running")

    with open(input_, "r", encoding="charmap") as d:
        if str(type(input_)) == "<class 'list'>":
            sentences = input_
        else:
            sentences = d.readlines()

        emails = []
        data = []
        email_1 = ""
        for sentence in sentences:
            try:
                if sentence.split(",") != ['\n']:
                    try:
                        email_1 = sentence.strip().split(",")[7].replace('"', "").replace("From:", "").replace('"',
                                                                                                               '').strip().lower()

                        if ";" in email_1:
                            email_1 = email_1.split(';')[0].strip()
                        email_2 = sentence.split(",")[8].replace('"', "").replace("To:", "").replace('"',
                                                                                                     '').strip().lower()
                        if ";" in email_2:
                            email_2 = email_2.split(';')[0].strip()
                        if email_1 not in emails:
                            emails.append(email_1)
                        if email_2 not in emails:
                            emails.append(email_2)
                        if [
                            sentence.split(",")[0].replace('"', ""),
                            sentence.split(",")[6].replace('"', "").replace("DateTime:", ""),
                            "EMID" + str(sentence.split(",")[0].replace('"', "")),
                            emails.index(email_1),
                            emails.index(email_2),
                            sentence.split(",")[9].replace("Sentence:", "").strip(),
                            sentence.split(",")[10].replace("PROPN:", ""),
                            sentence.split(",")[11].replace("VERB:", ""),
                            sentence.split(",")[12].replace("ADJ:", ""),
                            sentence.split(",")[13].replace("NOUN:", ""),
                            numpy.round(float(sentence.split(",")[1]), 4),
                            numpy.round(float(sentence.split(",")[2]), 4),
                            sentence.split(",")[3],
                            numpy.round(float(sentence.split(",")[4]), 4),
                            int(sentence.split(",")[-1])
                        ] not in data:
                            data.append([
                                sentence.split(",")[0].replace('"', ""),
                                sentence.split(",")[6].replace('"', "").replace("DateTime:", ""),
                                "EMID" + str(sentence.split(",")[0].replace('"', "")),
                                emails.index(email_1),
                                emails.index(email_2),
                                sentence.split(",")[9].replace("Sentence:", "").strip(),
                                sentence.split(",")[10].replace("PROPN:", ""),
                                sentence.split(",")[11].replace("VERB:", ""),
                                sentence.split(",")[12].replace("ADJ:", ""),
                                sentence.split(",")[13].replace("NOUN:", ""),
                                numpy.round(float(sentence.split(",")[1]), 4),
                                numpy.round(float(sentence.split(",")[2]), 4),
                                sentence.split(",")[3],
                                numpy.round(float(sentence.split(",")[4]), 4),
                                int(sentence.split(",")[-1])
                            ])
                    except:
                        pass
            except:
                pass

        df = pd.DataFrame(data, columns=[
            "ID", "date", "email_id", "from(email index)",
            "to(email index)", "sentence", "propn", "verb",
            "adjective", "noun", "jaccard_similarity",
            "cosine_similarity", "levenshtein_distance",
            "euclidean_distance", "group_id"
        ])

        conn = sqlite3.connect(output_)
        df.to_sql(f"tbl_sentence", conn, if_exists="replace", index=False)
        conn.close()
        ID = 1
        number_of_emails = 0

        # Connect to the SQLite database
        conn = sqlite3.connect(output_)
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS tbl_email_address (
                ID INTEGER,
                email TEXT
            )
        ''')

        # Insert the emails into the table
        for email in emails:
            try:
                if email != emails[0]:
                    if number_of_emails % 100 == 0:
                        print(f"{number_of_emails} email addresses are recorded")
                    number_of_emails += 1
                    cursor.execute(f"INSERT INTO tbl_email_address (ID, email) VALUES (?, ?)", (ID, email))
                    ID += 1
            except:
                pass

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        sentence_list = []
        email_ids = []
        ID = 0

        # Connect to the database
        conn = sqlite3.connect(output_)
        cursor = conn.cursor()

        # Create the email table if it doesn't exist
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS tbl_email (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT NOT NULL,
            email_date TEXT NOT NULL,
            email_time TEXT NOT NULL,
            email_subject TEXT,
            from_id INTEGER NOT NULL,
            to_id INTEGER NOT NULL,
            body TEXT NOT NULL
        )
        """)

        # Iterate over the sentences
        for sentence in sentences:
            sentence_list = []
            email_id = sentence.split(",")[0].replace('"', "")
            if email_id not in email_ids:
                email_ids.append(email_id)
            try:
                for s in sentences:
                    s_email_id = s.split(",")[0].replace('"', "")
                    if s_email_id == email_id and s.split(",")[9].replace("Sentence:", "").strip() not in sentence_list:
                        sentence_list.append(s.split(",")[9].replace("Sentence:", "").strip())
                email_1 = sentence.split(",")[7].replace('"', "").replace("From:", "").replace('"', '').strip().lower()
                email_1 = email_1.split(';')[0].strip() if ";" in email_1 else email_1
                email_2 = sentence.split(",")[8].replace('"', "").replace("To:", "").replace('"', '').strip().lower()
                email_2 = email_2.split(';')[0].strip() if ";" in email_2 else email_2
                subject = sentence.split(",")[14] if len(sentence.split(",")) > 14 else ''
                body = str(sentence_list).replace("]", "").replace("[", "")
                email_date = sentence.split(",")[6].replace('"', "").replace("DateTime:", "").split()[0]
                email_time = sentence.split(",")[6].replace('"', "").replace("DateTime:", "").split()[1]
                # Insert the email data into the database
                try:
                    cursor.execute(f"""
                    INSERT INTO tbl_email (email_id, email_date, email_time, email_subject, from_id, to_id, body)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        "EMID" + email_id, email_date, email_time, subject, emails.index(email_1),
                        emails.index(email_2),
                        body))
                    ID += 1
                except:
                    pass
            except:
                pass
        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()

        # Insert the emails into the table
        for email in emails:
            try:
                if email != emails[0]:
                    if number_of_emails % 100 == 0:
                        print(f"{number_of_emails} email addresses are recorded")
                    number_of_emails += 1
                    cursor.execute(f"INSERT INTO tbl_email_address (ID, email) VALUES (?, ?)", (ID, email))
                    ID += 1
            except:
                pass

        # Commit the changes and close the connection
        try:
            conn.commit()
        except:
            pass
        try:
            conn.close()
        except:
            pass
        sentence_list = []
        email_ids = []
        ID = 0

        # Connect to the database
        conn = sqlite3.connect(output_)
        cursor = conn.cursor()

        # Create the email table if it doesn't exist
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS tbl_email (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT NOT NULL,
            email_date TEXT NOT NULL,
            email_time TEXT NOT NULL,
            email_subject TEXT,
            from_id INTEGER NOT NULL,
            to_id INTEGER NOT NULL,
            body TEXT NOT NULL
        )
        """)

        # Iterate over the sentences
        for sentence in sentences:
            sentence_list = []
            email_id = sentence.split(",")[0].replace('"', "")
            if email_id not in email_ids:
                email_ids.append(email_id)
            for s in sentences:
                try:
                    s_email_id = s.split(",")[0].replace('"', "")
                    if s_email_id == email_id and s.split(",")[9].replace("Sentence:", "").strip() not in sentence_list:
                        sentence_list.append(s.split(",")[9].replace("Sentence:", "").strip())
                except:
                    pass
            try:
                email_1 = sentence.split(",")[7].replace('"', "").replace("From:", "").replace('"', '').strip().lower()
                email_1 = email_1.split(';')[0].strip() if ";" in email_1 else email_1
                email_2 = sentence.split(",")[8].replace('"', "").replace("To:", "").replace('"', '').strip().lower()
                email_2 = email_2.split(';')[0].strip() if ";" in email_2 else email_2
                subject = sentence.split(",")[14] if len(sentence.split(",")) > 14 else ''
                body = str(sentence_list).replace("]", "").replace("[", "")
                email_date = sentence.split(",")[6].replace('"', "").replace("DateTime:", "").split()[0]
                email_time = sentence.split(",")[6].replace('"', "").replace("DateTime:", "").split()[1]
                # Insert the email data into the database
                cursor.execute(f"""
                INSERT INTO tbl_email (email_id, email_date, email_time, email_subject, from_id, to_id, body)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    "EMID" + email_id, email_date, email_time, subject, emails.index(email_1), emails.index(email_2),
                    body))
                ID += 1
            except:
                pass

        # Commit the changes to the database and close the connection
        try:
            conn.commit()
        except:
            conn.close()


def communication_streams(output_):
    conn = sqlite3.connect(output_)
    data = pd.read_sql(f"SELECT * FROM tbl_email", conn)
    list_of_emails = data.values.tolist()
    sorted_list = []
    com_s = 0
    sorted_communication_stream = []
    for i in list_of_emails:
        try:
            for j in list_of_emails:
                if (i[5] == j[5] or j[5] == j[6]) and (i[6] == j[5] or i[6] == j[6]) and j[
                    1] not in sorted_communication_stream:
                    sorted_list.append((com_s, j))
                    sorted_communication_stream.append(j[1])
            com_s += 1
        except:
            pass

    db = pd.DataFrame({
        "id": [sorted_list.index(sorted_list[0])],
        "comm_stream_id": ["COMM" + str(sorted_list[0][0])],
        "email_id": [sorted_list[0][1][1]]
    })

    for comunication_stream in sorted_list:
        if comunication_stream != sorted_list[0]:
            try:
                new_db = pd.DataFrame({
                    "id": [sorted_list.index(comunication_stream)],
                    "comm_stream_id": ["COMM" + str(comunication_stream[0])],
                    "email_id": [comunication_stream[1][1]],
                })
                db = pd.concat([db, new_db], ignore_index=True, axis=0)
            except:
                pass
    try:
        db.to_sql(f"tbl_communication_streams", conn, if_exists="replace", index=False)
    except:
        raise Exception


def old_sentence_formatting(_input, _output):
    email_num = 0
    with open(_input, "r", encoding="charmap") as data:
        data_lines = data.readlines()
        line_num = 0
        print("sentence_formatting function is running")
        for line in data_lines:
            try:
                for i in sentence_extractor(line.split(",")[4]):
                    try:
                        if line_num % 500 == 0:
                            print(f"Sorted and formatted sentences {line_num}")
                        line_num += 1
                        doc = nlp(str(i))
                        propn = 0
                        #               propn: proper noun
                        verb = 0
                        #               verb:  Word used to describe an action
                        adj = 0
                        #               adjective: A word naming an attribute of a noun, such as sweet, red
                        noun = 0
                        #               noun: A word used to identify any of a class of people, places, or things
                        for token in doc:
                            if token.pos_ == "PROPN":
                                propn += 1
                            elif token.pos_ == "VERB":
                                verb += 1
                            elif token.pos_ == "ADJ":
                                adj += 1
                            elif token.pos_ == "NOUN":
                                noun += 1
                        finished_line = f"{email_num}," \
                                        f"DateTime: {line.split(',')[0]}," \
                                        f" From: {line.split(',')[1]}," \
                                        f" To: {line.split(',')[2]}," \
                                        f" Sentence:  {i.strip()}," \
                                        f" PROPN: {propn}," \
                                        f" VERB: {verb}," \
                                        f" ADJ: {adj}," \
                                        f" NOUN: {noun}," \
                                        f"{line.split(',')[3]}\n"
                        with open(_output, "a", encoding="charmap") as a:
                            a.write(finished_line)
                    except:
                        pass
            except:
                pass
            email_num += 1


def new_grouping_sentences(_input, _output):
    sen = set()
    counter = Counter()
    group_id = 1 # initialize group id
    with open(_input, "r", encoding="charmap") as d, open(_output, "w", encoding="charmap") as writer:
        data_lines = d.readlines()
        sentences = []
        for i in tqdm(range(len(data_lines))):
            line = data_lines[i]
            if line.split(",")[4] not in sen:
                try:
                    sentence = "{},{:.4f},{:.4f},{},{:.4f},{},{}\n".format(
                        line.split(',')[0],
                        1.0,
                        get_cosine(text_to_vector(line.split(',')[4]), text_to_vector(line.split(',')[4])),
                        0,
                        euclidean_distance(nlp(line.split(',')[4]).vector, nlp(line.split(',')[4]).vector),
                        line,
                        group_id).replace("\n"," ") + "\n"# add group_id at the end of the sentence
                    sentences.append(sentence)
                    sen.add(line.split(',')[4])
                except:
                    pass

                for j in range(i + 1, min(i + 501, len(data_lines))):
                    line_2 = data_lines[j]
                    if jaccard_similarity(line.split(",")[4].split(), line_2.split(",")[4].split()) > 0.5:
                        if line_2.split(',')[4] not in sen:
                            try:
                                if len(sentences) == 0:
                                    sentence = "{},{:.4f},{:.4f},{},{:.4f},{},{}\n".format(
                                        line_2.split(',')[0],
                                        1.0,
                                        get_cosine(text_to_vector(line.split(',')[4]),
                                                   text_to_vector(line_2.split(',')[4])),
                                        pylev.levenshtein(line.split(',')[4].split(), line_2.split(',')[4].split()),
                                        euclidean_distance(nlp(line.split(',')[4]).vector,
                                                           nlp(line_2.split(',')[4]).vector),
                                        line_2,
                                        group_id) # add group_id at the end of the sentence
                                else:
                                    sentence = "{},{:.4f},{:.4f},{},{:.4f},{},{}\n".format(
                                        line_2.split(',')[0],
                                        jaccard_similarity(line.split(',')[4].split(), line_2.split(',')[4].split()),
                                        get_cosine(text_to_vector(line.split(',')[4]),
                                                   text_to_vector(line_2.split(',')[4])),
                                        pylev.levenshtein(line.split(',')[4].split(), line_2.split(',')[4].split()),
                                        euclidean_distance(nlp(line.split(',')[4]).vector,
                                                           nlp(line_2.split(',')[4]).vector),
                                        line_2,
                                        group_id).replace("\n"," ") + "\n" # add group_id at the end of the sentence
                                sentences.append(sentence)
                                sen.add(line_2.split(',')[4])
                            except:
                                pass
            if len(sentences) > 2:
                for sentence in sentences:
                    writer.write(sentence)
                    counter.update({'count': 1})
                group_id += 1 # increment group_id after recording a group
            sentences = []
    print("grouping_sentences function is done")
    
from tqdm import tqdm

def new_grouping_groups(_input, _output):
    with open(_input, "r", encoding="charmap") as f:
        lines = f.readlines()
    # Group the sentences by their group_id
    groups = {}
    for line in lines:
        group_id = line.split(',')[-1].strip()
        if group_id not in groups:
            groups[group_id] = []
        groups[group_id].append(line)
    # Merge similar groups
    threshold = 0. # adjust this threshold as needed
    merged_groups = []
    to_remove = set()
    for group_id_1, sentences_1 in groups.items():
        if group_id_1 in to_remove:
            continue
        for group_id_2, sentences_2 in groups.items():
            if group_id_2 in to_remove:
                continue
            if group_id_1 == group_id_2:
                continue
            similarity = jaccard_similarity(sentences_1[0].split(',')[5].split(), sentences_2[0].split(',')[5].split())
            if similarity > threshold:
                merged_group = sentences_1 + sentences_2
                merged_groups.append(merged_group)
                to_remove.add(group_id_1)
                to_remove.add(group_id_2)
                break
    for group_id in to_remove:
        del groups[group_id]
    with open(_output, "w", encoding="charmap") as f:
        num_groups = len(groups) + len(merged_groups)
        num_processed = 0
        for group_id, sentences in tqdm(groups.items(), desc="Writing groups", total=len(groups)):
            for sentence in sentences:
                f.write(sentence)
            num_processed += 1
            tqdm.write(f"Processed {num_processed}/{num_groups} groups")
        for merged_group in tqdm(merged_groups, desc="Writing merged groups", total=len(merged_groups)):
            for sentence in merged_group:
                f.write(sentence)
            num_processed += 1
            tqdm.write(f"Processed {num_processed}/{num_groups} groups")

    print("new_grouping_groups function is done")



    
    
def final_function(_input, working_file_with_formated_sentences, working_file_sorted_sentences, db_name):
#     try:
#         sentence_formatting(_input, working_file_with_formated_sentences)
#     except:
#         old_sentence_formatting(_input, working_file_with_formated_sentences)
    print("The new_grouping_sentences function just started")
    new_grouping_sentences(working_file_with_formated_sentences, working_file_sorted_sentences)
#     write_sentences_in_sqlite(sentence_in_groups, db_name)
#     print("The communication_streams function just started")
#     communication_streams(db_name)


data_with_emails = "emails.csv"
formated_sentence = "formated_sentence.csv"
sentence_in_groups = "my_sentences_in_groupss.csv"
db_name = "db_name.db"
print("A")
# final_function(data_with_emails, formated_sentence, sentence_in_groups, db_name)
new_grouping_groups("my_sentences_in_groupss.csv", "my_sentences_in_groupssss.csv")
