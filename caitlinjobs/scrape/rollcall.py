#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: rollcall.py
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

BASE_URL = 'http://www.rcjobs.com/'


# ----------------------------- #
#   job scraper                 #
# ----------------------------- #

class RcJobsScraper(JobScraperPsql):
    def __init__(self, searchUrl, dbUrl, verbose=False, baseUrl=BASE_URL):
        super().__init__(url=dbUrl, verbose=verbose)
        self.searchUrl = searchUrl
        self.baseUrl = baseUrl

    def get(self):
        self.resp = requests.get(self.searchUrl)
        self.root = lxml.html.fromstring(self.resp.text)

        for el in self.root.cssselect('.ga_job'):
            try:
                title = el.find('span').text.strip()
                company = el.getparent().find('strong').text.strip()
                descUrl = urllib.parse.urljoin(self.baseUrl, el.attrib['href'])
                description = self._get_desc(descUrl)
                self.stage_job(
                    title=title,
                    company=company,
                    description=description,
                    url=self.searchUrl,
                    source='roll_call'
                )
            except AttributeError as e:
                logger.error(e)
                print("skipping non-matching tab")

    def _get_desc(self, descUrl):
        """given the full url to a single job posting, go grab and return
        the description

        """
        resp = requests.get(descUrl)
        root = lxml.html.fromstring(resp.text)
        deets = root.find('.//div[@class="generic-details-text"]')
        deetsHtml = lxml.html.tostring(deets)
        deetsHtml = re.subn(b'\\r|\\n|\\t', b'', deetsHtml)[0]
        deetsMd = html2text.html2text(deetsHtml.decode('utf-8').strip()).strip()

        return deetsMd


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def main(searchUrl, dbUrl, verbose=False, baseUrl=BASE_URL):
    """just a wrapper for running the above given command line args

    args:

    returns:

    raises:

    """
    rcj = RcJobsScraper(
        searchUrl=searchUrl,
        dbUrl=dbUrl,
        verbose=verbose,
        baseUrl=baseUrl
    )
    rcj.get()
    rcj.publish()


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
        conf = yaml.load(f)['rollcall']

    main(**conf)
