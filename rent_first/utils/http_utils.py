#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import requests
except ImportError:
    print("[-] Required library not installed in system.")
    print("[-] Execute: pip install -r requirements.txt")
    exit()

class HTTPUtils(object):
    def __init__(self, url, username=None, password=None, params=None):

        if not url:
            print("[-] An HTTP url should be specified.")
            return
        self.url = url
        self.usr = username
        self.pwd = password
        self.params = params

    def make_request(self):
        result = None
        try:
            result = requests.get(url=self.url, params=self.params)
        except Exception as e:
            print("[-] Error making HTTP request: %s" % e)
        return result

    @staticmethod
    def parse_arguments():
        desc = """
        This utility is used to make HTTP requests. By default, it handles
        authentication and GET parameters. It is intended as a start point
        to be extended. It uses external Requests library.
        """
        import argparse
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument("URL", help= """
                        URL to request. Ex.: www.overflowedminds.net
                        If parameters exist: www.overflowedminds.net/hello.php
                        """
                        )
        parser.add_argument("-c", "--credentials",  help= """
                        Specify user and password as: user,password
                       """)
        parser.add_argument("-p", "--parameters",  help= """
                        Specify request parameters as: key1=value1,key2=value2
                       """)
        return parser.parse_args()

if __name__ == "__main__":

    user= None
    pwd = None
    params = {}
    args = HTTPUtils.parse_arguments()
    if args.credentials:
        if args.credentials.find(",") != -1:
            user, pwd = args.credentials.split(",", 1)
    if args.parameters:
        param_list = args.parameters.split(",")
        for pair in param_list:
            if pair.find("=") != -1:
                key, value = pair.split("=")
                params[key] = value

    hu = HTTPUtils(args.URL, user, pwd, params)
    r = hu.make_request()


