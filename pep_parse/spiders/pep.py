import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        table = response.xpath('//section[@id="numerical-index"]')
        table_body = table.css('tbody')
        rows = table_body.css('tr')
        for row in rows:
            pep_link = row.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get().split()
        number = title[1]
        name = ' '.join(title[3:])
        status = response.css('dt:contains("Status") + dd::text').get()
        date = {
            'number': number,
            'name': name,
            'status': status.strip(),
        }
        return PepParseItem(date)
