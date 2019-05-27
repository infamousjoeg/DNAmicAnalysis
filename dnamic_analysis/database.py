import sqlite3
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
        with open(sqlfile, 'r') as file:
            sqlQuery = file.read()
            logger.info("Opened & read {}".format(sqlfile))
        
        # Create database connection
        conn = self.create_connection()

        # Create a cursor for the database connection
        c = conn.cursor()
        logger.info("Created database connection cursor")

        # Parse scan date from database file provided
        dbFileNameSplit = self._dbfile.split("_")
        scanDate = dbFileNameSplit[1]
        logger.info("Parsed scan date from database filename: {}".format(scanDate))

        # Execute the SQL query
        try:
            c.execute(sqlQuery.replace('{scanDate}', scanDate))
            logger.info("Executed {} on SQLite3 database successfully".format(sqlQuery.replace('{scanDate}', scanDate)))
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