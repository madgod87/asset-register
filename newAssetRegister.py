import scrapy

class AssetSpider(scrapy.Spider):
    name = 'AssetRegister'
    start_urls = ['https://mnregaweb2.nic.in/netnrega/writereaddata/citizen_out/assetscreated_Out_2021_3216011001_05_ALL_ALL_local.html']

    def parse(self, response):
        trees = response.xpath('//form/center/table//tr')
        i = 0
        for tree in trees:
            if i<3:
                print('skip')
                i+=1
            else:
                fixed_url = 'https://mnregaweb2.nic.in/netnrega/'
                looped_url = tree.xpath('.//td[5]/font/a/@href').get()
                looped_url = looped_url[6:]
                new_url = f"{fixed_url}{looped_url}"
                completion_date = tree.xpath('.//td[7]/font/text()').get()
                estimated_cost = tree.xpath('.//td[8]/font/text()').get()
                estimated_material = tree.xpath('.//td[9]/font/text()').get()
                expenditure_wage = tree.xpath('.//td[10]/font/text()').get()
                expenditure_material = tree.xpath('.//td[11]/font/text()').get()
                yield scrapy.Request(url = new_url, callback = self.parse_asset, meta={'completion_date':completion_date, 'estimated_cost':estimated_cost, 'estimated_material':estimated_material, 'expenditure_wage':expenditure_wage, "expenditure_material":expenditure_material})
                
    def parse_asset(self, response):
        completion_date = response.request.meta['completion_date']
        estimated_cost = response.request.meta['estimated_cost']
        estimated_material = response.request.meta['estimated_material']
        expenditure_wage = response.request.meta['expenditure_wage']
        expenditure_material = response.request.meta['expenditure_material']

# Sanitized Scheme Data
        # sanctiondate = response.xpath("//table[3]//tr[6]/td[1]/nobr/p/font[2]/text()").get()
        # wage_expense = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[1]/font/text()").get()
        # semiskilled_expense = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[2]/font/text()").get()
        # skilled_expense = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[3]/font/text()").get()
        # material_expense = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[4]/font/a/text()").get()
        # contingency_expense = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[5]/font/text()").get()
        # total_expense = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[6]/font/text()").get()
        # mandays = response.xpath('//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()').get()

# Other Scheme Data
        scheme_code = response.xpath('//table[3]//tr[2]/td[2]/font[1]/text()').get()
        scheme_name = response.xpath('//table[3]//tr[2]/td[2]/font[2]/text()').get()
        sanctiondate = response.xpath("//table[3]//tr[7]/td[1]/nobr/p/font[2]/text()").get()
        wage_expense = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[1]/font/text()").get()
        semiskilled_expense = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()").get()
        skilled_expense = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[3]/font/text()").get()
        material_expense = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[4]/font/a/text()").get()
        contingency_expense = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[5]/font/text()").get()
        total_expense = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[6]/font/text()").get()
        mandays = response.xpath('//table[3]//tr[12]/td/table//tr[2]/td[2]/font/text()').get()
        
        yield{
            'scheme_code':scheme_code,
            'scheme_name':scheme_name,
            'completion_date':completion_date,
            'estimated_cost':estimated_cost,
            'estimated_material':estimated_material,
            'expenditure_wage':expenditure_wage,
            'expenditure_material':expenditure_material,
            'sanctiondate':sanctiondate,
            'wage_expense':wage_expense,
            'semiskilled_expense':semiskilled_expense,
            'skilled_expense':skilled_expense,
            'material_expense':material_expense,
            'contingency_expense':contingency_expense,
            'total_expense':total_expense,
            'mandays':mandays
        }