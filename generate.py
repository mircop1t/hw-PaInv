import string

import nltk
import torch
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer, TreebankWordTokenizer
from transformers import BertTokenizer, BertForMaskedLM
import utils


stopWords = list(set(stopwords.words('english')))

def generate_syntactically_similar_sentences_replace(num_of_perturb, dataset):
    """Generate syntactically similar sentences for each sentence in the dataset.
    For PaInv-Replace
    Returns dictionary of original sentence to list of generated sentences
    """
    # Stopwords from nltk
    stopWords = list(set(stopwords.words('english')))

    # File from which sentences are read
    file = open(dataset, "r",encoding='utf-8')
    # Number of perturbations you want to make for a word in a sentence
    dic = {}
    num_of_perturb = 50
    num_sent = 0
    for line in file:
        s_list = line.split("\n")
        source_sent = s_list[0]
        # Generating new sentences using BERT
        new_sents = perturb(source_sent,num_of_perturb)
        #print(line)
        #print(new_sents)
        dic[line] = new_sents
        if new_sents != []:
            num_sent += 1
    return dic

def perturb(sent,num):
    """Generate a list of similar sentences by BERT
    Arguments:
    sentence: Sentence which needs to be perturbed
    bertModel: MLM model being used (BERT here)
    num: Number of perturbations required for a word in a sentence
    """
    # Tokenize the sentence
    pos_inf = utils.get_pos(sent)

    # the elements in the lists are tuples <index of token, pos tag of token>
    bert_masked_indexL = list()
    # collect the token index for substitution
    for idx, tag in enumerate(pos_inf):
        if (tag.startswith("JJ") or tag.startswith("JJR") or tag.startswith("JJS")
            or tag.startswith("PRP") or tag.startswith("PRP$") or  tag.startswith("RB")
            or tag.startswith("RBR") or tag.startswith("RBS") or tag.startswith("VB") or
            tag.startswith("VBD") or tag.startswith("VBG") or tag.startswith("VBN") or
            tag.startswith("VBP") or tag.startswith("VBZ") or tag.startswith("NN") or
            tag.startswith("NNS") or tag.startswith("NNP") or tag.startswith("NNPS")):

            tagFlag = tag[:2]

            if (idx!=0 and idx!=len(pos_inf)-1):
                bert_masked_indexL.append((idx, tagFlag))

    bert_new_sentences = list()
    # generate similar setences using Bert
    if bert_masked_indexL:
        bert_new_sentences = perturbBert(sent, num, bert_masked_indexL)
    for each in bert_new_sentences:
        print(each)
    print("================================================================================")
    return bert_new_sentences

import transformers.modeling_outputs
def perturbBert(sent, num, masked_indexL):
    """Generate a list of similar sentences by Bert

    Arguments:
    sent: sentence which need to be perturbed
    model: MLM model
    num: Number of perturbation for each word
    masked_indexL: List of indexes which needs to be perturbed
    """

    global num_words_perturb
    new_sentences = list()
    tokens = utils.tokenize(sent)
    # set of invalid characters
    invalidChars = set(string.punctuation)
    # for each idx, use Bert to generate k (i.e., num) candidate tokens
    for (masked_index, tagFlag) in masked_indexL:
        print(masked_index)
        original_word = tokens[masked_index]
        # Eliminating cases for "'s" as Bert does not work well on these cases.
        if original_word=="'s":
            continue
        # Eliminating cases of stopwords
        if original_word in stopWords:
            continue
        topk_tokens = utils.bert_predict_masked(sent,masked_index,num)
        #num_words_perturb += 1
        # Remove the tokens that only contains 0 or 1 char (e.g., i, a, s)
        topk_tokens = list(filter(lambda x:len(x)>1, topk_tokens))
        # Remove the cases where predicted words are synonyms of the original word or both words have same stem.
        # generate similar sentences
        for x in range(len(topk_tokens)):
            t = topk_tokens[x]
            if any(char in invalidChars for char in t):
                continue
            tokens[masked_index] = t
            new_sentence=utils.get_tokenizer().convert_tokens_to_string(tokens)
            new_pos_inf = utils.get_pos(new_sentence)
            # only use the similar sentences whose similar token's tag is still JJ, JJR, JJS, PRP, PRP$, RB, RBR, RBS, VB, VBD, VBG, VBN, VBP, VBZ, NN, NNP, NNS or NNPS
            if (new_pos_inf[masked_index].startswith(tagFlag)):
                new_sentences.append(new_sentence)
        tokens[masked_index] = original_word
    return new_sentences