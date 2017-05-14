#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: idealist.py
Author: zlamberty
Created: 2017-04-16

Description:
    scraper for rcjobs.com job postings

Usage:
    <usage>

"""

import logging
import urllib

import requests

from .jobscraper import JobScraperPsql


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)

BASE_URL = 'http://www.idealist.org/en/'


# ----------------------------- #
#   job scraper                 #
# ----------------------------- #

class IdealistScraper(JobScraperPsql):
    def __init__(self, searchUrl, dbUrl, verbose=False, baseUrl=BASE_URL):
        super().__init__(url=dbUrl, verbose=verbose)
        self.searchUrl = searchUrl
        self.baseUrl = baseUrl

    def get(self):
        params = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript (lite) 3.22.1',
            'x-algolia-application-id': 'NSV3AUESS7',
            'x-algolia-api-key': 'c2730ea10ab82787f2f3cc961e8c1e06',
        }
        jobFilter = "type:'JOB' AND isFullTime:true AND education:'FOUR_YEAR_DEGREE' AND professionalLevel:'PROFESSIONAL'"
        qryparams = {
            "query": None,
            "aroundLatLng": "38.907192, -77.036871",
            "minimumAroundRadius": 2000,
            "aroundPrecision": 1000,
            "aroundRadius": 100000,
            "filters": jobFilter
        }
        qrystring = "&".join(
            '{}={}'.format(k, requests.utils.quote(str(v or "")))
            for (k, v) in qryparams.items()
        )
        data = {
            "params": qrystring,
        }
        resp = requests.post(self.searchUrl, json=data, params=params)
        j = resp.json()
        for job in j['hits']:
            self.stage_job(
                title=job['name'],
                company=job['orgName'],
                description=job['description'],
                url=urllib.parse.urljoin(self.baseUrl, job['url']['en']),
                source='idealist'
            )


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def main(searchUrl, dbUrl, verbose=False, baseUrl=BASE_URL):
    """just a wrapper for running the above given command line args

    args:

    returns:

    raises:

    """
    ij = IdealistScraper(
        searchUrl=searchUrl,
        dbUrl=dbUrl,
        verbose=verbose,
        baseUrl=baseUrl
    )
    ij.get()
    ij.publish()


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
        conf = yaml.load(f)['idealist']

    main(**conf)
