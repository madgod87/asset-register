import scrapy
import logging

class AssetSpider(scrapy.Spider):
    name = 'asset'
  #  allowed_domains = ['mnregaweb4.nic.in/netnrega']
    start_urls = ['http://mnregaweb4.nic.in/netnrega/asset_report_dtl.aspx?lflag=eng&state_name=WEST%20BENGAL&state_code=32&district_name=24%20PARGANAS%20SOUTH&district_code=3216&block_name=JAYNAGAR-I&block_code=&panchayat_name=BAHARU%20KSHETRA&panchayat_code=3216011001&fin_year=2022-2023&source=national&Digest=yS84zyE/CbboReMTHoBtCQ']

    def parse(self, response):
        i = 4
        while i<2236:
            assetid = response.xpath('//table[2]//tr[$i]/td[2]/text()', i=i).get()
            assetname = response.xpath('//table[2]//tr[$i]/td[3]/text()', i=i).get()
            schemecode = response.xpath('//table[2]//tr[$i]/td[5]/text()', i=i).get()
            schemename = response.xpath('//table[2]//tr[$i]/td[7]/text()', i=i).get()
            classofasset = response.xpath('//table[2]//tr[$i]/td[8]/text()', i=i).get()
            link = response.xpath('//table[2]//tr[$i]/td[6]/a/@href', i=i).get()
            strlink = str(link)
            urlid = "http://mnregaweb4.nic.in/netnrega/"
            strurl = str(urlid)
            absoluteurl = f"{strurl}{strlink}"
            
           # absoluteurl = f"http://mnregaweb4.nic.in/netnrega{strlink}"
           # absoluteurl = response.urljoin(strlink)
           
            yield scrapy.Request(url=absoluteurl, callback=self.parse_asset, meta={'asset_id':assetid, 'scheme_code':schemecode, 'asset_name':assetname, 'scheme_name':schemename, 'class_of_asset':classofasset})
            i += 1
            
    def parse_asset(self, response):
        assetid = response.request.meta['asset_id']
        schemecode = response.request.meta['scheme_code']
        assetname = response.request.meta['asset_name']
        schemename = response.request.meta['scheme_name']
        classofasset = response.request.meta['class_of_asset']

# Sanitized Scheme Data
        # sanctiondate = response.xpath("//table[3]//tr[6]/td[1]/nobr/p/font[2]/text()").get()
        # wage = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[1]/font/text()").get()
        # semiskilled = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[2]/font/text()").get()
        # skilled = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[3]/font/text()").get()
        # material = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[4]/font/a/text()").get()
        # contingency = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[5]/font/text()").get()
        # total = response.xpath("//table[3]//tr[10]/td/table//tr[2]/td[6]/font/text()").get()
        # mandays = response.xpath('//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()').get()


# Other Scheme Data
        sanctiondate = response.xpath("//table[3]//tr[7]/td[1]/nobr/p/font[2]/text()").get()
        wage = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[1]/font/text()").get()
        semiskilled = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()").get()
        skilled = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[3]/font/text()").get()
        material = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[4]/font/a/text()").get()
        contingency = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[5]/font/text()").get()
        total = response.xpath("//table[3]//tr[11]/td/table//tr[2]/td[6]/font/text()").get()
        mandays = response.xpath('//table[3]//tr[12]/td/table//tr[2]/td[2]/font/text()').get()
        
       # contigency = contingency.replace(u'\xa0', u' ')
        yield {
            'assetid': assetid,
            'schemename': schemename,
            'schemecode': schemecode,
            'assetname': assetname,
            'classofasset': classofasset,
            'sanctiondate': sanctiondate,
            'wage': wage,
            'semiskilled': semiskilled,
            'skilled': skilled,
            'material': material,
            'contingency': contingency,
            'total': total,
            'mandays': mandays       
        }