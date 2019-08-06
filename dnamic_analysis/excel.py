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


    def create(self):
        # Init Excel workbook class
        workbook = xlwt.Workbook()
        return workbook

    def add(self, workbook, name):

        try:
            worksheet = workbook.add_sheet(name)
            return worksheet
        except:
            return False


    def write(self, worksheet, col, row, data, style='normal'):

        try:
            if style == 'header':
                worksheet.write(row, col, data, self.header_style)
            else:
                worksheet.write(row, col, data, self.normal_style)
            return True
        except:
            return False


    def save(self, workbook, save_path):

        try:
            workbook.save(save_path)
            return True
        except:
            return False