#!/usr/bin/env python3
"""
Automation for CyberArk's Discovery & Audit (DNA) reports.
"""

import argparse
import logging
from collections import defaultdict

import logzero
from dnamic_analysis import Database
import dnamic_analysis.metrics as Metrics
from logzero import logger
from tests import Tests

__author__ = "Joe Garcia, CISSP"
__version__ = "0.1.0"
__license__ = "MIT"

LOGFILE = 'DNAmicAnalysis.log'

def config_logger(logfile):
    """ Configures logging of this application """
    # Set a minimum log level
    logzero.loglevel(logging.INFO)

    # Set a logfile (all future log messages are also saved there), but disable the default stderr logging
    logzero.logfile(logfile, disableStderrLogger=True)

    # Set a custom formatter
    formatter = logging.Formatter('DNAmicAnalysis - %(asctime)-15s - %(levelname)s: %(message)s');
    logzero.formatter(formatter)


def main(args):
    """ Main entry point of the app """

    logger.info("Arguments received: {}".format(args))

    db = Database(args.database_file)

    """ Expired Domain Privileged IDs """

    expired_domain = db.exec_fromfile("data/sql/ExpiredDomainPrivID.sql")
    all_domain_count = db.exec_fromfile("data/sql/DomainAdminsPUCount.sql")

    domainMaxSorted = Metrics.domain_max(expired_domain)
    domainAverage = Metrics.domain_avg(expired_domain)
    domainPercent = Metrics.domain_percent(expired_domain, all_domain_count, domainMaxSorted)

    # If --test detected, make results verbose to console
    if args.test is True:
        Tests.domain_expired(
            domainMaxSorted,
            domainAverage[0],
            domainAverage[1],
            domainAverage[2],
            domainPercent[0],
            domainPercent[1],
            domainPercent[2])
        input("Press ENTER to continue...")
        print()

    """ Unique Expired Local Privileged IDs """

    expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql")
    all_local_count = db.exec_fromfile("data/sql/LocalAdministratorsCount.sql")

    localMaxSorted = Metrics.local_max(expired_local)
    localAverage = Metrics.local_avg(expired_local)
    localPercent = Metrics.local_percent(expired_local, all_local_count, localMaxSorted)

    # If --test detected, make results verbose to console
    if args.test is True:
        Tests.local_expired(
            localMaxSorted,
            localAverage[0],
            localAverage[1],
            localAverage[2],
            localPercent[0],
            localPercent[1],
            localPercent[2])
        input("Press ENTER to continue...")
        print()

    """ Expired Local Admins Total w/ Machine Names """

    # Take localMaxSorted first 2 values in each row and add to var
    localMaxPruned = [metric[0:2] for metric in localMaxSorted]
    # Create blank set
    localMaxGrouped = {}
    # Group by machine and add to set previously created
    for account, machine in localMaxPruned:
        if machine in localMaxGrouped:
            localMaxGrouped[machine].append((account))
        else:
            localMaxGrouped[machine] = [(account)]
    
    # If --test detected, make results verbose to console
    if args.test is True:
        Tests.local_expired_machines(localMaxGrouped, len(all_local_count))
        input("Press ENTER to continue...")
        print()

    """ Local Abandoned Accounts """

    abandoned_local = db.exec_fromfile("data/sql/LocalAbandonedAccounts.sql")

    # If --test detected, make results verbose to console
    if args.test is True:
        Tests.local_abandoned(abandoned_local, len(all_local_count))
        input("Press ENTER to continue...")
        print()


if __name__ == "__main__":
    """ This is executed when run from the command line """

    # Configure logging
    config_logger(LOGFILE)
    logger.info("Application initialized successfully")

    # Create argument parsing object
    parser = argparse.ArgumentParser(description="CyberArk DNA report generation utility")

    # Required positional argument for database file to query against
    parser.add_argument(
        "database_file",
        help="Path to the CyberArk DNA SQLite3 database file")

    # Optional argument flag for testing
    parser.add_argument(
        "--test",
        action="store_true",
        dest="test",
        help="For testing purposes only",
        default=True
    )

    # Optional argument flag to output current version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
        help="Shows current version information and exit")

    try:
        args = parser.parse_args()
    except:
        logger.error("Invalid argument(s) passed at initialization")
        raise

    main(args)
