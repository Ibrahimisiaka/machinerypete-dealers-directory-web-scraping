import scrapy


class MachinerypeteSpider(scrapy.Spider):
    name = 'machinerypete'
    allowed_domains = ['www.machinerypete.com']
    start_urls = ['https://www.machinerypete.com/dealerships/search']

    # View the list of all Stores in a State
    def parse(self, response):
        states =  response.css("a.btn.btn-default.btn-xs::attr(href)").getall()
        for state in states:
            state = response.urljoin(state)
            #print(state)
            yield scrapy.Request(url=state, callback=self.state_store)
    
    def state_store(self, response):
        stores =  response.css('li[style="font-size: 0.8em;"] > a::attr(href)').getall()
        for store in stores:
            store = response.urljoin(store)
            yield scrapy.Request(url = store, callback=self.store_content)

    def store_content(self, response):
        dealer_name = response.css("h1::text").get()
        contact_list = response.css(".store-header:contains('Contact') ~ div::text ").getall()
        contact = ", ".join(contact_list)
        address_list = response.css(".store-header:contains('Address') ~ div::text ").getall()
        address = ", ".join([x for x in address_list if x != '\n'])
        yield {
            'dealer_name' : dealer_name,
            'contact' : contact,
            'address' : address
        }
