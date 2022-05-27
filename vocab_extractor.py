from gensim.models.phrases import Phrases
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


CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_short]
corpus_preprocessed = []
for doc in corpus_doc_list:
    doc_preprocessed = preprocess_string(doc, CUSTOM_FILTERS)
    corpus_preprocessed.append(doc_preprocessed)

corpus_preprocessed[1]
