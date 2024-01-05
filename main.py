import json
import pickle

import detect
import filter
import generate
import translate_youdao
import utils
from generate import perturb



dataset = "dataset/business"
num_of_perturb = 50
syntactically_similar_sentences = generate.generate_syntactically_similar_sentences_replace(num_of_perturb, dataset)
with open("data/bert_output_replace.json", 'w') as f:
    json.dump(syntactically_similar_sentences,f)

with open("data/bert_output_replace.json", 'r') as f:
    syntactically_similar_sentences=json.load(f)
# Load dictionary of synonyms for each word
with open("data/synonyms.dat", 'rb') as f:
    synonyms = pickle.load(f)
# Filtering by synonyms and filtering by constituency structure
filtered_sentences = filter.filtering_via_syntactic_and_semantic_information_replace(syntactically_similar_sentences,synonyms)
with open("data/first_filter.json", 'w') as f:
    json.dump(filtered_sentences, f)
threshold = 0.95    # Choose threshold for filtering
# Run install_USE.sh and install Universal sentence encoder before running the code below
filtered_sentences = filter.filter_by_sentence_embeddings(filtered_sentences, threshold)
with open("data/second_filter.json", 'w') as f:
    json.dump(filtered_sentences, f)


translated_sentences=translate_youdao.youdao_translate(filtered_sentences)
with open("data/filtered_sentences.json", 'w') as f:
    json.dump(translated_sentences, f)


with open("data/second_filter.json", 'r') as f:
    filtered_sentences=json.load(f)
with open("data/filtered_sentences.json", 'r') as f:
    translated_sentences=json.load(f)
detect.detecting_translation_errors(filtered_sentences,translated_sentences,"errors/youdao_error.txt")