import scrapy
from termcolor import colored
import json
import traceback
import re

class PageCrawler(scrapy.Spider):
    #Crawler Name, Custom Settings, Main Dictionary and It's Index
    name = "PageCrawler"
    custom_settings = {
        'CONCURRENT_REQUESTS': '1',
    }
    page_index = 0
    data = {}

    def start_requests(self):
        #opening category crawler json 
        f = open('pages.json',)
        self.data = json.load(f)

        #collecting all urls from json to list
        urls = []
        for n in self.data:
            url = self.data[n]['Page-Url']
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        

    def closed(self, reason):
        #Complete message
        print(colored(self.page_index, 'green') +
              colored(' process successfully completed!', 'green'))
        #Writing to Json File
        with open('pages.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False,
                      indent=2, sort_keys=False)


    def parse(self, response):
        try:
            index = 0
            all_text = ''

            #Page Selectors
            page_div = response.xpath(
                "//*[contains(@id, 'mw-content-text')]")
            page_div = page_div.css('div.mw-parser-output')
            page_div = page_div.css('p')
            
            if len(page_div) != 0:
                for ptags in page_div:

                    #parahraph number for main section crawler of pages
                    if index <= 8 :
                        ptags = ptags.css('*::text').getall()
                        #checking is there any parahraph as a text or just a list page
                        if len(ptags) != 0:
                            #adding all texts on main section for create one parahraph
                            for text in ptags:
                                #regex functions to remove special characters
                                text = re.sub("\[.*?\]", '', str(text))
                                #text = re.sub("[^\w ]", '', str(text))
                                #text = re.sub('/(\r\n)+|\r+|\n+|\t+/', ' ', text)
                                all_text = all_text + text
                        index = index + 1
                    else:
                        break
            #adding text to the global dictionary with its index number
            self.data[str(self.page_index)]['Text'] = str(all_text)            

            #global process counter for crawler
            #print(self.page_index)
            self.page_index = self.page_index + 1
            
            
        #Error Handling
        except Exception:
            traceback.print_exc()
