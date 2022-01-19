import scrapy
import logging

class AssetSpider(scrapy.Spider):
    name = 'asset'
  #  allowed_domains = ['mnregaweb4.nic.in/netnrega']
    start_urls = ['http://mnregaweb4.nic.in/netnrega/asset_report_dtl.aspx?lflag=eng&state_name=WEST%20BENGAL&state_code=32&district_name=NADIA&district_code=3201&block_name=KRISHNAGAR-I&block_code=&panchayat_name=DOGACHI&panchayat_code=3201009009&fin_year=2020-2021&source=national&Digest=8+kWKUdwzDQA1IJ5qhD8Fw']

    def parse(self, response):
        i = 4
        while i<2236:
            assetid = response.xpath('//table[2]//tr[$i]/td[2]/text()', i=i).get()
            assetcategory = response.xpath('//table[2]//tr[$i]/td[3]/text()', i=i).get()
            schemecode = response.xpath('//table[2]//tr[$i]/td[5]/text()', i=i).get()
            schemename = response.xpath('//table[2]//tr[$i]/td[7]/text()', i=i).get()
            link = response.xpath('//table[2]//tr[$i]/td[6]/a/@href', i=i).get()
            strlink = str(link)
            urlid = "http://mnregaweb4.nic.in/netnrega/"
            strurl = str(urlid)
            absoluteurl = f"{strurl}{strlink}"
            
           # absoluteurl = f"http://mnregaweb4.nic.in/netnrega{strlink}"
           # absoluteurl = response.urljoin(strlink)
           
            yield scrapy.Request(url=absoluteurl, callback=self.parse_asset, meta={'asset_id':assetid, 'scheme_code':schemecode, 'asset_category':assetcategory, 'scheme_name':schemename})
            i += 1
            
    def parse_asset(self, response):
        assetid = response.request.meta['asset_id']
        schemecode = response.request.meta['scheme_code']
        assetcategory = response.request.meta['asset_category']
        schemename = response.request.meta['scheme_name']
        sanctiondate = response.xpath("//table[3]//tr[6]/td[1]/nobr/p/font[2]/text()").get()
        wage = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[1]/font/text()").get()
        semiskilled = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[2]/font/text()").get()
        skilled = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[3]/font/text()").get()
        material = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[4]/font/a/text()").get()
        contingency = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[5]/font/text()").get()
        total = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[6]/font/text()").get()
       # contigency = contingency.replace(u'\xa0', u' ')
        yield {
            'assetid': assetid,
            'schemename': schemename,
            'schemecode': schemecode,
            'assetcategory': assetcategory,
            'sanctiondate': sanctiondate,
            'wage': wage,
            'semiskilled': semiskilled,
            'skilled': skilled,
            'material': material,
            'contingency': contingency,
            'total': total          
        }