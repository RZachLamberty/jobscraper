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

import logging

import sqlalchemy

from . import db

# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)


# ----------------------------- #
#   job posting model           #
# ----------------------------- #

class JobPosting(db.Model):
    __tablename__ = 'job_posting'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    company = db.Column(db.Text)
    description = db.Column(db.Text)
    url = db.Column(db.Text)
    source = db.Column(db.Text)
    posting_timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return "<JobPosting(id={}, url={})>".format(self.id, self.url)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'url': self.url,
            'source': self.source,
            'posting_timestamp': self.posting_timestamp,
        }


# ----------------------------- #
#   init that ish               #
# ----------------------------- #

def bootstrap(dbUrl, echo=False):
    engine = sqlalchemy.create_engine(dbUrl, echo=echo)
    JobPosting.__table__.create(engine)


def drop_em(dbUrl, echo=False):
    engine = sqlalchemy.create_engine(dbUrl, echo=echo)
    JobPosting.__table__.drop(engine)
