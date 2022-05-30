from gensim.models.phrases import Phrases, ENGLISH_CONNECTOR_WORDS
from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_short

import os
import json



# Train Baseline Model #

## Build corpus ##

### Get ALL json files with relevant data:
data_files = []
for file in os.listdir("data/"):
    if file.endswith(".json"):
        data_files.append(file)

### Read ALL files:
corpus_raw = []
for file in data_files:
    data_date = file.split("_")[0]
    dir_suffix = "data/"
    filename = f"{dir_suffix}{file}"
    with open(filename, "r", encoding="utf-8") as f:
        listings = json.load(f)
        for listing in listings:
            listing_dated = {**listing, "date": data_date}
            corpus_raw.append(listing_dated)

len(corpus_raw)
corpus_raw[0]

corpus_doc_list = []
for listing in corpus_raw:
    corpus_doc_list.append(listing["job_title"])
    corpus_doc_list.append(listing["job_description"])
len(corpus_doc_list)


CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation, strip_multiple_whitespaces]#, remove_stopwords, strip_short]
corpus_preprocessed = []
for doc in corpus_doc_list:
    doc_preprocessed = preprocess_string(doc, CUSTOM_FILTERS)
    corpus_preprocessed.append(doc_preprocessed)

len(corpus_preprocessed)
corpus_preprocessed[1]



mwe_bigram_model = Phrases(
    sentences=corpus_preprocessed,
    min_count=10,
    threshold=0,
    scoring="npmi",
    connector_words=ENGLISH_CONNECTOR_WORDS)
mwe_bigrams_export = mwe_bigram_model.export_phrases()


corpus_bigrams = []
for doc in corpus_preprocessed:
    doc_bigrams = mwe_bigram_model[doc]
    corpus_bigrams.append(doc_bigrams)
len(corpus_bigrams)
corpus_bigrams[1]

mwe_trigram_model = Phrases(
    sentences=corpus_bigrams,
    min_count=10,
    threshold=0,
    scoring="npmi",
    connector_words=ENGLISH_CONNECTOR_WORDS)
mwe_trigrams_export = mwe_trigram_model.export_phrases()

corpus_trigrams = []
for doc in corpus_bigrams:
    doc_trigrams = mwe_trigram_model[doc]
    corpus_trigrams.append(doc_trigrams)
len(corpus_trigrams)
corpus_trigrams[1]
