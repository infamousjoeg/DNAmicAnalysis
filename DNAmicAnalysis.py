#!/usr/bin/env python3
"""
Automation for CyberArk's Discovery & Audit (DNA) reports.
"""

import argparse
import logging

import logzero
import tests.tests as tests
from dnamic_analysis import Database
from logzero import logger

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

    # Execute SQL queries
    expired_domain = db.exec_fromfile("data/sql/ExpiredDomainPrivID.sql")
    expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql")

    ### TODO
    # Percentage based on total accounts in report
    max_domain_sorted = sorted(expired_domain,
                            key=lambda expired_domain: expired_domain[2],
                            reverse=True)
    avg_domain_sorted = sorted(expired_domain,
                            key=lambda expired_domain: expired_domain[3],
                            reverse=True)
    max_local_sorted = sorted(expired_local,
                            key=lambda expired_local: expired_local[2],
                            reverse=False)
    avg_local_sorted = sorted(expired_local,
                            key=lambda expired_local: expired_local[3],
                            reverse=True)
    count_local_accounts = len(expired_local)

    if args.test is True:
        tests.print_sorted(
            max_domain_sorted,
            avg_domain_sorted,
            max_local_sorted,
            avg_local_sorted,
            count_local_accounts)


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
        default=False
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
