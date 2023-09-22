import scrapy

class create_spider(scrapy.Spider):
    name = "spid"
    def start_requests(self):
        urls = [
            'http://scanme.nmap.org/', 
            'https://nmap.org/book/man.html#man-description'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'spdr-{page}.html'
        
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        
        for urlListed in response.css('ul.toc'):
            yield {
                'url': urlListed.css('.sect1 a ::attr(href)').getall(),
                'text': urlListed.css('.sect1 ::text').getall()
                }
