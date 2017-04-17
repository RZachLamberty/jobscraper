#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: jobscraper.py
Author: zlamberty
Created: 2017-04-16

Description:
    generic scraper class; mostly to make publishing uniform

Usage:
    <usage>

"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..model import JobPosting


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

class JobScraper(object):
    """class to establish the required api for job scrapers"""
    def __init__(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def publish(self):
        raise NotImplementedError()


class JobScraperPsql(JobScraper):
    """extend api to auto-publish to psql"""
    def __init__(self, url, verbose=False):
        self.engine = create_engine(url, echo=True if verbose else False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get(self):
        raise NotImplementedError()

    def stage_job(self, **kwargs):
        self.session.add(JobPosting(**kwargs))

    def publish(self):
        self.session.commit()
