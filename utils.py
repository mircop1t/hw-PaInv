import torch
from transformers import RobertaTokenizer, pipeline, BertForMaskedLM, BertTokenizer, AutoModelForTokenClassification, \
    TokenClassificationPipeline, \
    AutoTokenizer, BertModel, RobertaModel, AutoModelForMaskedLM, RobertaForMaskedLM, RobertaForTokenClassification
from nltk.corpus import wordnet

pos_model_path="bert-base-multilingual-cased-pos-english/"
bert_model_path= "bert-base-cased"

bert=BertForMaskedLM.from_pretrained(bert_model_path)
berttokenizer=AutoTokenizer.from_pretrained(bert_model_path)
#
# robertatokenizer = AutoTokenizer.from_pretrained(bert_model_path)
# roberta=RobertaForMaskedLM.from_pretrained(bert_model_path)

# roberta.eval()
# pipe = pipeline("fill-mask", model=roberta, tokenizer=robertatokenizer)
token_classify_model=AutoModelForTokenClassification.from_pretrained(pos_model_path)
token_classify_tokenizer=AutoTokenizer.from_pretrained(pos_model_path)
pipeline = TokenClassificationPipeline(model=token_classify_model, tokenizer=berttokenizer)

def tokenize(sentence):
    return berttokenizer.tokenize(sentence)
def get_tokenizer():
    return berttokenizer
def get_model():
    return berttokenizer
def get_pos(sentence):
    if not type(sentence)  is str:
        sentence=bert.convert_tokens_to_string(sentence)
    data=pipeline(sentence)
    pos=[]
    for each in data:
        pos.append(each['entity'])
    return pos
# print(get_pos("this is a dog"))
# num=10
# sen="Hello I'm a <mask> model."
# print(pipe(sen))
# tokens=tokenize(sen)
# print(tokens)
# print(get_tokenizer().convert_tokens_to_ids(tokens))
# tokens_tensor = torch.tensor([get_tokenizer().convert_tokens_to_ids(tokens)])
# prediction = roberta(tokens_tensor)
#
# topk_Idx = torch.topk((prediction['logits'][0,4]), num)[1].tolist()
# print(topk_Idx)
# for each in get_tokenizer().convert_ids_to_tokens(topk_Idx):
#     if each.startswith("\u0120"):
#         each=each[1:]
#         print(each)

def get_wordnet_pos(sentence):
    """Get pos tags of words in a sentence"""
    """"return [{'token': 'They', 'pos': 'n'}]"""
    pos=get_pos(sentence)
    tokens=tokenize(sentence)
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    wordnet_pos=[]
    for i in range(0,len(tokens)):
        tag=pos[i]
        token=tokens[i]
        wordnet_pos.append({"token":token,"pos":tag_dict.get(tag[0:1], wordnet.NOUN)})
    return wordnet_pos

def roberta_predict_masked(sentence,masked_index,num):
    tokens=robertatokenizer.tokenize(sentence.lower())
    print(tokens)
    tokens[masked_index] = '<mask>'
    indexed_tokens = robertatokenizer.convert_tokens_to_ids(tokens)
    print(indexed_tokens)
    tokens_tensor = torch.tensor([indexed_tokens])
    prediction = roberta(tokens_tensor)
    topk_Idx = torch.topk((prediction['logits'][0, masked_index]), num)[1].tolist()
    print(robertatokenizer.convert_ids_to_tokens(topk_Idx))
    return robertatokenizer.convert_ids_to_tokens(topk_Idx)
    # print(topk_Idx)
    # for each in get_tokenizer().convert_ids_to_tokens(topk_Idx):
    #     if each.startswith("\u0120"):
    #         each = each[1:]
    #         print(each)
    #
def bert_predict_masked(sentence,masked_index,num):
    tokens = berttokenizer.tokenize(sentence.lower())
    print(tokens)
    tokens[masked_index] = '[MASK]'
    indexed_tokens = berttokenizer.convert_tokens_to_ids(tokens)
    print(indexed_tokens)
    tokens_tensor = torch.tensor([indexed_tokens])
    prediction = bert(tokens_tensor)
    topk_Idx = torch.topk((prediction['logits'][0, masked_index]), num)[1].tolist()
    print(berttokenizer.convert_ids_to_tokens(topk_Idx))
    return berttokenizer.convert_ids_to_tokens(topk_Idx)