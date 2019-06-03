import sqlite3
from datetime import datetime
from sqlite3 import Error

import logzero
from logzero import logger


class Database(object):

    def __init__(self, dbfile):

        self._dbfile = dbfile


    def create_connection(self):
        """ Create a database connection to the SQLite database """
        try:
            conn = sqlite3.connect(self._dbfile)
            logger.info("Successfully connected to SQLite3 database at {}".format(self._dbfile))
            return conn
        except Error as e:
            logger.exception(e)

        return None


    def exec_fromfile(self, sqlfile):
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

        # Parse scan date from database file provided
        try:
            # Split to arrays
            dbFileNameSplit = self._dbfile.split("_")
            dbFileTimeSplit = dbFileNameSplit[2].split(".")
            # Format as proper datetime value
            inScanTime = datetime.strptime(dbFileTimeSplit[0].replace("-", " "), "%I %M %S %p")
            # Strip 1900-01-01 placemarker date and format to 24-hour
            scanTime = datetime.strftime(inScanTime, "%H:%M:%S")
            # Combine datetime for SQL query
            scanDateTime = dbFileNameSplit[1] + " " + scanTime
            # Make sure SQL filename was valid
            if scanDateTime is None:
                raise Exception("DNA Database filename should remain unchanged. Modifications detected.")
            logger.info("Parsed scan datetime from database filename: {}".format(scanDateTime))
        except Exception as e:
            logger.exception(e)

        # Execute the SQL query
        try:
            c.execute(sqlQuery.replace("{scanDateTime}", scanDateTime))
            logger.info("Executed {} on SQLite3 database successfully".format(sqlQuery.replace('{scanDateTime}', scanDateTime)))
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
