import scrapy
import xlrd


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):

        data = xlrd.open_workbook(
            "/home/jlzhu/spider/scrapyspider/scrapyspider/url/page.xlsx")
        table = data.sheet_by_index(0)
        nrow = table.nrows
        self.log("行数 %s" % nrow)
        urls = []
        for i in range(nrow):
            urls.append(table.row(i-1)[1].value+'/')
        for url in urls:
            self.log("新增url %s" % url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data1 = response.xpath(
            '//article/div[@class="entry-content"]/div[5]').get()
        data2 = response.xpath(
            '//article/div[@class="entry-content"]/div[6]').get()
        self.log('saved data1 %s' % data1)
        self.log('saved data2 %s' % data2)
