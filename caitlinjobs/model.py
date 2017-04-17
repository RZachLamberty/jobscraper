#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: model.py
Author: zlamberty
Created: 2017-04-16

Description:
    model for a webscrapable job

Usage:
    <usage>

"""

import argparse
import logging
import logging.config
import os
import yaml

import sqlalchemy

from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)

Base = declarative_base()


# ----------------------------- #
#   job posting model           #
# ----------------------------- #

class JobPosting(Base):
    __tablename__ = 'job_posting'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    company = Column(Text)
    description = Column(Text)
    url = Column(Text)
    source = Column(Text)
    posting_timestamp = Column(DateTime)

    def __repr__(self):
        return "<JobPosting(id={}, url={})>".format(self.id, self.url)


# ----------------------------- #
#   init that ish               #
# ----------------------------- #

def bootstrap(dbUrl):
    engine = sqlalchemy.create_engine(dbUrl, echo=True)
    Base.metadata.create_all(engine)
