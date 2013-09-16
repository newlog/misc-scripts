#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.http_utils import HTTPUtils
from utils.file_utils import FileUtils
from utils.os_utils import OSUtils
from utils.parsing_engine import ParsingEngine

class Main(object):

    def __init__(self, args):
        self.engine = args.engine
        self.minp = args.minprice
        self.maxp = args.maxprice
        self.mins = args.minsize
        self.f = args.furnished
        self.l = args.limit
        self.op = args.output_path
        self.cf = args.config_file

    def run(self):
        results = None
        if self.cf:
            print("[-] Still not implemented. Could not read from file.")
        else:
            try:
                url, params = self.build_request()
                hu = HTTPUtils(url, params=params)
                html = hu.make_request()
                links = ParsingEngine.parse_search(html.content, self.engine)
                if not links:
                    print("[-] Search did not return results. Exiting...")
                    exit()
                # Check if search with these params was made 4 this engine
                filepath = self.check_or_create_params_dir()
                filepath += "/"
                search_filepath = filepath
                # Check if last_result exist
                last_result = self.check_last_result(filepath)
                # Check if today, a search was done with these params
                filepath = self.check_or_create_today_dir(filepath)
                filepath += "/"
                i = 0
                for link in links:
                    try:
                        if last_result == link:
                            print("[ * Result from prior searches found * ]")
                            break
                        hu = HTTPUtils(link)
                        html = hu.make_request()
                        results = ParsingEngine.parse_result(html.content, self.engine)
                        if not results:
                            print("[-] No data retrieved for result: %s" % link)
                            continue
                        lines = self.build_text(results, link)
                        f, e = self.check_or_create_res_dir(filepath, link, i)
                        f += "/"
                        if e: # result already saved
                            continue
                        self.download_photos(f, results)
                        fu = FileUtils(f + "info.txt")
                        if html.encoding:
                            fu.write(lines.encode(html.encoding))
                        else:
                            fu.write(lines)
                        i += 1
                    except Exception as e:
                        print("[-] Search result: %s could not be processed: %s" % (link, str(e)) )
                        import sys, os
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                if links and links[0]:
                    fu = FileUtils(search_filepath + "last_result")
                    fu.write(links[0])
                print("[+] %s results processed" % str(i))
            except Exception as e:
                print("[-] Something went wrong: %s" % e)

        return results

    def build_text(self, results, link):
        lines = "[+] DATA RETRIEVED:\n\n"
        if results.has_key("price") and results["price"] != None:
            lines += "Price: " + results["price"] + "\n"
        if results.has_key("size") and results["size"] != None:
            lines += "Size: " + results["size"] + " metros\n"
        if results.has_key("rooms") and results["rooms"] != None:
            lines += "Rooms: " + results["rooms"]+ "\n"
        if results.has_key("baths") and results["baths"] != None:
            lines += "Bathrooms: " + results["baths"] + "\n"
        if results.has_key("street") and results["street"] != None:
            lines += "Street: " + results["street"] + "\n"
        if results.has_key("parquet") and results["parquet"] != None:
            if results["parquet"]:
                lines += "Parquet: Yes\n"
            else:
                lines += "Parquet: No\n"
        lines += "Link: " + link
        return lines

    def check_or_create_params_dir(self):
        filepath = "results/" + self.engine + "_minp_" + str(self.minp) + "_maxp_" + str(self.maxp) + "_mins_" + str(self.mins) + "_f_" + str(self.f)
        if not OSUtils.check_folder(filepath):
            OSUtils.create_folder(filepath)
        return filepath

    def check_last_result(self, filepath):
        last_link = None
        try:
            with open(filepath + "last_result") as f:
                last_link = f.readline().strip()
                if not last_link:
                    print("[*] No previous results saved.")
        except (OSError, IOError):
            # File doesn't exist
            print("[*] No previous results saved.")
        return last_link

    def check_or_create_today_dir(self, filepath):
        date_str = OSUtils.get_date()
        filepath += date_str
        if not OSUtils.check_folder(filepath):
            OSUtils.create_folder(filepath)
        return filepath

    def check_or_create_res_dir(self, filepath, link, i):
        dir_name = ""
        existed = True
        link_list = link.split("/")
        length = len(link_list)
        if length < 2:
            dir_name = str(i)
        else:
            if link_list[length-1] == "":
                dir_name = link_list[length-2]
            else:
                dir_name =link_list[length-1]

        filepath += dir_name
        if not OSUtils.check_folder(filepath):
            existed = False
            OSUtils.create_folder(filepath)
        return filepath, existed

    def download_photos(self, filepath, results):
        if results.has_key("photos"):
            i = 0
            for photo_link in results["photos"]:
                hu = HTTPUtils(photo_link)
                res = hu.make_request()
                photo_list = photo_link.split(".")
                ext = photo_list[len(photo_list) - 1]
                fu = FileUtils(filepath + str(i) + "." + ext)
                fu.write_binary(res.content)
                i += 1
        else:
            print("[*] No photos to download.")

    def build_request(self):

        params = {}
        url = ""
        if args.engine == "fotocasa.es":
            url = "http://www.fotocasa.es/viviendas/barcelona-capital/alquiler/listado"
            if self.minp:
                params["minp"] = self.minp
            if self.maxp:
                params["maxp"] = self.maxp
            if self.mins:
                params["mins"] = self.mins
            if self.f:
                params["esm"] = "19;"
        elif args.engine == "idealista.com":
            print("[-] Still not implemented.")
        return url, params

    @staticmethod
    def parse_arguments():

        desc = """
        Launch parameterized queries to different house renting sites and get
        house photos and important information such as price, size or rooms.
        """
        import argparse
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument("-e", "--engine",  help= """
                        Search engine to use.
                        """, choices=["fotocasa.es","idealista.com"]
                        )
        parser.add_argument("-minp", "--minprice",  help= """
                        Specify the minimum price.
                       """, type=int)
        parser.add_argument("-maxp", "--maxprice",  help= """
                        Specify the maximum price.
                       """, type=int)
        parser.add_argument("-mins", "--minsize",  help= """
                        Specify the minimum size in square meter.
                       """, type=int)
        parser.add_argument("-f", "--furnished",  help= """
                        Specify if the flat must be furnished.
                       """, action="store_true")
        parser.add_argument("-l", "--limit",  help= """
                        Limit the number of results.
                       """, type=int)
        parser.add_argument("-op", "--output_path",  help= """
                        Output path in which save results.
                       """, type=int)
        parser.add_argument("-cf", "--config_file",  help= """
                        Configuration file from which get parameters.
                       """, type=int)
        return parser.parse_args()


if __name__ == "__main__":
    """
    <a class="property-location" id="130887074" propertyid="130887074" href="/vivienda/barcelona-capital/piscina-comunitaria-horta-centro-130887074"
    fu = FileUtils("./image.gif")
    hu = HTTPUtils("http://www.fotocasa.es/viviendas/barcelona-capital/alquiler/listado?mins=55&minp=550&maxp=700&esm=19")
    html = hu.make_request()
    """
    
    args = Main.parse_arguments()
    m = Main(args)
    m.run()



