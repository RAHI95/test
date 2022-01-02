import scrapy


class TwitterScraperItem(scrapy.Item):
    # social_media = scrapy.Field()
    website = scrapy.Field()
    screenName = scrapy.Field()
    userId = scrapy.Field()
    name = scrapy.Field()
    bio = scrapy.Field()
    location = scrapy.Field()
    createdAt = scrapy.Field()
    redirected_website = scrapy.Field()
    profileUrl = scrapy.Field()
    email_without_contact = scrapy.Field()
    contact_page = scrapy.Field()
    email_list = scrapy.Field()
    status = scrapy.Field()

