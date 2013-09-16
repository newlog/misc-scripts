#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from bs4 import BeautifulSoup
    from tidylib import tidy_document
except ImportError:
    print("[-] Required library not installed in the system.")
    print("[-] Execute: pip install -r requirements.txt")
    exit()

class ParsingEngine(object):

    def __init__(self):
        pass

    @staticmethod
    def parse_search(html, engine):
        results = None
        if engine == "fotocasa.es":
            results = ParsingEngine.parse_search_fotocasa(html, engine)
        elif engine == "idealista.com":
            pass
        return results

    @staticmethod
    def parse_result(html, engine):
        results = {}
        if engine == "fotocasa.es":
            results = ParsingEngine.parse_result_fotocasa(html)
        elif engine == "idealista.com":
            pass
        return results

    @staticmethod
    def parse_search_fotocasa(html, engine):
        results = None
        try:
            html, errors = tidy_document(html)
            soup = BeautifulSoup(html, "lxml")
            links = soup.find_all("a", class_="property-location")
            results =   [
                "http://www." + engine + link['href'] for link in links
                        ]
        except Exception as e:
            print("[-] Something went wrong parsing search: %s." % str(e))
        return results

    @staticmethod
    def parse_result_fotocasa(html):
        results = {}
        photos = None
        street = None
        price = None
        rooms = None
        baths = None
        parquet = None
        size = None
        try:
            html, errors = tidy_document(html)
            soup = BeautifulSoup(html, "lxml")
            photo_input = soup.find("input", 
                    attrs={"name":"ctl00$slidePhoto$hidUrlsPhotos"})
            if photo_input:
                photos = photo_input["value"].strip()
                photos = photos.split("|")
            # TODO: Parquet shit does not work because it is dinamically 
            # loaded by javascript. A workaround for this is here:
            # http://webscraping.com/blog/Scraping-JavaScript-webpages-with-webkit/
            parquet_span = soup.find("span",
                    attrs={"id":"ctl00_rptInteriorExtra_ctl17_lblExtra"})
            parquet = False
            if parquet_span:
                if not ("hasnt" in parquet_span['class']):
                    parquet = True
            price_span = soup.find("span",
                    attrs={"id":"currentPriceDetail"})
            if price_span:
                price = price_span.get_text().strip()
            street_h1 = soup.find("h1",
                    attrs={"class":"property-title"})
            if street_h1:
                street = street_h1.get_text().strip()
            street_span = soup.find("span",
                    attrs={"class":"title-extra-info"})
            if street_span:
                street_extra = street_span.get_text().strip()
                street = street + ", " + street_extra
            data_div = soup.find("div",
                    attrs={"id":"ctl00_DetailInfo"})
            if data_div:
                data_list = data_div.find_all("b")
                if len(data_list) > 0:
                    size = data_list[0].get_text()
                if len(data_list) > 1:
                    rooms = data_list[1].get_text()
                if len(data_list) > 2:
                    baths = data_list[2].get_text()
            results =   {
                "photos":photos,"price":price,"street":street,
                "size":size,"baths":baths,"rooms":rooms,"parquet":parquet
                        }
        except Exception as e:
            print("[-] Something went wrong parsing results: %s" % str(e))
            print("[*] Getting as much results as possible")
            if photos:
                results["photos"] = photos
            if price:
                results["price"] = price
            if street:
                results["street"] = street
            if size:
                results["size"] = size
            if baths:
                results["baths"] = baths
            if rooms:
                results["rooms"] = rooms
            results["parquet"] = parquet
        return results

if __name__ == "__main__":
    pass
