import scrapy
import pprint
import re
from urllib.parse import urlparse

class BetterFyiSpider(scrapy.Spider):
    name = "better_fyi_spider"
    start_urls =[
        'https://better.fyi/trackers/',
        # 'https://better.fyi/trackers/adform.net/',
        # 'https://better.fyi/trackers/honorableland.com/',
        # 'https://better.fyi/trackers/1rx.io/'
    ]

    def parse(self, response):
        count = 0
        for tracker in response.xpath("//ul[@data-set-text='html list']/li/a"):
            href_val = tracker.xpath("@href").get()
            tracker_found_url = response.urljoin(href_val)+"/"            
            tracker_title = tracker.xpath("./strong/text()").get()
            tracker_website = tracker.xpath("text()").get()
            
            request = scrapy.Request(tracker_found_url,
                             callback=self.parse_tracker,
                             cb_kwargs=dict(tracker_found_url=tracker_found_url))
            request.cb_kwargs['tracker_title'] = tracker_title
            request.cb_kwargs['tracker_website'] = tracker_website
            yield request
            
            
            count += 1
            print("count: ", count)
            # if count == 100:
                # break
            
    def parse_tracker(self, response, tracker_found_url, tracker_title, tracker_website):
        
        tracker_description_p = response.xpath("//blockquote/p/text()").get()
        tracker_description_a = response.xpath("//blockquote/p/a/text()").get()
        tracker_description = None
        tracker_description_source = ""
        href_value = response.xpath("//blockquote/p/a/@href").get()
        if tracker_description_a and tracker_description_a.strip() == "Source":
            tracker_description = tracker_description_p.replace(chr(8221), "").replace(chr(8220), "")[:-3]
            tracker_description_source = href_value
        else:
            if tracker_description_p and tracker_description_a:
                tracker_description = tracker_description_p + tracker_description_a
            parsed_url = urlparse(response.url)
            fully_qualified_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
            if fully_qualified_domain and href_value:
                tracker_description_source = fully_qualified_domain + href_value
            
        rule_text = response.xpath('//code[@class="mson"]//text()').getall()
        rule_text = re.sub(' +', ' ', "".join(rule_text)+'\n')
        bool_val = response.xpath('boolean(//code[@class="mson"]/span)').get()
        tracker_block_rule = ""
        if int(bool_val):
            tracker_block_rule = rule_text
        else:
            tracker_block_rule = ''.join(rule_text.split('\n')).replace('\n', '')
        
        
        
        output_dict = {   'found_url': tracker_found_url,
                        'title': tracker_title,
                        'website' : tracker_website,
                        'description' : tracker_description,
                        'description_source': tracker_description_source,
                        'block_rule': tracker_block_rule,
                    }
        
        yield output_dict