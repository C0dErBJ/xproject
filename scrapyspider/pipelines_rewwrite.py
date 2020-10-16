# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

db = pymysql.connect("localhost", "root", "12345678aA!", "test")

class WritePipeline:
    def process_item(self, item, spider):
        cursor=db.cursor()
        cursor.execute(item['sql'])
        db.commit()
        return item
