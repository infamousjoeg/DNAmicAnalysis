import ntpath
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

from logzero import logger


class Database(object):

    def __init__(self, dbfiles, disabled, scan_datetime, expiration_days):
        # Create array of file path(s) to database file(s)
        self._dbfiles = []
        for dbfile in dbfiles:
            self._dbfiles.append(Path(dbfile))

        self._expirationDays = str(expiration_days)
        self._disabledSqlQuery = "0"
        if disabled is False:
            self._disabledSqlQuery = "1"
        self._flagScanDateTime = scan_datetime['override']
        self._progressIndex = 0
        self._metricName = None
        # Set the value below to increase performance for larger data sets
        # Note: This is the amount of SQLite VMs per progress report - NOT RESULTS!
        self._progressIncrement = 100000

        # Parse scan date & time if no override detected
        self._scanDateTime = []
        i = 0
        if not self._flagScanDateTime:
            for dbfile in self._dbfiles:
                # Split to arrays
                dbFileName = ntpath.basename(dbfile)
                dbFileNameSplit = dbFileName.split("_")
                dnaIndex = dbFileNameSplit.index("DNA")
                dIndex = dnaIndex + 1
                tIndex = dIndex + 1
                dbFileTimeSplit = dbFileNameSplit[tIndex].split(".")
                try:
                    # Format as proper datetime value
                    inScanTime = datetime.strptime(dbFileTimeSplit[0].replace("-", " "), "%I %M %S %p")
                except ValueError:
                    print("DNAmic Analysis does not support 24-hour format in DNA database filenames:", dbFileTimeSplit[0])
                    print("FIX: Either change the filename to 12-hour format or change your config YAML to override scan datetime.")
                    print("--------------------------")
                    raise
                # Strip 1900-01-01 placemarker date and format to 24-hour
                scanTime = datetime.strftime(inScanTime, "%H:%M:%S")
                # Combine datetime for SQL query
                self._scanDateTime.append(dbFileNameSplit[dIndex] + " " + scanTime)
                logger.info("Parsed scan datetime from database filename: {}".format(self._scanDateTime[i]))
                i = i + 1
        else:
            for dbfile in self._dbfiles:
                self._scanDateTime.append(scan_datetime['manual_scan_datetime'])
                logger.info("Manual override detected, received scan datetime as: {}".format(self._scanDateTime[i]))
                i = i + 1


    def progress_handler(self):
        """ Handles progress animation during SQLite database queries """
        self._progressIndex += 1
        print("{} Processing... [{}]".format(self._metricName, self._progressIndex), end="\r", flush=True)


    def create_connection(self, dbfile):
        """ Create a database connection to the SQLite database """
        try:
            conn = sqlite3.connect(dbfile)
            logger.info("Successfully connected to SQLite3 database at {}".format(dbfile))
            return conn
        except Error as e:
            logger.exception(e)

        return None


    def exec_fromfile(self, sqlfile, metric_name, regex_flag=False, regex_array=None):
        """ Executes the query from a SQL file and returns all rows """
        # Open and read the SQL file as a single buffer
        try:
            with open(sqlfile, 'r') as file:
                sqlQuery = file.read()
            logger.info("Opened & read {}".format(sqlfile))
        except Exception as e:
            logger.exception(e)

        ################################################################
        # BEGIN FOR LOOP ON SQLITE CONNECTIONS
        ################################################################
        i = 0
        all_fetched_rows = []
        for dbfile in self._dbfiles:
            # Create database connection
            try:
                conn = self.create_connection(dbfile)
                self._metricName = metric_name
                conn.set_progress_handler(self.progress_handler, self._progressIncrement)

                # Create a cursor for the database connection
                c = conn.cursor()
                logger.info("Created database connection cursor")
            except Error as e:
                logger.exception(e)

            try:
                # Make replacement in SQL query
                sqlQueryDT = sqlQuery.replace("{scanDateTime}", self._scanDateTime[i])
                sqlQueryExpire = sqlQueryDT.replace("{expirationDays}", self._expirationDays)
                # Replace disabled section of SQL query
                sqlQueryFinal = sqlQueryExpire.replace("{disabled}", self._disabledSqlQuery)
            except Exception as e:
                logger.exception(e)

            # Execute the SQL query
            logger.info("Starting query execution and analysis.")
            if regex_flag:
                try:
                    whereStmt = ""
                    counter = 0
                    for regex in regex_array:
                        if counter == 0:
                            whereStmt += "Accounts.Name LIKE '{}' ".format(regex.replace('^','%'))
                        else:
                            whereStmt += "OR Accounts.Name LIKE '{}' ".format(regex.replace('^','%'))
                        counter += 1
                    c.execute(sqlQueryFinal.replace("{whereStmt}", whereStmt))
                    logger.info("Executed {} on SQLite3 database successfully".format(sqlQueryFinal.replace("{whereStmt}", whereStmt)))
                except Error as e:
                    logger.exception(e)
            else:
                # Execute the SQL query
                try:
                    c.execute(sqlQueryFinal)
                    logger.info("Executed {} on SQLite3 database successfully".format(sqlQueryFinal))
                except Error as e:
                    logger.exception(e)

            # Fetch all rows returned from SQL query
            try:
                current_fetched_rows = c.fetchall()
                row_count = len(current_fetched_rows)
                if row_count > 0:
                    all_fetched_rows = all_fetched_rows + current_fetched_rows
                logger.info("Fetched {} rows".format(row_count))
            except Error as e:
                logger.exception(e)
            finally:
                print("\nFinished processing {} on {} finding {} row(s).".format(self._metricName, dbfile, row_count), flush=True)
                self._progressIndex = 0
                conn.close()
            i = i + 1

        ################################################################
        # END FOR LOOP ON SQLITE CONNECTIONS
        ################################################################

        # Return all rows returned from SQL query
        return all_fetched_rows
