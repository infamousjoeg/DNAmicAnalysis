#!/usr/bin/env python3

from dnamic_analysis import Xlsx

dummy_data = [('Mike', '2017-11-21 17:26:40', 3, 546), ('Robert', '2017-12-22 21:00:31', 3, 514), ('h_admin', '2018-02-27 21:43:41', 3, 447), ('Administrator', '2018-04-18 18:50:47', 3, 398), ('svc_sql', '2018-04-27 17:55:07', 3, 389), ('rogueadmin', '2018-06-26 16:32:21', 3, 329), ('Vendor_1', '2018-09-10 19:16:46', 3, 253), ('svc_mgmt', '2018-09-12 04:27:22', 3, 251)]

# Init Xlsx object
xlsx = Xlsx('cyberarkdemo.com')
# Create workbook
workbook = xlsx.create_workbook()
# Add three test worksheets
worksheet1 = xlsx.add_worksheet(workbook, 'Format Tests')
# Write string
xlsx.write(worksheet1, 0, 0, 'Row1 Test String', 'row1')
xlsx.write_merge(worksheet1, 1, 0, 1, 1, 'Header Test String with Cell Merge', 'header')
xlsx.write(worksheet1, 2, 0, 'Username', 'subheader')
xlsx.write(worksheet1, 2, 1, 'Last Password Change', 'subheader')
xlsx.write(worksheet1, 2, 2, 'Number of Machines', 'subheader')
xlsx.write(worksheet1, 2, 3, 'Something', 'subheader')
# Write row
row_count = 3
for row in dummy_data:
    xlsx.write(worksheet1, row_count, 0, row, None, 'row')
    row_count += 1
# Set autofilter
xlsx.autofilter(worksheet1, 2, 0, 2, 3)
# Close and save workbook
xlsx.close_workbook(workbook)