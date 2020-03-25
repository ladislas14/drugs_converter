# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class ActiveSubstanceNameTranslationsItem(scrapy.Item):
    latinName = scrapy.Field()
    frenchName = scrapy.Field()
    chineseName = scrapy.Field()
    englishName = scrapy.Field()
    spanishName = scrapy.Field()
    russianName = scrapy.Field()
    arabicName = scrapy.Field()
    americanName = scrapy.Field()


class INNSpider(scrapy.Spider):
    name = "inn_spider"

    def __init__(self, language=None, substance=None):
        # do something else, don't care about the args
        if (language == "french"):
            self.language = 'INNF'
        elif (language == "english"):
            self.language = "INNE"
        elif (language == "chinese"):
            self.language = "INNCH"
        elif (language == "spanish"):
            self.language = "INNS"
        elif (language == "arabic"):
            self.language = "INNA"
        elif (language == "russian"):
            self.language = "INNR"
        elif (language == "latin"):
            self.language = "INN"
        elif (language == "american"):
            self.language = "INNUS"
        else:
            # TODO retourner une erreur
            pass

        self.substance = substance.lower()

    def start_requests(self):
        return [scrapy.FormRequest("https://mednet-communities.net/inn/login",
                                   formdata={'email': 'ladislas14@gmail.com', 'password': 'P7qp6hAJS4pEfB7trd'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        if (self.language != "american"):
            url = 'https://mednet-communities.net/inn/db/searchinn.aspx?ctl00$rightcolumn$optionType=1&ctl00$rightcolumn$option=1&ctl00$rightcolumn$Name=' + self.substance + '&ctl00$rightcolumn$language=' + self.language + '&ctl00$rightcolumn$proposedList=Select one&ctl00$rightcolumn$recommendedList=Select one&ctl00$rightcolumn$searchButton=Search&__VIEWSTATE=%2FwEPDwUJNzg0NjUzOTA4ZGQEej1%2FLKWwfDL1B4IMtn3hnu4TLw%3D%3D'
            return scrapy.Request(url, self.get_active_substance_link)
        else:
            pass
            # TODO gérer ces ricains

    def get_active_substance_link(self, response):
        if (response.status == 200):
            links = LinkExtractor(canonicalize=False, unique=False).extract_links(response)
            if (links != []):
                return scrapy.Request(links[0].url, self.parse)
            else:
                # TODO exception aucune substance trouvée, peut être tester d'abord avec l'alternate name
                return False
        else:
            # TODO lever une exception
            return False

    def parse(self, response):
        active_substance_name_translations = ActiveSubstanceNameTranslationsItem()

        active_substance_name_translations["englishName"] = response.css("h2 ::text").extract_first().strip()
        active_substance_name_translations["latinName"] = response.css(
            "#ctl00_rightcolumn_innForm_label0 ::text").extract_first()
        active_substance_name_translations["frenchName"] = response.css(
            "#ctl00_rightcolumn_innForm_Label2 ::text").extract_first()
        active_substance_name_translations["spanishName"] = response.css(
            "#ctl00_rightcolumn_innForm_Label4 ::text").extract_first()
        active_substance_name_translations["russianName"] = response.css(
            "#ctl00_rightcolumn_innForm_Label6 ::text").extract_first()
        active_substance_name_translations["arabicName"] = response.css(
            "#ctl00_rightcolumn_innForm_Label8 ::text").extract_first()
        active_substance_name_translations["chineseName"] = response.css(
            "#ctl00_rightcolumn_innForm_Label10 ::text").extract_first()

        index_for_american_name = None
        alternate_name = response.xpath('//table[@width="400px"]/tr/td/font/text()').getall()

        ##
        for i, item in enumerate(alternate_name):
            if (item.strip() == "USP"):
                index_for_american_name = i + 1

        if (index_for_american_name):
            active_substance_name_translations["americanName"] = alternate_name[index_for_american_name].strip()
        else:
            active_substance_name_translations["americanName"] = active_substance_name_translations["englishName"]

        return active_substance_name_translations