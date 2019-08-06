import os
from datetime import datetime

import xlwt


class Excel(object):

    def __init__(self):

        # Define font for column headers
        header_font = xlwt.Font()
        header_font.name = 'Calibri'
        header_font.bold = True

        # Define font for column values
        normal_font = xlwt.Font()
        normal_font.name = 'Calibri'

        # Define styles for column headers & values
        header_style = xlwt.XFStyle()
        header_style.font = header_font
        normal_style = xlwt.XFStyle()
        normal_style.font = normal_font
        normal_style.num_format_str = "#,###.##"

        # Declare styles to class
        self.header_style = header_style
        self.normal_style = normal_style

        # Get datetime stamp for save filename
        self.timestamp = datetime.now().isoformat(timespec='seconds')

    # Creates the workbook class
    def create(self):
        # Init Excel workbook class
        workbook = xlwt.Workbook()
        return workbook


    # Adds a worksheet to the workbook (tab)
    def add(self, workbook, name):

        try:
            worksheet = workbook.add_sheet(name)
            return worksheet
        except:
            return False


    # Writes a row to the worksheet specified
    def write(self, worksheet, col, row, data, style='normal'):

        try:
            if style == 'header':
                worksheet.write(row, col, data, self.header_style)
            else:
                worksheet.write(row, col, data, self.normal_style)
            return True
        except:
            return False


    # Saves the workbook to the reports/ directory
    def save(self, workbook):

        try:
            if not os.path.exists('reports'):
                os.mkdir('reports')
            workbook.save('DNAmicAnalysis_' + self.timestamp + '.xls')
            return True
        except:
            return False
