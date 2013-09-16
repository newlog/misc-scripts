Rent First
=======

This is a weekend project I built to be the first to know which flats appear for rent in Barcelona. So as you can imagine, if you are not from Spain, you won't find this of much useful. The idea behind this project is to automate the search of flats for rent, so you execute this script to obtain new flats for rent in your region and get their photos and important information.

Nevertheless, if you are here watching projects in Github is because you are a code lover :) In this project you can find how to use the following libraries:

- [argparse](http://docs.python.org/dev/library/argparse.html)
- [BeautifulSoup](http://docs.python-requests.org/en/latest/)
- [Requests](http://www.crummy.com/software/BeautifulSoup/)

Installation
----------------

If you have the libraries mentioned in the previous section, you don't have to do anything. If not, is as simple as:

    $ pip install -r requirements.txt

The requirements.txt file is in the main project directory. If you have any problem using pip (you might have to use *sudo*), install the libraries as explained in the their webpages. It's easy ;)

Usage
----------

Here comes the magic of argparse :)

    $ ./main.py -h
    usage: main.py [-h] [-e {fotocasa.es,idealista.com}] [-minp MINPRICE]
               [-maxp MAXPRICE] [-mins MINSIZE] [-f] [-l LIMIT]
               [-op OUTPUT_PATH] [-cf CONFIG_FILE]

    Launch parameterized queries to different house renting sites and 
    get house photos and important information such as price, size or rooms.

    optional arguments:
      -h, --help            show this help message and exit
      -e {fotocasa.es,idealista.com}, --engine {fotocasa.es,idealista.com}
                            Search engine to use.
      -minp MINPRICE, --minprice MINPRICE
                            Specify the minimum price.
      -maxp MAXPRICE, --maxprice MAXPRICE
                            Specify the maximum price.
      -mins MINSIZE, --minsize MINSIZE
                            Specify the minimum size in square meter.
      -f, --furnished       Specify if the flat must be furnished.
      -l LIMIT, --limit LIMIT
                            Limit the number of results.
      -op OUTPUT_PATH, --output_path OUTPUT_PATH
                            Output path in which save results.
      -cf CONFIG_FILE, --config_file CONFIG_FILE
                            Configuration file from which get parameters.

An example to launch the script follows:

    $ ./main.py -e fotocasa.es -minp 600 -maxp 700 -mins 60 -f

This query will create the next directory structure:

- results
    - fotocasa.es\_minp\_600\_maxp\_700\_mins\_60\_f\_True
        - 15-08-2013
            - flat\_identifier\_1
                - photo\_1
                - photo\_2
                - (...)
                - photo\_n
                - info.txt
            - flat\_identifier\_2
                - photo\_1
                - photo\_2
                - (...)
                - photo\_n
                - info.txt
            - (...)

Farewell
-------------

And that's it, folks! Enjoy the code and be the first to find the "gangas" to rent :P
