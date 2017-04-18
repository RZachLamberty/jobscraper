#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: thehill.py
Author: zlamberty
Created: 2017-04-16

Description:
    scraper for rcjobs.com job postings

Usage:
    <usage>

"""

import logging
import re
import urllib

import lxml.html
import requests

import html2text

from .jobscraper import JobScraperPsql


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)

BASE_URL = 'http://thehill.com/'


# ----------------------------- #
#   job scraper                 #
# ----------------------------- #

class TheHillScraper(JobScraperPsql):
    def __init__(self, searchUrl, dbUrl, verbose=False, baseUrl=BASE_URL):
        super().__init__(url=dbUrl, verbose=verbose)
        self.searchUrl = searchUrl
        self.baseUrl = baseUrl

    def get(self):
        for root in self._get_root_pages():
            for el in root.xpath('.//article'):
                try:
                    titleElem = el.find('./header/h2/a')
                    title = titleElem.text.strip()
                    company = None
                    url = urllib.parse.urljoin(self.baseUrl, titleElem.attrib['href'])
                    description = el.find('./header/div[@class="body"]').text.strip()
                    self.stage_job(
                        title=title,
                        company=company,
                        description=description,
                        url=url,
                        source='the_hill'
                    )
                except AttributeError as e:
                    logger.error(e)
                    print("skipping non-matching tab")

    def _get_root_pages(self):
        nextUrl = self.searchUrl
        while True:
            resp = requests.get(nextUrl)
            root = lxml.html.fromstring(resp.text)
            yield root

            try:
                nextUrl = urllib.parse.urljoin(
                    self.baseUrl, root.find('.//a[@rel="next"]').attrib['href']
                )
            except:
                logger.info('no more pages to find')
                break


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def main(searchUrl, dbUrl, verbose=False, baseUrl=BASE_URL):
    """just a wrapper for running the above given command line args

    args:

    returns:

    raises:

    """
    thj = TheHillScraper(
        searchUrl=searchUrl,
        dbUrl=dbUrl,
        verbose=verbose,
        baseUrl=baseUrl
    )
    thj.get()
    thj.publish()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

def parse_args():
    """ Take a log file from the commmand line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="a path to a config file")

    args = parser.parse_args()

    logger.debug("arguments set to {}".format(vars(args)))

    return args


if __name__ == '__main__':

    args = parse_args()

    with open(args.config, 'r') as f:
        conf = yaml.load(f)['thehill']

    main(**conf)
