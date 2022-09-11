import spacy
from nltk.tokenize import sent_tokenize
import string
import re

nlp = spacy.load("en_core_web_sm")


# -------------------------------------------------------------------------------------------------------
# The sentences should be compared by similarity as well as the display must be better I am working on it
# -------------------------------------------------------------------------------------------------------


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


def grouping_sentences(input_, output_):
    # The function groups sentences between two persons, checks how many adjectives,
    # verbs and objects are in them and in what time they were sent.
    # And it will also group them by similarity
    with open(input_, "r", encoding="charmap") as data:
        data_lines = data.readlines()
        c = 0
        all_emails = []
        from_to_to_from = []
        for line in data_lines:
            if line != data_lines[0]:
                from_to = [line.split('",')[1], line.split('",')[2]]
                to_from = [line.split('",')[2], line.split('",')[1]]
                c += 1
                from_to_sentence = []
                if from_to not in from_to_to_from and to_from not in from_to_to_from:
                    for line_2 in data_lines:
                        try:
                            if line.split('",')[1] in line_2.split('",') and line.split('",')[2] in line_2.split('",'):
                                try:
                                    for sentance in sentence_extractor(line_2.split('",')[4]):
                                        if sentance not in from_to_sentence:
                                            from_to_sentence.append([line_2.split('",')[0], sentance])
                                    data_lines.remove(line_2)
                                except:
                                    pass
                        except:
                            pass
                    if from_to_sentence not in all_emails and from_to not in from_to_to_from and to_from\
                            not in from_to_to_from:
                        f_t = line.split('",')

                        with open(output_, "a", encoding="charmap") as n:
                            n.write(f"Email between: {f_t[1]}\n and\n {f_t[2]}\n\n\n")
                        for i in from_to_sentence:
                            doc = nlp(str(i))
                            PROPN = 0
                            VERB = 0
                            ADJ = 0
                            for token in doc:
                                if token.pos_ == "PROPN":
                                    PROPN += 1
                                elif token.pos_ == "VERB":
                                    VERB += 1
                                elif token.pos_ == "ADJ":
                                    ADJ += 1
                            print(i[0] + " " + i[1] + f" PROPN: {PROPN} VERB: {VERB} ADJ: {ADJ}\n")
                            with open(output_, "a", encoding="charmap") as n:
                                n.write(i[0] + "," + i[1] + "," + f" PROPN: {PROPN}, VERB: {VERB}, ADJ: {ADJ}" + "\n")
                        all_emails.append(from_to_sentence)
                        from_to_to_from.append(from_to)
                        from_to_to_from.append(to_from)


grouping_sentences("ex3.csv", "ex.txt")
