import scrapy
import xlrd
import pymysql
from scrapyspider.items import Switch


db = pymysql.connect("localhost", "root", "12345678aA!", "test")


class RewriteSpider(scrapy.Spider):
    name = "rewrite"

    def start_requests(self):
        cursor = db.cursor()
        cursor.execute(
            'select url from switch where content like \'%sharedaddy%\'')
        shareds = cursor.fetchall()
        urls = []
        for i in shareds:
            urls.append(i[0]+'/')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sql = ''
        item = Switch()
        item['name'] = response.xpath('/html/head/title').get()
        item['url'] = response.url
        data1 = response.xpath(
            '//article/div[@class="entry-content"]/div[4]').get()
        sql = "update switch set content='%s' where url ='%s'" % \
            (data1, item['url'])
        item['content'] = data1
        item['sql'] = sql
        yield item
