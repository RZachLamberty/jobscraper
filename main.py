#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: main.py
Author: zlamberty
Created: 2017-04-16

Description:


Usage:
    <usage>

"""

import argparse
import logging
import logging.config
import os
import yaml

import caitlinjobs.scrape.idealist
import caitlinjobs.scrape.rollcall
import caitlinjobs.scrape.senatedotgov
import caitlinjobs.scrape.thehill


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('caitlinjobs')
LOGCONF = os.path.join(HERE, 'caitlinjobs', 'logging.yaml')
with open(LOGCONF, 'rb') as f:
    logging.config.dictConfig(yaml.load(f))
logging.getLogger('requests').setLevel(logging.INFO)


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def scrape(fconf):
    """given a configuration file, go get job postings and persist them to
    the database

    args:
        fconf (str): path to the yaml configuration file. nodes in this file
            should have names and sub-structure commensurate with the individual
             scrapers' requirements

    returns:
        None

    raises:
        None

    """
    with open(fconf, 'r') as f:
        conf = yaml.load(f)

    caitlinjobs.scrape.idealist.main(**conf['idealist'])
    caitlinjobs.scrape.rollcall.main(**conf['rollcall'])
    caitlinjobs.scrape.senatedotgov.main(**conf['senatedotgov'])
    caitlinjobs.scrape.thehill.main(**conf['thehill'])


# ----------------------------- #
#   Command line                #
# ----------------------------- #

def parse_args():
    """ Take a log file from the commmand line """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--conf", help="yaml configuration file", default='conf.yaml'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    scrape(args.conf)
