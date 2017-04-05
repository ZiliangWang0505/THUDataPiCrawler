# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import hashlib
import traceback
import pymongo
from spiders.utils import *

mongo_client = pymongo.MongoClient()


# 每一个招聘信息都会计算出一个md5，作为mysql数据库的UNIQUE KEY，避免重复写入数据
def md5str(strr):
    m = hashlib.md5(strr)
    md5 = m.hexdigest().lower()
    return md5


# 将职位需求拼接到一起，方便写入数据库
def get_require(requires):
    require = ''
    for r in requires:
        require += r + ' '
    return require.strip().encode('utf-8')


class MongoPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client.get_database('liepin')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            # position_dict = self.get_cup(item)
            self.db['positions'].insert(dict(item))
            print 'data inserted!'

        # 捕捉错误信息写入log
        except Exception, e:
            print 'url is: %s, error is: %s.' % (item['url'], traceback.format_exc()),
            print e
            traceback.print_exc()
        finally:
            return item
