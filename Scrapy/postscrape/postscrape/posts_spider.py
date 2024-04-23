import scrapy 

class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = ['https://www.thriftbooks.com/']
    visited_urls = set()
    all_content = []
    max_pages = 4
    max_depth = 1

    def parse(self, response):
        page_content = response.body
        self.all_content.append(page_content)
        if len(self.visited_urls) >= self.max_pages or response.meta.get('depth', 0) >= self.max_depth:
            return
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)
        for link in response.css('a::attr(href)').extract():
            yield response.follow(link, callback=self.parse, meta={'depth': response.meta.get('depth', 0) + 1})

    def closed(self, reason):
        combined_content = b'\n'.join(self.all_content)
        with open('combined_posts.html', 'wb') as f:
            f.write(combined_content)
