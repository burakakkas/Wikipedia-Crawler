import scrapy
from termcolor import colored
import json
import traceback
from DuplicateRemover import DuplicatePages

class CategoryCrawler(scrapy.Spider):
    #Crawler Name, Main Dictionary and It's Index
    name = "CategoryCrawler"
    page_and_categories = {}
    index = 0

    def start_requests(self):
        urls = [
            'https://tr.wikipedia.org/wiki/Kategori:Oyuncu_listeleri'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    #end function for crawler which is start to work on when parse function ended.
    def closed(self, reason):
        #Writing to Json File
        with open('pages.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.page_and_categories, json_file, ensure_ascii=False, indent=2, sort_keys=False)
        complete_msg = str((self.index)) + ' process succesfully completed!'
        print(colored(complete_msg, 'green'))
        #Function for to remove duplicate pages on json
        DuplicatePages()

    def parse(self, response):
        try:
            #Dictionaries and Json Index's
            page_index = 0
            item_object = {}

            #Category Selectors
            category_div_items = response.css('div.CategoryTreeItem')
            category_name = response.css('h1.firstHeading')
            category_name = category_name.css('::text').extract()

            #Page Selectors
            page_div_items = response.xpath("//*[contains(@id, 'mw-pages')]")
            page_div_items = page_div_items.css('li')

            

            #Page Crawling in Current Category
            if page_div_items is not None:
                for pages in page_div_items:

                    #Category Name And Url Crawl
                    item_object["Category-Url"] = response.request.url
                    item_object["Category-Name"] = str(category_name[0])[9:]

                    #Page Selectors
                    page_title = pages.css('a::attr(title)').extract()
                    href = pages.css('a::attr(href)').extract()
                    
                    #Page Name And Url Crawl
                    item_object['Page-Name'] = str(page_title[0])
                    item_object['Page-Url'] = 'https://tr.wikipedia.org' + str(href[0])
                    
                    #Copy context into global dictionary and resetting local dictionary for each page crawl
                    self.page_and_categories[self.index] = item_object
                    self.index = self.index + 1
                    item_object={}

                    #Success Message
                    #print(colored(('Process ' + str(self.index) + ' Completed Successfully.'), 'green'))

            #Check Category is Null or Not
            if len(category_div_items) != 0:
                category = category_div_items[0].css('a::attr(title)').extract()  
                del category_div_items[0]

                #Category Recursive Function
                for items in category_div_items:
                    sub_category_link = items.css('a::attr(href)').get()
                    if sub_category_link is not None:
                        yield response.follow(sub_category_link,callback= self.parse)

        #Error Handling
        except Exception:
            traceback.print_exc()
                    
                
