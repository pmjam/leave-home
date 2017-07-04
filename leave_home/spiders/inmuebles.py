# -*- coding: utf-8 -*-
import scrapy


class InmueblesSpider(scrapy.Spider):
    name = 'inmuebles'
    allowed_domains = [
        'inmuebles24.com',
        # 'adondevivir.com',
        # 'conlallave.com',
        # 'plusvalia.com',
        # 'compreoalquile.com',
        # 'zonaprop.com.ar',
        # 'compreoalquile.co.cr',
        # 'inmuebles24.co',
        # 'wimoveis.com.br',
        # 'imoveiscuritiba.com.br',
        # 'imovelweb.com.br',
    ]
    start_urls = [
        # add your urls to scrapy here
        'http://www.inmuebles24.com/departamentos-en-venta-en-aguascalientes-provincia.html'
        # 'http://www.adondevivir.com/departamentos-en-alquiler-en-piura-provincia.html',
        # 'http://www.conlallave.com/apartamentos-en-venta-en-cojedes.html',
        # 'http://www.plusvalia.com/casas-en-venta-en-canar-provincia.html',
        # 'http://www.compreoalquile.com/apartamentos-en-venta-en-colon-provincia.html',
        # 'http://www.zonaprop.com.ar/departamento-venta-catamarca.html',
        # 'http://www.compreoalquile.co.cr/apartamentos-en-venta.html',
        # 'http://www.inmuebles24.co/apartamentos-venta-bolivar.html',
        # 'http://www.wimoveis.com.br/apartamentos-venda-aguas-lindas-de-goias-go.html',
        # 'http://www.imoveiscuritiba.com.br/lancamentos-curitiba-pr.html',
        # 'http://www.imovelweb.com.br/apartamentos-venda-amapa.html',
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

        next_page = response.css(
            'li.pagination-action-next'
        ).xpath(
            'self::*[not(contains(@class,"disabled"))]/a/@href'
        ).extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
