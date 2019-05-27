#!/usr/bin/env python3
"""
Automation for CyberArk's Discovery & Audit (DNA) reports.
"""

import argparse
import logging
from collections import defaultdict

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
    all_domain_count = db.exec_fromfile("data/sql/ExpiredDomainPrivIDCnt.sql")
    expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql")
    all_local_count = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivIDCnt.sql")

    # Sorting Expired (non-compliant) Domain Accounts by Max Password Age
    max_domain_sorted = sorted(expired_domain,
                            key=lambda expired_domain: expired_domain[2],
                            reverse=True)
    
    # Create list of Average Password Age values non-compliant
    avg_domain_values = [x[3] for x in expired_domain]

    # Calculate Average Password Age of all Domain accounts expired (non-compliant)
    avg_domain_overall = sum(avg_domain_values) / len(avg_domain_values)
    logger.info("Calculated Overall Average Password Age for Expired Domain Accounts using: {} / {}".format(sum(avg_domain_values),len(avg_domain_values)))
    
    # Calculate percentage overall of Expired (non-compliant) Domain accounts
    percent_domain_overall = len(max_domain_sorted) / len(all_domain_count)
    logger.info("Calulated Percentage Overall Non-Compliant Expired Domain Accounts using: {} / {}".format(len(max_domain_sorted),len(all_domain_count)))

    # Sorting Unique Expired (non-compliant) Local Accounts by Max Password Age
    max_local_sorted = sorted(expired_local,
                            key=lambda expired_local: expired_local[2],
                            reverse=False)

    # Create list of Average Password Age values non-compliant
    avg_local_values = [x[4] for x in expired_local]

    # Calculate Average Password Age of all Local accounts expired (non-compliant)
    avg_local_overall = sum(avg_local_values) / len(avg_local_values)
    logger.info("Calculated Overall Average Password Age for Expired Local Accounts using: {} / {}".format(sum(avg_local_values),len(avg_local_values)))

    # Calculate percentage overall of Expired (non-compliant) Local accounts
    percent_local_overall = len(max_local_sorted) / len(all_local_count)
    logger.info("Calulated Percentage Overall Non-Compliant Expired Local Accounts using: {} / {}".format(len(max_local_sorted),len(all_local_count)))

    # If --test is detected, values will be pretty-output to console
    if args.test is True:
        tests.print_sorted(
            max_domain_sorted,
            avg_domain_overall,
            percent_domain_overall,
            max_local_sorted,
            avg_local_overall,
            percent_local_overall,
            len(expired_local))


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
