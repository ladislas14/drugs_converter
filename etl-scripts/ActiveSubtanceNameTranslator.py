import scrapy
from scrapy.linkextractors import LinkExtractor


class ActiveSubstanceTranslationItem(scrapy.Item):
    countryId = scrapy.Field()
    name = scrapy.Field()
    activeSubstanceId = scrapy.Field()


class INNSpider(scrapy.Spider):
    name = "inn_spider"

    def start_requests(self):
        return [scrapy.FormRequest("https://mednet-communities.net/inn/login",
                                   formdata={'email': 'ladislas14@gmail.com', 'password': 'P7qp6hAJS4pEfB7trd'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        url = 'https://mednet-communities.net/inn/db/searchinn.aspx?ctl00$rightcolumn$optionType=1&ctl00$rightcolumn$option=1&ctl00$rightcolumn$Name=' + self.substance + '&ctl00$rightcolumn$language=' + self.language + '&ctl00$rightcolumn$proposedList=Select one&ctl00$rightcolumn$recommendedList=Select one&ctl00$rightcolumn$searchButton=Search&__VIEWSTATE=%2FwEPDwUJNzg0NjUzOTA4ZGQEej1%2FLKWwfDL1B4IMtn3hnu4TLw%3D%3D'
        return scrapy.Request(url, self.get_active_substance_link)

    def get_active_substance_link(self, response):
        links = LinkExtractor(canonicalize=False, unique=False).extract_links(response)
        return scrapy.Request(links[0].url, self.parse)

    def parse(self, response):
        scrapy.utils.response.open_in_browser(response)