#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @author: focus
# @Time : 2019/10/31 9:05 AM
# @Software: PyCharm
import time
import re
import json
import requests
from lxml import etree
from traceback import format_exc
import random
import math



class ZhihuSpider(object):
    """
    知乎爬虫逻辑 百度搜索->知乎链接->知乎搜索->知乎翻页
    """

    def __init__(self, param):
        self.sess = requests.session()
        self.keyword = param['keyword']
        self.baidu_host = 'http://www.baidu.com'
        self.baidu_search = 'http://www.baidu.com/s?wd={}&ie=utf-8&rqlang=cn&tn=baiduhome_pg'
        self.enter_zhihu = ''
        self.zhihu_search = 'https://www.zhihu.com/search?type=content&q={}'
        self.zhihu_add = 'https://api.zhihu.com/search_v3?t=general&q={}&correction=1&offset={}&limit=20&lc_idx={}&show_all_topics=0&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
        self.zhihu_addhash = 'https://api.zhihu.com/search_v3?t=general&q={}&correction=1&offset={}&limit=20&lc_idx={}&show_all_topics=0&search_hash_id={}&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
        self.header = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
        self.result = []
        self.hash_id = None
        self.redis_key = param['redis_key']
        self.error_code = 0
        self.title_all = []
        self.content_all = []
        self.article_id_all = []

    def link_request(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        self.sess.headers.update(self.header)
        try:
            self.sess.get(self.baidu_host,headers=headers, timeout=3)
            url = self.baidu_search.format(u'\u77e5\u4e4e'.encode('utf-8') + self.keyword[:2].encode('utf-8'))
            time.sleep(5)
            resp_bsearch = self.sess.get(url,headers=headers, timeout=3)
            self.enter_zhihu = self.search_parse(resp_bsearch.content)
            if self.enter_zhihu:
                self.sess.get(self.enter_zhihu)
                resp_index = self.sess.get(self.zhihu_search.format(self.keyword.encode('utf-8')))
                self.resp_parse(resp_index.content)
            else:
                self.error_code = 5
        except Exception as e:
            print(e)
            self.error_code = 4
            return

    def add_request(self):
        offset = 20
        lc_idx = 21
        while len(self.result) < 100:
            try:
                if not self.hash_id:
                    url = self.zhihu_add.format(self.keyword.encode('utf-8'), offset, lc_idx)
                    resp_add = self.sess.get(url, timeout=3)
                else:
                    url = self.zhihu_addhash.format(self.keyword.encode('utf-8'), offset, lc_idx, self.hash_id)
                    resp_add = self.sess.get(url, timeout=3)
                offset += 20
                lc_idx += 20
                if lc_idx > 220:
                    break
                self.add_parse(resp_add.content)
                time.sleep(3)
            except Exception as e:
                break

    def search_parse(self, resp):
        print(resp)
        dment = etree.HTML(resp)
        res_list = dment.xpath("//div[@class='f13 c-gap-top-xsmall se_st_footer']/a[@class='c-showurl c-color-gray']")
        inter_zhihu = ''
        for i in res_list:
            if i.text and 'zhihu' in i.text:
                inter_zhihu = i.attrib['href']
                break
            elif u'\u77e5\u4e4e' in i.xpath("string(.)"):
                inter_zhihu = i.attrib['href']
                break
        # if not inter_zhihu:
        #    with open('{}.html'.format(int(time.time())), 'a+') as f:
        #        f.write(resp)
        return inter_zhihu

    def resp_parse(self, resp):
        hment = etree.HTML(resp)
        json_text = hment.xpath("//script[@id='js-initialData']")
        resa = json.loads(json_text[0].text)
        str_replace = re.compile(r'<.+?>')

        article_list = resa['initialState']['entities']['articles']
        for k1, v1 in article_list.items():
            if v1.get('content'):
                v1['content'] = v1['content'].replace('<p>', '').replace('</p>', '\n')
                news = str_replace.sub('', v1['content'])
                try:
                    if len(news) > 200:
                        if v1.get('title'):
                            title = str_replace.sub('', v1['title'])
                        else:
                            title = str_replace.sub('', v1['question']['name'])
                        self.result.append({'title': title, 'article_id': 'zh_' + str(v1['id']), 'content': news})
                except Exception as e:
                    print(e)
        answer_list = resa['initialState']['entities']['answers']
        for k2, v2 in answer_list.items():
            if v2.get('content'):
                v2['content'] = v2['content'].replace('<p>', '').replace('</p>', '\n')
                news = str_replace.sub('', v2['content'])
                try:
                    if len(news) > 200:
                        if v2.get('title'):
                            title = str_replace.sub('', v2['title'])
                        else:
                            title = str_replace.sub('', v2['question']['name'])
                        self.result.append({'title': title, 'article_id': 'zh_' + str(v2['id']), 'content': news})
                except Exception as e:
                        print(e)

    def add_parse(self, data):
        atext = json.loads(data)

        self.hash_id = atext['search_action_info']['search_hash_id']
        str_replace = re.compile(r'<.+?>')
        for i in atext['data']:
            if i['object'].get('content'):
                i['object']['content'] = i['object']['content'].replace('<p>', '').replace('</p>', '\n')
                news = str_replace.sub('', i['object']['content'])
                if len(news) > 200:
                    if i['object'].get('title'):
                        title = str_replace.sub('', i['object']['title'])
                    else:
                        title = str_replace.sub('', i['object']['question']['name'])
                    print({'title': title, 'article_id': 'zh_' + str(i['object']['id']), 'content': news})
                    self.result.append({'title': title, 'article_id': 'zh_' + str(i['object']['id']), 'content': news})

    def start_main(self):
        self.link_request()
        # if len(self.result) < 100 and self.error_code == 0:
        self.add_request()


if __name__ == '__main__':
    print(time.time())
    zp = ZhihuSpider({'keyword': u'雾炮机', 'redis_key': 'a'})
    zp.start_main()
    pass

