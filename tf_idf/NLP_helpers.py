import nltk
from nltk import word_tokenize
import re, json, os
from nltk.stem import WordNetLemmatizer
from math import log
from nltk.corpus import brown
from string import punctuation

lemmatizer = WordNetLemmatizer()
sents = brown.sents()
punctuation += "``''--"
doc_vocabs = json.loads(open(os.path.dirname(__file__) + '\doc_vocabs.json').read())


def preproc(raw):
    raw = remove_spec_chars(raw)
    tokens = word_tokenize(raw)
    tokens = [tok for tok in tokens if tok not in punctuation and not tok.replace(',','').replace('.','').isdigit()]
    return [lemmatizer.lemmatize(tok.lower()) for tok in tokens]


def remove_spec_chars(string):
    string = re.sub('[^\w\s]', '', string)
    string = re.sub('_', '', string)
    string = re.sub('\s+', ' ', string)
    return string.strip()


def word_frequencies(words):
    counts = {}
    vocab = set(words)
    doc_length = float(len(words))
    for word in words:
        if word in counts.keys():
            counts[word] += 1
        else:
            counts[word] = 1.0
    return {word: counts[word]/doc_length for word in vocab}


def idf(vocab):
    doc_counts = {}
    for word in vocab:
        for doc in doc_vocabs:
            if word in doc_vocabs[doc]:
                if word in doc_counts.keys():
                    doc_counts[word] += 1
                else:
                    doc_counts[word] = 1.0
    return {word: log(len(doc_vocabs) / doc_counts[word]) for word in doc_counts.keys()}


def tf_idf(tfs, idfs):
    tf_idfs = {term: tfs[term] * idfs[term] for term in tfs.keys() if term in idfs.keys()}
    sorted_scores = sorted(tf_idfs.items(), key=lambda kv: kv[1])
    return reversed(sorted_scores)


if __name__ == '__main__':
    print(doc_vocabs["ca01"])

    # print(word_tokenize('I\'m'))

    # print("earlier :", lemmatizer.lemmatize("earlier", pos='a'))
    # print("translations :", lemmatizer.lemmatize("translations"))
    # print("rocks :", lemmatizer.lemmatize("rocks"))
    # print("corpora :", lemmatizer.lemmatize("corpora"))

    # a denotes adjective in "pos"
    # print("better :", lemmatizer.lemmatize("better", pos="a"))

    #print(idf(1000, ['test']))

#######################################################################
    # import json
    # dict = {}
    # for file in brown.fileids():
    #     words = brown.words(file)
    #     words = [tok for tok in words if tok not in punctuation]
    #     words = [tok for tok in words if
    #               tok not in punctuation and not tok.replace(',', '').replace('.', '').isdigit()]
    #     words = [lemmatizer.lemmatize(tok.lower()) for tok in words]
    #     dict[file] = list(set(words))
    # with open('doc_vocabs.json', 'w') as outfile:
    #     json.dump(dict, outfile)
######################################################################

# todo: remove numbers? DONE
# todo: remove stop words?
# todo: should lower be before lemmatize???
# todo: clean up punctuation better
# todo: lemmatizer is under-performing
# todo: n-grams for phrases??
