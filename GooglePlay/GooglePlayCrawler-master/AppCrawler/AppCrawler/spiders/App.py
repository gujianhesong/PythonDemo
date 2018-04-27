#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import sys
sys.path.append(r"E:\PycharmProjects\CrapyTest\GooglePlayCrawler-master\AppCrawler")
from AppCrawler.items import GoogleItem
# from AppCrawler.config import SpiderConfig
from scrapy.spiders import Rule, CrawlSpider

import urlparse
import time

class AppSpider(CrawlSpider):
    name = "App"
    allowed_domains = ["play.google.com"]
    start_urls = [
        'http://play.google.com/',
        'https://play.google.com/store/apps/details?id=com.UCMobile.intl'
    ]

    rules =( 
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details", )), callback = 'parse_app', follow = True),
    )

    # def parse_item(self, response):
    #     if response.url.find('reviewId') != -1: return;
    #     item = AppCrawlerItem()
    #
    #     item["Downloads"] = response.xpath("//div[@itemprop='numDownloads']/text()").extract_first().strip()
    #
    #     # item["Name"] = response.xpath('//div[@class="AHFaub"]/text()').extract_first().strip()
    #     # item["Name"] = response.xpath('//div[@class="id-app-title"]/text()').extract_first().strip()
    #     # item["URL"] = response.url[0]
    #     # item["Downloads"] = response.xpath("//div[@itemprop='numDownloads']/text()").extract_first().strip()
    #     # item["Updated"] = response.xpath("//div[@itemprop='datePublished']/text()").extract_first().strip()
    #     # item["Version"] = response.xpath('//div[@itemprop="softwareVersion"]/text()').extract_first().strip()
    #     # item["Review_number"] = response.xpath("//span[@class='reviews-num']/text()").extract_first().strip()
    #     # item["Rating"] = float(response.xpath("//div[@class='score']/text()").extract_first().strip())
    #     # item["Author"] = response.xpath('//div[@itemprop="author"]/a/span/text()').extract_first().strip()
    #     # item["Genre"] = response.xpath('//span[@itemprop="genre"]/text()').extract_first().strip()
    #     price = response.xpath('//button[@class="price buy id-track-click id-track-impression"]/span[2]/text()').extract_first().strip()
    #     if price == u'Install': item["Price"] = 0
    #     else: item["Price"] =float(price.split()[0][1:])
    #
    #     yield item

    # def parse_item2(self, response):
    #     if response.url.find('reviewId') != -1: return;
    #     item = AppItem()
    #
    #     google_play = SpiderConfig.google_play
    #     print "Grabing Start：%s" % response.url
    #     # 根据SpiderConfig中的xpath配置进行抓取数据
    #     for key in google_play:
    #         value = response.xpath(google_play[key]).extract() if google_play[key] != '' else ''
    #         item[key] = value[0].strip() if len(value) == 1 else ('' if len(value) == 0 else value)
    #     item['imgs_url'] = " ".join(item['imgs_url'])
    #     item['download_times'] = item['download_times'].replace(',', '')[:item['download_times'].find('-')]
    #     item['rating_count'] = item['rating_count'].replace(',', '')
    #     item['platform'] = "googleplay"
    #     print "Grabing finish, step into information pipline"
    #
    #     yield item

    def parse_app(self, response):
        # 在这里只获取页面的 URL 以及下载数量
        item = GoogleItem()

        url = response.url
        url = urlparse.urlparse(url).query.split('&')[0].split('=')[-1]
        # 分类
        categories = response.xpath(
            '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div/div[1]/div[1]/span[2]/a/text()').extract()[
            0]
        # 详情
        desc = response.xpath('//*[@id="fcxH9b"]//content/div[1]/text()').extract()
        if len(desc):
            if str(desc[0].encode('utf-8')) == 'Translate':
                desc.pop(0)
        desc = ''.join(desc)
        # 评分
        rating = dict()
        # rating['overall'] = response.xpath('//*[@id="fcxH9b"]//div[@class="BHMmbe"]/text()').extract()[0]
        # rating['five_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][1]/span[@class="UfW5d"]/text()').extract()[0]
        # rating['four_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][2]/span[@class="UfW5d"]/text()').extract()[0]
        # rating['three_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][3]/span[@class="UfW5d"]/text()').extract()[0]
        # rating['two_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][4]/span[@class="UfW5d"]/text()').extract()[0]
        # rating['one_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][5]/span[@class="UfW5d"]/text()').extract()[0]
        # rating["total_rating"] = response.xpath('//*[@id="fcxH9b"]//span[@class="EymY4b"]/span[2]/text()').extract()[0]
        # pprint(rating)

        # 获取权限
        # permission_set = set()
        # while True:
        #     try:
        #         next = self.driver.find_element_by_xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"]//a[@jsname="Hly47e"]')
        #         next.click()
        #         time.sleep(3)
        #         next_list = next.find_elements_by_xpath('//div[@class="fnLizd"]//li')
        #         print(len(next_list))
        #         for element in next_list:
        #             print(element.text)
        #             permission_set.add(element.text)
        #         break
        #     except NoSuchElementException:
        #         return
        # permission = list(permission_set)

        item['url'] = url
        item['title'] = response.xpath('//*[@id="fcxH9b"]//h1[@class="AHFaub"]/span/text()').extract()[0]
        item['categories'] = categories
        # item['download_num'] = response.xpath('//*[@id="fcxH9b"]//span[@class="AYi5wd TBRnV"]//text()').extract()[0]
        item['description'] = desc
        # item["rating"] = "one_star:" + rating["one_star"] + ";" + "two_star:" + rating[
        #     "two_star"] + ";" + "three_star:" + rating["three_star"] + ";" + "four_star:" + rating[
        #                      "four_star"] + ";" + "five_star:" + rating["five_star"] + ";" + "total_rating:" + rating[
        #                      "total_rating"] + ";" + "overall:" + rating["overall"]

        item['update_date'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][1]//span/text()').extract()[0]
        item['size'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][2]//span/text()').extract()[0]
        item['download_num'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][3]//span/text()').extract()[0]
        item['cur_version'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][4]//span/text()').extract()[0]
        item['require'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][5]//span/text()').extract()[0]
        item['level'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][6]//span/div/text()').extract()[0]
        item['interaction'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][7]//span/text()').extract()[0]
        item['developer'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][8]//span/text()').extract()[0]
        item['dev_web'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][9]//span/div[1]/a/@href').extract()[0]
        item['dev_email'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][9]//span/div[2]/a/text()').extract()[
            0]
        item['dev_name'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][9]//span/div/text()').extract()[0]

        item["authority"] = ""
        # if len(permission):
        #     for per in permission:
        #         item["authority"] = item["authority"] + per + ";"

        # with open('F:\PROJECT\googleCrawl\googleCrawl\package_FINANCE.txt', 'w+') as f:
        #     f.write(url + '\n')
        yield item