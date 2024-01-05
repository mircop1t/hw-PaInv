import requests
import hashlib
import time
import uuid
import json
APP_KEY = '0a04ee53d5a5c590'
# 您的应用密钥
APP_SECRET = '5hrsHXRrbpkD858oT3m0V9giKyqftCrM'

def createRequest(sentence,lang_from='en',lang_to='zh-CHS'):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    lang_from = 'en'
    lang_to = 'zh-CHS'
    vocab_id = 'F2D34C9D62F04830A832B38B5647B628'

    data = {'q': sentence, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    print(str(res.content, 'utf-8'))
    return json.loads(str(res.content, 'utf-8'))['translation']

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)
def addAuthParams(appKey, appSecret, params):
    q = params.get('q')
    if q is None:
        q = params.get('img')
    q = "".join(q)
    salt = str(uuid.uuid1())
    curtime = str(int(time.time()))
    sign = calculateSign(appKey, appSecret, q, salt, curtime)
    params['appKey'] = appKey
    params['salt'] = salt
    params['curtime'] = curtime
    params['signType'] = 'v3'
    params['sign'] = sign

# def addAuthParams(appKey, appSecret, q):
#     salt = str(uuid.uuid1())
#     curtime = str(int(time.time()))
#     sign = calculateSign(appKey, appSecret, q, salt, curtime)
#     params = {'appKey': appKey,
#               'salt': salt,
#               'curtime': curtime,
#               'signType': 'v3',
#               'sign': sign}
#     return params

'''
    计算鉴权签名 -
    计算方式 : sign = sha256(appKey + input(q) + salt + curtime + appSecret)
    @param appKey    您的应用ID
    @param appSecret 您的应用密钥
    @param q         请求内容
    @param salt      随机值
    @param curtime   当前时间戳(秒)
    @return 鉴权签名sign
'''
def calculateSign(appKey, appSecret, q, salt, curtime):
    strSrc = appKey + getInput(q) + salt + curtime + appSecret
    return encrypt(strSrc)


def encrypt(strSrc):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(strSrc.encode('utf-8'))
    return hash_algorithm.hexdigest()


def getInput(input):
    if input is None:
        return input
    inputLen = len(input)
    return input if inputLen <= 20 else input[0:10] + str(inputLen) + input[inputLen - 10:inputLen]


def youdao_translate(filtered_sent):
    translation_dic={}
    for sent in filtered_sent.keys():
        if sent in translation_dic:
            continue
        sent1 = sent.split("\n")[0]
        ref_translation = createRequest(sent1)
        translation_dic[sent] = ref_translation
        for new_s in filtered_sent[sent]:
            new_ref_translation=createRequest(new_s)
            translation_dic[new_s] = new_ref_translation
            time.sleep(2)
    return translation_dic
# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == '__main__':
    createRequest()
