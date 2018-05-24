import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from stackFlw.items import StackflwItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from datetime import datetime as dt


class StackFlw(Spider):
    name = 'stackFlw'
    allowed_domains = ['stackoverflow.com']

    start_urls = [
        'https://stackoverflow.com/questions/tagged/python?page=1&sort=newest&pagesize=50'
    ]

    def parse(self, response):
        posts = response.css('div.question-summary')
        # self.logger.info('Parse function called on %s', response.url)


        for post in posts:
            # item = StackflwItem()
            #
            # item['date'] = dt.today().strftime('%Y-%m-%d')
            #
            # item['title'] = post.css('div.summary h3 a::text').extract_first()
            #
            # item['url'] = post.css('div.summary h3 a::attr(href)').extract_first()
            #
            # item['author'] = post.css('div.user-details a::text').extract_first()
            #
            #
            # yield item
            views = post.css('div.views::text').extract_first()
            if views.find('views'):
                views_strip = views.replace('views', '')
            else:
                views_strip = views.replace('view', '')
            views_int = int(views_strip)
            print('\n')
            yield {

                'date': dt.today().strftime('%Y-%m-%d %-I:%M:%S %p'),
                'title': post.css('div.summary h3 a::text').extract_first(),
                'url': post.css('div.summary h3 a::attr(href)').extract_first(),
                'author': post.css('div.user-details a::text').extract_first(),
                'views': views_int
            }
            print('\n')

        #Pagination
        next_page = response.css('div.pager.fl  a[rel="next"]::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        
        # posts2 = Selector(response).xpath('//div[@class="user-info"]/div')
        #
        # for post2 in posts2:
        #     item2 = StackflwItem()
        #
        #     item['author'] = post2.xpath(
        #         'a[@class="user-details"]/text()').extract()[0]
        #
        #     yield item2


# //*[@id="question-summary-50112188"]/div[2]/div[3]/div/div[3]/a
# //*[@id="question-summary-50112188"]/div[2]/h3/a