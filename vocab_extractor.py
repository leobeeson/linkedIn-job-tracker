from gensim.models.phrases import Phrases, FrozenPhrases, ENGLISH_CONNECTOR_WORDS
from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_short
from utils.stopwords import stopwords_english

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

### Extract text from which to extract MWE:
corpus_doc_list = []
for listing in corpus_raw:
    job_title = listing["job_title"]
    if job_title is not None:
        corpus_doc_list.append(job_title)
    job_description = listing["job_description"]
    if job_description is not None:
        corpus_doc_list.append(job_description)
len(corpus_doc_list)


### Tokenise and clean text:
CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation, strip_multiple_whitespaces]#, remove_stopwords, strip_short]
corpus_preprocessed = []
for doc in corpus_doc_list:
    doc_preprocessed = preprocess_string(doc, CUSTOM_FILTERS)
    corpus_preprocessed.append(doc_preprocessed)

len(corpus_preprocessed)
corpus_preprocessed[1]


### Train Bigrams model:
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


### Train Trigrams model:
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


## Filter MWE:
def identify_mwe_with_leading_and_trailing_stopwords(mwe_export: dict, stopwords: list) -> dict:
    mwe_blacklist = []
    for mwe in mwe_export:
        terms = mwe.split("_")
        if terms[0] in stopwords or terms[-1] in stopwords:
            mwe_blacklist.append(mwe)
    return mwe_blacklist

mwe_blacklist = identify_mwe_with_leading_and_trailing_stopwords(mwe_trigrams_export, stopwords_english["stopwords"])

mwe_trigram_frozen = mwe_trigram_model.freeze()


def remove_blacklisted_mwe(mwe: FrozenPhrases, blacklist: list) -> FrozenPhrases:
    for term in blacklist:
        try:
            del mwe.phrasegrams[term]
        except KeyError:
            print(f"MWE not in frozen model: {term}")
    return mwe

mwe_trigram_filtered = remove_blacklisted_mwe(mwe_trigram_frozen, mwe_blacklist)
mwe_trigram_filtered.phrasegrams

#TODO:
# Analyze software development-related MWE: How can we raise their signal?