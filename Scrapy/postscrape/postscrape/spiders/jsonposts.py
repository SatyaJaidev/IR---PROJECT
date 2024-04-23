import scrapy 
import json

class PostsSpider(scrapy.Spider):
    name = "jsonposts"
    start_urls = ['https://www.thriftbooks.com/']
    visited_urls = set()
    all_content = []
    max_pages = 4
    max_depth = 1

    def parse(self, response):
        if len(self.visited_urls) >= self.max_pages or response.meta.get('depth', 0) >= self.max_depth:
            return

        if response.url in self.visited_urls:
            return

        self.visited_urls.add(response.url)

        # Extract the data you want from the page
        page_title = response.css('title::text').get()
        page_url = response.url
        page_content = response.body.decode('utf-8')

        # Create a JSON item with the extracted data
        yield {
            'title': page_title,
            'url': page_url,
            'content': page_content
        }

        # Follow links for further scraping
        for link in response.css('a::attr(href)').extract():
            yield response.follow(link, callback=self.parse, meta={'depth': response.meta.get('depth', 0) + 1})
