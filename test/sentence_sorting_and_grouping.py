import spacy
from nltk.tokenize import sent_tokenize
import string
import re
import pandas
import xlsxwriter


nlp = spacy.load("en_core_web_sm")


# -------------------------------------------------------------------------------------------------------
# The sentences should be compared by similarity as well as the display must be better I am working on it
# -------------------------------------------------------------------------------------------------------


def jaccard_similarity(x, y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


def Cleaning(text):
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

    # remove punctuations # unfortunately the @ sign goes with it, so explicitly remove the @ sign from the exclude list
    text = ''.join(character for character in text if character not in exclude)

    # standardize white space
    text = re.sub(r'\s+', ' ', text)

    # drop capitalization
    text = text.lower()
    # now remove all twitter usernames, they have the structure @username, so explicitly leave the @ above to identify the usernames
    text = re.sub('@[^\s]+', '', text)

    # remove white space, this is the last step, because after removing the usernames there are often empty characters left
    text = text.strip()

    return text


def sentence_extractor(string):
    sentences_list = []
    data = sent_tokenize(string)
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
            txt = Cleaning(txt)
            sentences_list.append(txt.strip())
    return sentences_list


def sentence_formatting(_input, _output):
    with open(_input, "r", encoding="charmap") as data:
        data_lines = data.readlines()
        for line in data_lines:
            for i in sentence_extractor(line.split(",")[4]):
                doc = nlp(str(i))
                PROPN = 0
                VERB = 0
                ADJ = 0
                NOUN = 0
                for token in doc:
                    if token.pos_ == "PROPN":
                        PROPN += 1
                    elif token.pos_ == "VERB":
                        VERB += 1
                    elif token.pos_ == "ADJ":
                        ADJ += 1
                    elif token.pos_ == "NOUN":
                        NOUN += 1
                finished_line = f"" \
                                f"DateTime: {line.split(',')[0]}," \
                                f" From: {line.split(',')[1]}," \
                                f" To: {line.split(',')[2]}," \
                                f" Sentence:  {i.strip()}," \
                                f" PROPN: {PROPN}," \
                                f" VERB: {VERB}," \
                                f" ADJ: {ADJ}," \
                                f" NOUN: {NOUN}\n"
                print(finished_line)
                with open(_output, "a", encoding="charmap") as a:
                    a.write(finished_line)


def grouping_sentences(_input, _output):
    sen = []
    with open(_input, "r", encoding="charmap") as d:
        data_lines = d.readlines()
        for line in data_lines:
            sentences = []
            for line_2 in data_lines:
                if jaccard_similarity(line.split(",")[3].split(), line_2.split(",")[3].split()) > 0.2:
                    if line_2.split(',')[3] not in sen:
                        sentences.append(f""
                                         f"{jaccard_similarity(line.split(',')[3].split(), line_2.split(',')[3].split())},"
                                         f" {line_2}\n")
                        sen.append(line_2.split(',')[3])
            if len(sentences) > 1:
                for sentence in sentences:
                    with open(_output, "a", encoding="charmap") as writer:
                        writer.write(sentence)


def grouping_sentences_in_excel(input_, output_):
    with open(input_, "r", encoding="charmap") as d:
        sentences = d.readlines()
        print(sentences[0].split(",")[1])
        db = pandas.DataFrame({
            "similarity": [sentences[0].split(",")[0]],
            "date": [sentences[0].split(",")[1].replace('"', "").replace("DateTime:", "")],
            "from": [sentences[0].split(",")[2].replace('"', "").replace("From:", "")],
            "to": [sentences[0].split(",")[3].replace('"', "").replace("To:", "")],
            "sentence": [sentences[0].split(",")[4].replace("Sentence:", "").strip()],
            "propn": [sentences[0].split(",")[5].replace("PROPN:", "")],
            "verb": [sentences[0].split(",")[6].replace("VERB:", "")],
            "adj": [sentences[0].split(",")[7].replace("ADJ:", "")],
            "noun": [sentences[0].split(",")[8].replace("NOUN:", "")]

        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[
            ["similarity", "date", "from",
             "to", "sentence", "propn", "verb", "adj", "noun"]
        ]
        num = 0
        for sentence in sentences:
            try:
                new_db = pandas.DataFrame({
                    "similarity": [sentence.split(",")[0]],
                    "date": [sentence.split(",")[1].replace('"', "").replace("DateTime:", "")],
                    "from": [sentence.split(",")[2].replace('"', "").replace("From:", "")],
                    "to": [sentence.split(",")[3].replace('"', "").replace("To:", "")],
                    "sentence": [sentence.split(",")[4].replace("Sentence:", "").strip()],
                    "propn": [sentence.split(",")[5].replace("PROPN:", "")],
                    "verb": [sentence.split(",")[6].replace("VERB:", "")],
                    "adj": [sentence.split(",")[7].replace("ADJ:", "")],
                    "noun": [sentence.split(",")[8].replace("NOUN:", "")]

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


def final_function(_input, _output):
    sentence_formatting(_input, "file.txt")
    grouping_sentences("file.txt", "sentence_in_groups.txt")
    grouping_sentences_in_excel("sentence_in_groups.txt",_output)
    
final_function("ex3.csv", "new.xlsx")

