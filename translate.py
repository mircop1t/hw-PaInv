from google.cloud import translate_v2 as translate
source_language = 'en'
target_language = 'hi'
sent1="hello"
translate_client = translate.Client()
ref_translation = translate_client.translate(sent1, target_language=target_language,
                                                     source_language=source_language)['translatedText'].replace('&#39;',
                                                                                                                "'").replace(
            '&quot;', "'")
print(ref_translation)
def GoogleTranslate(filtered_sent, source_language, target_language):
    """Google Translate, visit https://cloud.google.com/translate/docs to know pre-requisites

    Arguments:
    filtered_sent = dictionary of original sentence to list of filtered sentences
    source_language = Source language code
    target_language = Target language code

    returns translation dictionary from source sentence to target sentence
    """
    translate_client = translate.Client()
    translation_dic = {}

    for sent in filtered_sent.keys():
        sent1 = sent.split("\n")[0]
        ref_translation = ""
        print(sent1)
        ref_translation = translate_client.translate(sent1, target_language=target_language,
                                                     source_language=source_language)['translatedText'].replace('&#39;',
                                                                                                                "'").replace(
            '&quot;', "'")
        translation_dic[sent] = ref_translation
        for new_s in filtered_sent[sent]:
            print('there')
            new_ref_translation = translate_client.translate(new_s, target_language=target_language,
                                                             source_language=source_language)['translatedText'].replace(
                '&#39;', "'").replace('&quot;', "'")
            translation_dic[new_s] = new_ref_translation
    return translation_dic

def collect_target_sentences(translator, filtered_sent, source_language, target_language, api_key=None):
    """Return Translation dic for a translator"""
    if translator == 'Google':
        return GoogleTranslate(filtered_sent, source_language, target_language)
