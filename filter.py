from nltk import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords

import embeddings_utils
import utils
def filtering_via_syntactic_and_semantic_information_replace(pert_sent, synonyms):
    """Filter sentences by synonyms and constituency structure for PaInv-Replace.
    Returns a dictionary of original sentence to list of filtered sentences
    """
    stopWords = list(set(stopwords.words('english')))
    syn_dic = {}
    filtered_sent = {}
    stemmer = SnowballStemmer("english")
    lemmatizer = WordNetLemmatizer()
    for original_sentence in list(pert_sent.keys()):
        # Create a dictionary from original sentence to list of filtered sentences
        filtered_sent[original_sentence] = []
        tokens_or = utils.tokenize(original_sentence)
        # Get lemma of each word of source sentence
        source_lem = [lemmatizer.lemmatize(each['token'], each['pos']) for each in utils.get_wordnet_pos(original_sentence)]
        new_sents = pert_sent[original_sentence]
        x = int(len(new_sents))
        for x in range(len(new_sents)):
            s = new_sents[x]
            target_lem = [lemmatizer.lemmatize(each['token'], each['pos']) for each in utils.get_wordnet_pos(s)]
            # If sentence is same as original sentence then filter that
            if s.lower()==original_sentence.lower():
                continue
            # If original sentence and generate sentence have same lemma, then filter
            if target_lem == source_lem:
                continue
            # Tokens of generated sentence
            tokens_tar = utils.tokenize(s)
            if len(tokens_tar)!=len(tokens_or):
                filtered_sent[original_sentence].append(s)
                continue
            for i in range(len(tokens_or)):
                if tokens_or[i]!=tokens_tar[i]:
                    word1 = tokens_or[i]
                    word2 = tokens_tar[i]
                    word1_stem = stemmer.stem(word1)
                    word2_stem = stemmer.stem(word2)
                    word1_base = WordNetLemmatizer().lemmatize(word1,'v')
                    word2_base = WordNetLemmatizer().lemmatize(word2,'v')
                    print(word1_base)
                    print(word2_base)
                    # If original word and predicted word have same stem, then filter
                    if word1_stem==word2_stem:
                        continue
                    # If they are synonyms of each other, the filter
                    syn1 = synonyms.get(word1_base,[word2_base])
                    syn2 = synonyms.get(word2_base,[word1_base])
                    if (word1 in syn2) or (word1_base in syn2) or (word2 in syn1) or (word2_base in syn1):
                        continue
                    if ((word1 in stopWords) or (word2 in stopWords) or (word1_stem in stopWords)
                        or (word2_stem in stopWords) or (word1_base in stopWords) or (word2_base in stopWords)):
                        continue
                    filtered_sent[original_sentence].append(s)
    return filtered_sent
def filter_by_sentence_embeddings(sentences_dic, threshold):
    """Filter sentence by ensuring similarity less than threshold
    Returns dictionary of original sentence to list og filtered sentences
    """
    filtered_sentences = {}
    for original_sentence in list(sentences_dic.keys()):
        filtered_sentences[original_sentence] = []
        generated_sents = sentences_dic[original_sentence]
        original_sentence_embed=embeddings_utils.get_embedding(original_sentence)
        for sent in generated_sents:
            sent_embed=embeddings_utils.get_embedding(sent)
            sim=embeddings_utils.cosine_similarity(original_sentence_embed, sent_embed)
            print(sim)
            if sim < threshold:
                filtered_sentences[original_sentence].append(sent)
    return filtered_sentences
