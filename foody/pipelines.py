# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
sys.path.append('C:/Users/Admin/PROGRAM/PYTHON/FILE.PY/Foody_Crawl_Data-master/Foody_Crawl_Data-master/')

import pymongo
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import logging as log
import json
# from foody.middleware.sqlite4lsmmiddlewares import LSMEngine

# Lưu vào mongodb
class FoodyPipeline(object):
    def __init__(self):
        connection = MongoClient(settings['MONGODB_URI'])
        db = connection[settings['MONGODB_DATABASE']]
        # db.authenticate(settings['MONGODB_USERNAME'], settings['MONGODB_PASSWORD'])
        self.collection = db[settings['CRAWLER_COLLECTION']]

    def process_item(self, item, spider):
        data = dict(item)
        #     if data['url'] not in LSMEngine.db:
        #         LSMEngine.db['url'] = '1'
        self.collection.insert_one(data)
        return item


# Lưu vào file json
# import json

# class JsonWriterPipeline(object):
#     def __init__(self):
#         self.file = open('items.json', 'w')

#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item

#     def close_spider(self, spider):
#         self.file.close()



# # Đưa lên hadoop
# from scrapy.exceptions import DropItem
# from hdfs.ext.kerberos import KerberosClient 
# import json
# class HDFSWriterPipeline:
#     def __init__(self):
#         self.client = KerberosClient("http://localhost:9870")
#         self.file_path = 'item3.json'
#     def open_spider(self, spider):
#         self.hdfs_dir = "/"  # Thay đổi thư mục đích trên HDFS nếu cần

#     def process_item(self, item, spider):
#         # Chuyển đổi item thành chuỗi JSON
#         json_data = json.dumps(dict(item), ensure_ascii=False)

#         # Kiểm tra xem file đã tồn tại trên HDFS hay chưa
#         file_exists = False
#         try:
#             self.client.status(self.hdfs_dir + self.file_path)
#             file_exists = True
#         except:
#             pass

#         # Ghi dữ liệu JSON vào HDFS
#         with self.client.write(self.hdfs_dir + self.file_path, append=file_exists, encoding="utf-8") as writer:
#             writer.write(json_data + "\n")

#         return item

#     def close_spider(self, spider):
#         pass