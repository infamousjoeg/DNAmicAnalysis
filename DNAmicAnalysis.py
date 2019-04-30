#!/usr/bin/env python3
"""
Automation for CyberArk's Discovery & Audit (DNA) reports.
"""

__author__ = "Joe Garcia, CISSP"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import logging
import sqlite3
from sqlite3 import Error

import logzero
from logzero import logger

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


def create_connection(dbfile):
    """ Create a database connection to the SQLite database """
    try:
        conn = sqlite3.connect(dbfile)
        logger.info("Successfully connected to SQLite3 database at {}".format(dbfile))
        return conn
    except Error as e:
        logger.exception(e)

    return None


def exec_fromfile(dbfile, sqlfile):
    """ Executes the query from a SQL file and returns all rows """
    # Open and read the SQL file as a single buffer
    fileToRead = open(sqlfile, 'r')
    logger.info("Opened {}".format(sqlfile))
    sqlQuery = fileToRead.read()
    logger.info("Read {}".format(sqlfile))
    fileToRead.close()
    logger.info("Closed {}".format(sqlfile))

    # Create database connection
    conn = create_connection(dbfile)

    # Create a cursor for the database connection
    c = conn.cursor()
    logger.info("Created database connection cursor")

    # Execute the SQL query
    try:
        c.execute(sqlQuery)
        logger.info("Executed {} on SQLite3 database successfully".format(sqlQuery))
    except Error as e:
        logger.exception(e)

    # Fetch all rows returned from SQL query
    try:
        fetched_rows = c.fetchall()
        row_count = len(fetched_rows)
        logger.info("Fetched {} rows".format(row_count))
    except Error as e:
        logger.exception(e)
    finally:
        conn.close()


    # Return all rows returned from SQL query
    return fetched_rows


def main(args):
    """ Main entry point of the app """
    logger.info("Arguments received: {}".format(args))

    # Execute SQL queries
    expired_domain = exec_fromfile(args.database_file, "data/sql/ExpiredDomainPrivID.sql")
    expired_local = exec_fromfile(args.database_file, "data/sql/UniqueExpiredLocalPrivID.sql")

    print(expired_domain)
    print("----------------------------------------")
    print(expired_local)


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

    # Optional argument flag to output current version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
        help="Displays current version information")

    args = parser.parse_args()
    main(args)
