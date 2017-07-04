# -*- coding: utf-8 -*-
import scrapy


class InmueblesSpider(scrapy.Spider):
    name = 'inmuebles'
    allowed_domains = [
        'inmuebles24.com',
    ]
    start_urls = [
        'http://www.inmuebles24.com/departamentos-en-venta-en-aguascalientes-provincia.html'
    ]

    def parse(self, response):
        offers = response.css('li.post')
        for offer in offers:
            yield {
                'id': offer.css('::attr(id)').extract_first().strip(),
                'title': offer.css('h4.post-titulo a::text').extract_first().strip(),
                'price': offer.css('span.precio-valor::text').extract_first().strip(),
                'href': response.urljoin(
                    offer.css('::attr(data-href)').extract_first().strip()
                ),
            }

        next_page = response.css('li.pagination-action-next').xpath('self::*[not(contains(@class,"disabled"))]/a/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
