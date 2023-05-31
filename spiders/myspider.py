import scrapy
from scrapy import FormRequest


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://www.hcidirectory.gov.sg/hcidirectory/"]

    def parse(self, response, **kwargs):
        payload = {
            "struts.token.name": "token",
            "token": "AMST1B6OPF1ZH4C82V98XFPWCUBR2GA5",
            "task": "search",
            "RadioGroup1": "HCI Name",
            "name": "",
            "clinicType": "all"
        }

        yield FormRequest.from_response(response, formdata=payload, callback=self.parse_data)

    def parse_data(self, response):
        for result in response.xpath("//*[@class='result_container']"):
            items = {
                'Name': result.xpath('normalize-space(./*[@class="col1"]//a/text())').get(),
                'Phones': ', '.join([t.replace('\xa0', ' ') for t in
                                     result.xpath('normalize-space(./*[@class="col1"]//*[@class="tel"])').getall()]),
                'Address': result.xpath('normalize-space(./*[@class="col2"]//*[@class="add"])').get(),
                'Timing': result.xpath('normalize-space(./*[@class="col3"])').get()
            }
            yield items
        current_page = int(response.css('#targetPageNo ::attr(value)').get())
        total_page = int(response.css('#totalPage ::attr(value)').get())
        if current_page < total_page:
            data = {
                'task': 'search',
                'RadioGroup1': 'HCI Name',
                'name': '',
                'clinicType': 'all',
                'targetPageNo': str(current_page + 1),
                'totalPage': str(total_page),
            }
            yield FormRequest.from_response(response, formdata=data, callback=self.parse_data)

