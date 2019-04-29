#!/usr/bin/env python3
"""
Automation for CyberArk's Discovery & Audit (DNA) reports.
"""

__author__ = "Joe Garcia, CISSP"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import sqlite3
from sqlite3 import Error

import logzero
from logzero import logger


def config_logger(logfile, debug):
    """ Configures logging of this application """
    # Format logfile path in logfile variable
    if logfile is None:
        logfile = "DNAmicAnalysis.log"
    else:
        logfile = logfile.rstrip()
        if logfile.endswith('/'):
            logfile = logfile[:-1]
        logfile = logfile + "/DNAmicAnalysis.log"

    # Set a minimum log level
    if debug is None:
        logzero.loglevel(logging.INFO)
    else:
        logzero.loglevel(logging.DEBUG)

    # Set a logfile (all future log messages are also saved there), but disable the default stderr logging
    logzero.logfile(logfile, disableStderrLogger=True)

    # Log to syslog, using default logzero logger and 'local0' syslog facility
    logzero.syslog(facility=SysLogHandler.LOG_LOCAL0)

    # Set a custom formatter
    formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
    logzero.formatter(formatter)


def create_connection(dbfile):
    """ Create a database connection to the SQLite database """
    try:
        conn = sqlite3.connect(dbfile)
        logger.info("Successfully connected to SQLite3 database at ", dbfile)
        return conn
    except Error as e:
        logger.exception(e)

    return None


def exec_fromfile(sqlfile):
    """ Executes the query from a SQL file and returns all rows """
    # Open and read the SQL file as a single buffer
    fileToRead = open(sqlfile, 'r')
    logger.info("Opened ", sqlfile)
    sqlQuery = fileToRead.read()
    logger.info("Read ", sqlfile)
    fileToRead.close()
    logger.info("Closed ", sqlfile)

    # Create a cursor for the database connection
    c = conn.cursor
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

    # Return all rows returned from SQL query
    return fetched_rows


def main(args):
    """ Main entry point of the app """
    logger.debug("Arguments received: ", args)

    # Create database connection
    conn = create_connection(database)
    with conn:
        expired_domain = exec_fromfile(data/sql/ExpiredDomainPrivID.sql)
        expired_local = exec_fromfile(data/sql/UniqueExpiredLocalPrivID.sql)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    # Configure logging
    config_logger(logfile, debug)
    logger.info("Application initialized successfully")

    # Create argument parsing object
    parser = argparse.ArgumentParser(description="CyberArk DNA report generation utility")

    # Required positional argument for database file to query against
    parser.add_argument(
        "database_file",
        dest="dbfile",
        help="Path to the CyberArk DNA SQLite3 database file")

    # Optional argument flag to set minimum log level to DEBUG - Default: INFO
    parser.add_argument(
        "--debug",
        action="store_true",
        dest="debug",
        default=False,
        help="Sets DEBUG as the minimum log level [Default: INFO]")

    # Optional argument flag to set the log file path - Default: root directory of script
    parser.add_argument(
        "-l",
        "--logfile",
        dest="logfile",
        help="Sets the path for the log file to be generated [Default: root directory of script]"
    )

    # Optional argument flag to output current version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
        help="Displays current version information")

    args = parser.parse_args()
    main(args)
