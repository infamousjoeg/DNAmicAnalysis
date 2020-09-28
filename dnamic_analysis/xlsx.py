import os
import time

import xlsxwriter


class Xlsx(object):

    def __init__(self, domain):

        # Get datetime stamp for save filename
        self._timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

        # Declare domain name of scan
        self._domain = domain

        # Parse filename
        self._filename = 'reports/DNAmicAnalysis_' + self._domain + '_' + self._timestamp + '.xlsx'
    

    # Convert list of tuples to tuple of lists for output
    # Returns a tuple of lists for easy write of row data
    def convert_results(self, sqlresults):
        # Create a list for lists
        lists = []
        # If there are results returned in sqlresults...
        if sqlresults:
            # Iterate through each row of sqlresults
            for row in sqlresults:
                # Add each row (tuple) to my list of lists
                # while converting the tuple to a list
                lists.append(list(row))
            # Add the list of lists into a tuple
            bigTuple = tuple(lists)
            # Return our tuple of lists
            return bigTuple


    # Creates the workbook class and inits cell formats for later use
    # Returns the workbook object
    def create_workbook(self):
        # Init Excel workbook class
        try:
            # Init workbook class with filename/path
            workbook = xlsxwriter.Workbook(self._filename)
            # Set properties to the workbook
            workbook.set_properties({
                'title':    'DNAmic Analysis Report',
                'subject':  'for {}'.format(self._domain),
                'author':   'DNAmic Analysis Application',
                'company':  'CyberArk Software, Ltd.',
                'comments': 'Automated analysis of DNA results'
            })
            # Set the top row style (row1)
            self._row1_format = workbook.add_format({
                'font_name':    'Calibri',
                'font_size':    10,
                'text_wrap':    True
            })
            # Set the header row style
            self._header_format = workbook.add_format({
                'font_name':    'Calibri',
                'font_size':    14,
                'bold':         True
            })
            # Set the subheader row style
            self._subheader_format = workbook.add_format({
                'font_name':    'Calibri',
                'font_size':    14,
                'bold':         True,
                'font_color':   'red'
            })
            # Set the normal style (default)
            self._normal_format = workbook.add_format({
                'font_name':    'Calibri',
                'font_size':    14,
                'num_format':   '#,###'
            })
            return workbook
        except:
            return False
    

    # Creates the worksheet in the workbook object
    # Returns the worksheet object added
    def add_worksheet (self, workbook, name):
        try:
            # Add a worksheet to workbook with the worksheet tab title matching name
            worksheet = workbook.add_worksheet(name)
            worksheet.set_column('A:Z', 40)
            if name == 'Expired Local Admins Total w Ma':
                worksheet.autofilter('A1')
                return worksheet
            elif name == 'Clear Text IDs' or name == 'Applications w Clear Text Passw':
                worksheet.autofilter('A2:C2')
                return worksheet
            elif name == 'Unique Expired Local Privileged' or name == 'Unique Expired Service Accounts':
                worksheet.autofilter('A3:D3')
                return worksheet
            elif name == 'Local Abandoned Accounts' or name == 'Domain Abandoned Accounts':
                worksheet.autofilter('A3:E3')
                return worksheet
            elif name == 'Unique Domain Admins':
                worksheet.autofilter('A4:F4')
                return worksheet
            elif name == 'Accounts w Multiple Machine Acc' or name == 'Account Hashes that Expose Mult':
                worksheet.autofilter('A3:Z3')
                return worksheet
            else:
                worksheet.autofilter('A3:C3')
                return worksheet
        except Exception as e:
            raise Exception(e)


    # Writes `data` in the format of `type` to a cell in the worksheet specified
    # Returns true if successful and false if failure
    def write(self, worksheet, col, row, data, cell_format=None, rowcol=None):

        try:
            if cell_format == 'row1':
                cell_format = self._row1_format
            elif cell_format == 'header':
                cell_format = self._header_format
            elif cell_format == 'subheader':
                cell_format = self._subheader_format
            elif cell_format == 'normal' or cell_format is None:
                cell_format = self._normal_format
            else:
                raise Exception('Unknown cell format.')

            if rowcol is None:
                worksheet.write(row, col, data, cell_format)
            elif rowcol == 'row':
                worksheet.write_row(row, col, data, cell_format)
            elif rowcol == 'col':
                worksheet.write_column(row, col, data, cell_format)
            else:
                raise Exception ('Unknown rowcol value.')
            return True
        except Exception as e:
            raise Exception(e)


    def write_merge(self, worksheet, row1, col1, row2, col2, data, cell_format=None):

        try:
            if cell_format == 'row1':
                cell_format = self._row1_format
            elif cell_format == 'header':
                cell_format = self._header_format
            elif cell_format == 'subheader':
                cell_format = self._subheader_format
            elif cell_format == 'normal' or cell_format is None:
                cell_format = self._normal_format
            else:
                raise Exception('Unknown cell format.')
            
            worksheet.merge_range(row1, col1, row2, col2, data, cell_format)
            return True
        except:
            return False


    def autofilter(self, worksheet, row1, col1, row2, col2):

        try:
            worksheet.autofilter(row1, col1, row2, col2)
            return True
        except:
            return False


    # Closes the workbook to further edits
    def close_workbook(self, workbook):

        while True:
            try:
                workbook.close()
            except xlsxwriter.exceptions.FileCreateError as e:
                decision = input("Exception caught in workbook.close(): {}\n"
                                 "Please close the file if it is open in Excel.\n"
                                 "Try to write file again? [Y/n]: ".format(e))
                if decision != 'n':
                    continue
            
            break
