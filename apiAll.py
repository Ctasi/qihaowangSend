import requests
import json
import taskModel

website = 'http://www.qihaonet.com'
website_keyword = 'http://www.qihaonet.com'

def Login_in(username,password,taskId):
    print(username)
    try:
        response = requests.post(url='{}/shop/api/login'.format(website), data={"userName": '{}'.format(username), "userPwd": '{}'.format(password), "taskId": '{}'.format(taskId)})
        result = json.loads(response.content)
        print(result)
        return result
    except Exception as e:
        print(e)
        return {'errno':1}


def getOption(token):
    try:
        sess = requests.session()
        response = sess.post(url='{}/shop/api/basicParams'.format(website),
                             data={"token": token})
        # js = json.loads(res.text)
        return json.loads(response.content)
    except Exception as e:
        print(e)
        return {'errno':1}

def getProductAttr(token,goods_id):
    try:
        sess = requests.session()
        response = sess.post(url='{}/shop/api/proParams'.format(website),
                             data={"token": token,"goodsCatId":goods_id})
        # js = json.loads(res.text)
        return json.loads(response.content)
    except Exception as e:
        print(e)
        return {'errno':1}

def uploadImg(token,filelist):
    try:
        url = "{}/shop/api/upload".format(website)
        print(filelist)
        files = {"file": open(filelist, 'rb')}
        print(files)
        r = requests.post(url, data={'token': token, 'isThumb': '0', 'isWatermark': '0',
                                     'dir': 'goods'}, files=files)
        print(r.content)
        return json.loads(r.content)
    except Exception as e:
        print(e)

def Sendinfo(data):
    url = "{}/shop/api/publish".format(website)
    r = requests.post(url, data=data)
    return json.loads(r.content)

def getKeywordsList(keyword):
    url = "http://www.qihaonet.com/shop/api/getKR?keyword={}".format(keyword)
    r = requests.get(url)
    result = json.loads(r.content)
    keyword_all = []
    if len(result['data']) > 0:
        for info in result['data']:
            if len(keyword_all) <= 400:
                keyword_all.append(info['word'])
    return keyword_all
Login_in('sdybkj','13953772340',16)