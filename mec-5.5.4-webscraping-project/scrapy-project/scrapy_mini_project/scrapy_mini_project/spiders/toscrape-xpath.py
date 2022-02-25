import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.xpath("//div[contains(@class, 'quote')]"):
            yield {
                "text": quote.xpath(
                    "concat(//span[contains(@class, 'text')], //class[contains(@class, 'text')])"
                ).get(),
                "author": quote.xpath(
                    "concat(//small[contains(@class, 'author')], //class[contains(@class, 'text')])"
                ).get(),
                "tags": quote.xpath(
                    "concat(//div[contains(@class, 'tags')], concat(//a[contains(@class, 'tag')], //class[contains(@class, 'text')]))"
                ).getall(),
            }

        next_page = response.xpath("//li[@class='next']//a/@href").get()
        if next_page is not None:
            yield from response.follow(css="ul.pager a", callback=self.parse)
