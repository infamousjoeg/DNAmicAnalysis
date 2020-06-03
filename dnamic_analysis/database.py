import ntpath
import sqlite3
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

from logzero import logger


class Database(object):

    def __init__(self, dbfile, disabled, scan_datetime):

        self._dbfile = Path(dbfile)
        self._disabledSqlQuery = ""
        if disabled is False:
            self._disabledSqlQuery = "AND OSAccounts.Enabled = 1"
        
        # Parse scan date & time if no override detected
        if not scan_datetime['override']:
            # Split to arrays
            dbFileName = ntpath.basename(self._dbfile)
            dbFileNameSplit = dbFileName.split("_")
            dnaIndex = dbFileNameSplit.index("DNA")
            dIndex = dnaIndex + 1
            tIndex = dIndex + 1
            dbFileTimeSplit = dbFileNameSplit[tIndex].split(".")
            # Format as proper datetime value
            inScanTime = datetime.strptime(dbFileTimeSplit[0].replace("-", " "), "%I %M %S %p")
            # Strip 1900-01-01 placemarker date and format to 24-hour
            scanTime = datetime.strftime(inScanTime, "%H:%M:%S")
            # Combine datetime for SQL query
            self._scanDateTime = dbFileNameSplit[dIndex] + " " + scanTime
            logger.info("Parsed scan datetime from database filename: {}".format(self._scanDateTime))
        else:
            self._scanDateTime = scan_datetime['manual_scan_datetime']
            logger.info("Manual override detected, received scan datetime as: {}".format(self._scanDateTime))


    def create_connection(self):
        """ Create a database connection to the SQLite database """
        try:
            conn = sqlite3.connect(self._dbfile)
            logger.info("Successfully connected to SQLite3 database at {}".format(self._dbfile))
            return conn
        except Error as e:
            logger.exception(e)

        return None


    def exec_fromfile(self, sqlfile, regex_flag=False, regex_array=None):
        """ Executes the query from a SQL file and returns all rows """
        # Open and read the SQL file as a single buffer
        try:
            with open(sqlfile, 'r') as file:
                sqlQuery = file.read()
            logger.info("Opened & read {}".format(sqlfile))
        except Exception as e:
            logger.exception(e)

        # Create database connection
        try:
            conn = self.create_connection()

            # Create a cursor for the database connection
            c = conn.cursor()
            logger.info("Created database connection cursor")
        except Error as e:
            logger.exception(e)

        try:
            # Make replacement in SQL query
            sqlQueryDT = sqlQuery.replace("{scanDateTime}", self._scanDateTime)
            # Replace disabled section of SQL query
            sqlQueryFinal = sqlQueryDT.replace("{disabled}", self._disabledSqlQuery)
        except Exception as e:
            logger.exception(e)

        # Execute the SQL query
        if regex_flag:
            try:
                whereStmt = ""
                counter = 0
                for regex in regex_array:
                    if counter == 0:
                        whereStmt += "Accounts.Name LIKE '%{}%' ".format(regex.replace('^','%'))
                    else:
                        whereStmt += "OR Accounts.Name LIKE '%{}%' ".format(regex.replace('^','%'))
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
            fetched_rows = c.fetchall()
            row_count = len(fetched_rows)
            logger.info("Fetched {} rows".format(row_count))
        except Error as e:
            logger.exception(e)
        finally:
            conn.close()

        # Return all rows returned from SQL query
        return fetched_rows
