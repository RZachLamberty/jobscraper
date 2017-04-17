#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: senatedotgov.py
Author: zlamberty
Created: 2017-04-16

Description:
    scraper for senate.gov job postings

Usage:
    <usage>

"""

import logging

import lxml.html
import requests

from .jobscraper import JobScraperPsql


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)


# ----------------------------- #
#   job scraper                 #
# ----------------------------- #

class SenateDotGov(JobScraperPsql):
    def __init__(self, rootUrl, dbUrl, verbose=False):
        super().__init__(url=dbUrl, verbose=verbose)
        self.rootUrl = rootUrl

    def get(self):
        self.resp = requests.get(self.rootUrl)
        self.root = lxml.html.fromstring(self.resp.text)

        for tab in self.root.xpath('//td[@class="contenttext"]/table'):
            try:
                title = '{regtitle} ({postid})'.format(
                    regtitle=tab.xpath(
                        'tr/td[not(@valign) and @class="po_employment"]/b'
                    )[0].text,
                    postid=tab.find('tr/td[@valign="top"]/b').text
                )
                company = 'US Senate'
                description = tab.xpath('tr/td[not(@valign) and @class="po_employment"]/p')[0].text
                title = title.strip()
                description = description.strip()
                self.stage_job(
                    title=title,
                    company=company,
                    description=description,
                    url=self.rootUrl,
                    source='senate_dot_gov'
                )
            except AttributeError as e:
                logger.error(e)
                print("skipping non-matching tab")


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def main(rootUrl, dbUrl, verbose=False):
    """just a wrapper for running the above given command line args

    args:

    returns:

    raises:

    """
    sdg = SenateDotGov(
        rootUrl=rootUrl,
        dbUrl=dbUrl,
        verbose=verbose
    )
    sdg.get()
    sdg.publish()


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
        conf = yaml.load(f)['senate_dot_gov']

    main(**conf)
