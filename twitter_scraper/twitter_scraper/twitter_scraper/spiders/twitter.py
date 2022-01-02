import time

import scrapy
import re
import pandas as pd
from scrapy.linkextractors import LinkExtractor
from twitter_inputs import read_csv, sample_csv, read_csv_as_dict
from twitter_scraper.items import TwitterScraperItem
from scrapy_selenium import SeleniumRequest

def wait(driver):
    time.sleep(1)
    return True

class TwitterSpider(scrapy.Spider):
    name = 'twitter'

    def start_requests(self):
        for data in read_csv_as_dict():
            url = data["website"]
            if url:
                yield SeleniumRequest(
                    url=url,
                    callback=self.parse,
                    wait_time=5,
                    wait_until=wait,
                    screenshot=True,
                    dont_filter=True,
                    meta=data
                )
                # yield scrapy.Request(url=url, meta=data, callback=self.parse, dont_filter=True)


    def parse(self, response):
        data = response.request.meta
        q = TwitterScraperItem()
        q['profileUrl'] = data['profileUrl']
        q['screenName'] = data['screenName']
        q['userId'] = data['userId']
        q['name'] = data['name']
        q['bio'] = data['bio']
        q['website'] = data['website']
        q['location'] = data['location']
        q['createdAt'] = data['createdAt']
        q['redirected_website'] = response.url

        flag = 0
        bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki', 'linkedin']

        for word in bad_words:
            if word in str(response.url):
                flag = 1
                break

        if (flag != 1):
            html_text = str(response.text)
            email_regex = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
            email_set = set(re.findall(email_regex, html_text))
            email_without_contact = list(email_set)
            # print(email_list)
            q['email_without_contact'] = email_without_contact

        about_page = []
        if (flag != 1):
            link_extractor = LinkExtractor(allow=['contact', 'CONTACT', 'Contact', 'about', 'ABOUT', 'About'], unique=True)
            for link in link_extractor.extract_links(response):
                about_page.append(link.url)

        contact_page = []
        check = 0
        for l in about_page:
            if ('contact' in l) or ('Contact'in l) or ('CONTACT' in l):
                check = 1
                contact_page.append(l)
                break
        # print(li)

        if (check != 0):
            contact = contact_page[0]
            q['contact_page'] = contact
            # print(contact)
            yield SeleniumRequest(
                url=contact,
                callback=self.parsecontactpage,
                wait_time=5,
                wait_until=wait,
                screenshot=True,
                dont_filter=True,
                meta={'q': q}
            )
            # yield scrapy.Request(url=contact, meta={'q': q}, callback=self.parsecontactpage, dont_filter=True)
        elif (len(about_page) > 0):
            q['contact_page'] = about_page[0]
            # print(about_page[0])
            yield SeleniumRequest(
                url=about_page[0],
                callback=self.parsecontactpage,
                wait_time=5,
                wait_until=wait,
                screenshot=True,
                dont_filter=True,
                meta={'q': q}
            )
            # yield scrapy.Request(url=about_page[0], meta={'q': q}, callback=self.parsecontactpage, dont_filter=True)
        else:
            q['contact_page'] = ""


    def parsecontactpage(self, response):
        q = response.meta['q']
        html_text = str(response.text)
        email_regex = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
        email_set = set(re.findall(email_regex, html_text))
        all_email_list = list(email_set) + q['email_without_contact']
        ## this set is not necessary
        email_list = list(set(all_email_list))

        email_with_contactpage = []
        extension = ['.com', '.org', '.edu', '.de', '.in', '.es', '.ru', '.ca', '.jp', '.ar', '.mx', '.it', '.de',
                     '.id', '.sg', '.nl', '.fr', '.au', '.co', '.ch', '.be', '.net', '.nl', '.au', '.ac']
        for email in email_list:
            for ext in extension:
                if ext in email:
                    email_with_contactpage.append(email)

        # q['contact_page'] = response.url
        if (len(email_with_contactpage) > 0):
            q['email_list'] = ", ".join(set(email_with_contactpage))
            q['status'] = True
        else:
            email_with_contactpage.append('None')
            q['email_list'] = email_with_contactpage
            q['status'] = False
        q.pop('email_without_contact')

        return q








        # special_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki', 'linkedin']
        # for word in special_words:
        #     if word in str(response.request.url):
        #         q["social_media"] = response.request.url
        #     else:
        #         q["social_media"] = ""
        #
        # for word in special_words:
        #     if word not in str(response.request.url):
        #         q["website"] = response.request.url
        #     else:
        #         q["website"] = ""
        # return q




#     self.df.loc[self.df.website == self.url, "Email"] = q['email_list']
#     self.df.to_csv("helpareporter_twitter_follower.csv", index=False)
#     # subset = self.df.loc[:151, ['website', 'Email']]