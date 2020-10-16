import scrapy
import xlrd
import pymysql
from scrapyspider.items import Switch


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        data = xlrd.open_workbook(
            "/home/jlzhu/spider/scrapyspider/scrapyspider/url/page.xlsx")
        table = data.sheet_by_index(0)
        nrow = table.nrows
        urls = []
        for i in range(nrow):
            urls.append(table.row(i-1)[1].value+'/')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sql = ''
        item = Switch()
        item['name'] = response.xpath('/html/head/title').get()
        item['url'] = response.url
        data0 = response.xpath(
            '//article/div[@class="entry-content"]/div[4]').get()
        data1 = response.xpath(
            '//article/div[@class="entry-content"]/div[5]').get()
        data2 = response.xpath(
            '//article/div[@class="entry-content"]/div[6]').get()

        if(data1 != None and data1.find('Download') != -1):
            sql = "insert into switch(`name`, url, content) value ('%s','%s','%s') " % \
                  (item['name'], item['url'], data1)
            item['content'] = data1
        elif (data0 != None and data0.find('Download') != -1):
            sql = "insert into switch(`name`, url, content) value ('%s','%s','%s') " % \
                  (item['name'], item['url'], data0)
            item['content'] = data0
        else:
            sql = "insert into switch(`name`, url, content) value ('%s','%s','%s') " % \
                  (item['name'], item['url'], data2)
            item['content'] = data2
        item['sql'] = sql
        yield item
