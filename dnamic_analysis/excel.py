import os
import time

import xlwt


class Excel(object):

    def __init__(self, domain):

        # Define font for Row 1 data
        row1_font = xlwt.Font()
        row1_font.name = 'Calibri'
        row1_font.height = 200

        # Define font for column headers
        header_font = xlwt.Font()
        header_font.name = 'Calibri'
        header_font.bold = True
        header_font.height = 280

        # Define font for column sub-headers
        subheader_font = xlwt.Font()
        subheader_font.name = 'Calibri'
        subheader_font.bold = True
        subheader_font.colour_index = xlwt.Style.colour_map['red']
        subheader_font.height = 280

        # Define font for column values
        normal_font = xlwt.Font()
        normal_font.name = 'Calibri'
        normal_font.height = 280

        # Define styles for column headers & values
        row1_style  = xlwt.XFStyle()
        row1_style.font = row1_font
        row1_style.alignment.wrap = 1
        header_style = xlwt.XFStyle()
        header_style.font = header_font
        subheader_style = xlwt.XFStyle()
        subheader_style.font = subheader_font
        normal_style = xlwt.XFStyle()
        normal_style.font = normal_font
        normal_style.num_format_str = "#,###.##"

        # Declare styles to class
        self._row1_style = row1_style
        self._header_style = header_style
        self._subheader_style = subheader_style
        self._normal_style = normal_style

        # Get datetime stamp for save filename
        self._timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

        # Declare domain name of scan
        self._domain = domain

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

        worksheet.col(col).width = 640 * 20

        try:
            if style == 'header':
                worksheet.write(row, col, data, self._header_style)
            elif style == 'subheader':
                worksheet.write(row, col, data, self._subheader_style)
            elif style == 'row1':
                worksheet.write(row, col, data, self._row1_style)
            else:
                worksheet.write(row, col, data, self._normal_style)
            return True
        except:
            return False


    # Saves the workbook to the reports/ directory
    def save(self, workbook):

        try:
            if not os.path.exists('reports'):
                os.mkdir('reports')
            workbook.save('DNAmicAnalysis_' + self._domain + '_' + self._timestamp + '.xls')
            return True
        except:
            return False
