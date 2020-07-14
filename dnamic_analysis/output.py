import os
import sys

from dnamic_analysis import Excel


class Output(object):

    def __init__(self, excel_object, workbook, worksheet):
        self._excel_object = excel_object
        self._workbook = workbook
        self._worksheet = worksheet
        self._col = 0


    ###################################
    ## Expired Domain Privileged IDs ##
    ###################################
    def domain_expired(
        self,
        max_sorted,
        avg_sum,
        avg_len,
        avg_overall,
        percent_len,
        all_len,
        percent_overall,
        password_age
    ):
        if max_sorted is not False:
            # Write bulk data to Excel workbook
            data = 'Oldest Non-Compliant Username: {}\n' \
                    'Max Password Age: {} days ({:.1f} years)\n' \
                    'Total Avg Password Age: {:.2f} / {} = {:.2f} days ({:.1f} years)\n' \
                    'Total Percent Non-Compliant: {} / {} = {:.2%}'.format(max_sorted[0][0],max_sorted[0][2],max_sorted[0][2]/365,
                                                                        avg_sum,avg_len,avg_overall,avg_overall/365,percent_len,all_len,percent_overall)
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Expired Domain Privileged IDs', 'header')
            self._excel_object.write(self._worksheet, self._col, 2, 'Usernames', 'subheader')
            self._excel_object.write(self._worksheet, self._col+1, 2, 'Avg Password Age', 'subheader')
            row = 3
            for username,_,_ in max_sorted:
                self._excel_object.write(self._worksheet, self._col, row, username)
                self._excel_object.write(self._worksheet, self._col+1, row, password_age[username])
                row += 1
            self._col += 2
            self._excel_object.save(self._workbook)


    #########################################
    ## Unique Expired Local Privileged IDs ##
    #########################################
    def local_expired(
        self,
        max_sorted,
        avg_sum,
        avg_len,
        avg_overall,
        percent_len,
        all_len,
        percent_overall,
        sqlcount,
        unique_count,
        password_age
    ):
        if max_sorted is not False and sqlcount != 0 and unique_count != 0:
            # Write bulk data to Excel workbook
            data = 'Oldest Non-Compliant Username: {}\n' \
                    'Max Password Age: {} days ({:.1f} years)\n' \
                    'Total Avg Password Age: {:.2f} / {} = {:.2f} days ({:.1f} years)\n' \
                    'Total Percent Non-Compliant: {} / {} = {:.2%}\n' \
                    'Total Unique Local Privileged IDs: {}\n' \
                    'Total Unique Local Privileged ID Names: {}'.format(max_sorted[0][0],max_sorted[0][3],max_sorted[0][3]/365,
                                                                    avg_sum,avg_len,avg_overall,avg_overall/365,percent_len,
                                                                    all_len,percent_overall,sqlcount,unique_count)
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Unique Expired Local Privileged IDs', 'header')
            self._excel_object.write(self._worksheet, self._col, 2, 'Usernames', 'subheader')
            self._excel_object.write(self._worksheet, self._col+1, 2, 'Avg Password Age', 'subheader')
            row = 3
            used_usernames = []
            for username,_,_,_ in max_sorted:
                if username not in used_usernames:
                    self._excel_object.write(self._worksheet, self._col, row, username)
                    self._excel_object.write(self._worksheet, self._col+1, row, password_age[username])
                    used_usernames.append(username)
                    row += 1
            self._col += 2
            self._excel_object.save(self._workbook)


    #####################################################
    ## Expired Local Admins Total w/ Machine Addresses ##
    #####################################################
    def local_expired_machines(self,max_grouped,count_accounts,percent_accounts):
        self._excel_object.write(self._worksheet, self._col, 1, 'Expired Local Admins Total w/ Machine Addresses', 'header')
        count = 0
        row = 2
        for value in max_grouped.items():
            for key in value:
                if not isinstance(key, str):
                    if isinstance(key, list):
                        for machine in key:
                            self._excel_object.write(self._worksheet, self._col, row, machine)
                            count = len(key)
                            row += 1
                else:
                    self._excel_object.write(self._worksheet, self._col, row, key, 'subheader')
                    row += 1

        self._col += 1
        self._excel_object.save(self._workbook)

    ##############################
    ## Local Abandoned Accounts ##
    ##############################
    def local_abandoned(self,abandoned_accounts, count_accounts):
        if abandoned_accounts is not False and count_accounts != 0:
            # Write bulk data to Excel workbook
            data = 'Total Abandoned / Total Overall: {} / {}'.format(len(abandoned_accounts), count_accounts)
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Local Abandoned Accounts', 'header')
            row = 2
            for username,_,_,_ in abandoned_accounts:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)

    ###############################
    ## Domain Abandoned Accounts ##
    ###############################
    def domain_abandoned(self,abandoned_accounts, count_accounts):
        if abandoned_accounts is not False:
            # Write bulk data to Excel workbook
            data = 'Total Abandoned / Total Overall: {} / {}'.format(len(abandoned_accounts), count_accounts)
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Domain Abandoned Accounts', 'header')
            row = 2
            for username,_,_,_ in abandoned_accounts:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    #########################################################
    ## Accounts w/ Multiple Machine Exposure - By %age Tiers ##
    #########################################################
    def multi_machine_accts(self,multi_machine_accts):
        if multi_machine_accts is not False:
            tiers = ['> 95% Exposure','90-95% Exposure','80-90% Exposure','70-80% Exposure','60-70% Exposure',
                '50-60% Exposure','40-50% Exposure','30-40% Exposure','20-30% Exposure','10-20% Exposure',
                '< 10% Exposure']

            self._excel_object.write(self._worksheet, 5, 1, 'Accounts with Multiple Machine Exposure', 'header')

            for i in range(len(multi_machine_accts)):
                if len(multi_machine_accts[i]) != 0:
                    self._excel_object.write(self._worksheet, self._col, 2, tiers[i], 'subheader')
                    row = 3
                    for username in multi_machine_accts[i]:
                        self._excel_object.write(self._worksheet, self._col, row, username)
                        row += 1
                    self._col += 1

            self._excel_object.save(self._workbook)


    ##########################
    ## Unique Domain Admins ##
    ##########################
    def unique_domain_admins(self,sqlresults, svc_sqlresults, svc_domadm, svc_domadm2):
        if sqlresults is not False:
            data = 'Total Detected: {}\n' \
                    'Total Potential Service Accounts: {}'.format(len(sqlresults),len(svc_sqlresults))
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Unique Domain Admins', 'header')
            self._excel_object.write(self._worksheet, self._col, 2, 'Total Detected', 'subheader')
            row = 3
            for username in sqlresults:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.write(self._worksheet, self._col, 2, 'Potential Service Accounts', 'subheader')
            row = 3
            for username in svc_domadm:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            for username2 in svc_domadm2:
                self._excel_object.write(self._worksheet, self._col, row, username2)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    ##########################################
    ## Expired Domain Privileged IDs ##
    ##########################################
    def unique_domain_expired(self,max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
        if max_sorted is not False:
            data = 'Oldest Non-Compliant Username: {}\n' \
                    'Max Password Age: {} days ({:.1f} years)\n' \
                    'Total Avg Password Age: {} / {} = {:.2f} days ({:.1f} years)\n' \
                    'Total Percent Non-Compliant: {} / {} = {:.2%}'.format(max_sorted[0][0],max_sorted[0][3],max_sorted[0][3]/365,
                                                                        avg_sum,avg_len,avg_overall,avg_overall/365,percent_len,
                                                                        all_len,percent_overall)
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Expired Domain Admins', 'header')
            row = 2
            for username,_,_,_,_ in max_sorted:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    ########################################
    ## Personal Accounts Running Services ##
    ########################################
    def personal_accts_running_svcs(self,sqlresults):
        if sqlresults is not False:
            # Write bulk data to Excel workbook
            data = 'Total Personal Accounts: {}'.format(len(sqlresults))
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Personal Accounts Running Services', 'header')
            row = 2
            for username in sqlresults:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    #######################################################
    ## Non-adm Accounts w/ Local Admin Rights on Systems ##
    #######################################################
    def non_admin_with_local_admin(self,sqlresults):
        if sqlresults is not False:
            # Write bulk data to Excel workbook
            data = 'Total Non-Admin Accounts: {}'.format(len(sqlresults))
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Non-Admin Accounts w/ Local Admin to Systems', 'header')
            row = 2
            for username,_,_ in sqlresults:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    #####################################
    ## Unique Expired Service Accounts ##
    #####################################
    def unique_expired_svcs(self,max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
            if max_sorted is not False:
                # Write bulk data to Excel workbook
                data = 'Oldest Non-Compliant Service: {}\n' \
                        'Max Password Age: {} days ({:.1f} years)\n' \
                        'Total Avg Password Age: {} / {} = {:.2f} days ({:.1f} years)\n' \
                        'Total Percent Non-Compliant: {} / {} = {:.2%}'.format(max_sorted[0][0],max_sorted[0][2],max_sorted[0][2]/365,
                                                                            avg_sum,avg_len,avg_overall,avg_overall/365,percent_len,
                                                                            all_len,percent_overall)
                self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
                self._excel_object.write(self._worksheet, self._col, 1, 'Unique Expired Service Accounts', 'header')
                self._excel_object.write(self._worksheet, self._col, 2, 'Username', 'subheader')
                row = 3
                for username,_,_,_ in max_sorted:
                    self._excel_object.write(self._worksheet, self._col, row, username)
                    row += 1
                self._col += 1
                self._excel_object.write(self._worksheet, self._col, 2, 'Address', 'subheader')
                row = 3
                for _,_,_,address in max_sorted:
                    self._excel_object.write(self._worksheet, self._col, row, address)
                    row += 1
                self._col += 1
                self._excel_object.save(self._workbook)


    ####################
    ## Clear Text IDs ##
    ####################
    def clear_text_ids(self,sqlcount, sqlresults):
        if sqlcount is not False:
            self._excel_object.write(self._worksheet, self._col, 1, 'Clear Text IDs', 'header')
            row = 2
            if sqlcount > 0:
                for username,total,length in sqlresults:
                    self._excel_object.write(self._worksheet, self._col, row, username)
                    row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    ##########################################
    ## Applications w/ Clear Text Passwords ##
    ##########################################
    def apps_clear_text_passwords(self,sqlresults):
        if sqlresults is not False:
            self._excel_object.write(self._worksheet, self._col, 1, 'Applications with Clear Text Passwords', 'header')
            row = 2
            if len(sqlresults) > 0:
                app_names = []
                for app_name,username in sqlresults:
                    app_names.append(app_name)
                for app_name in set(app_names):
                    self._excel_object.write(self._worksheet, self._col, row, app_name)
                    row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    #################################################
    ## Risky Expired Service Principal Names (SPN) ##
    #################################################
    def risky_spns(self,risky_spns, sqlcount):
        if risky_spns is not False:
            # Write bulk data to Excel workbook
            data = 'Total Unique Expired over Total Overall: {} / {}'.format(len(risky_spns), sqlcount)
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Risky Expired Service Principal Names', 'header')
            row = 2
            for username,_ in risky_spns:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    #######################################
    ## Hashes Found on Multiple Machines ##
    #######################################
    def hashes_found_on_multiple(self,uniquecount, admin_hash_found, totalsrv, totalwks, totaladminsrv, totaladminwks):
        if totalsrv is not False:
            data = 'Total Unique Accounts: {}\n' \
                    'Total Administrative Hashes Found: {}\n' \
                    'Total on Workstations: {}\n' \
                    'Total on Servers: {}\n' \
                    'Total Admin Hashes on Workstations: {}\n' \
                    'Total Admin Hashes on Servers: {}'.format(uniquecount,len(admin_hash_found),totalwks,totalsrv,totaladminwks,totaladminsrv)
            self._excel_object.write(self._worksheet, self._col, 0, data, 'row1')
            self._excel_object.write(self._worksheet, self._col, 1, 'Hashes Found on Multiple Machines', 'header')
            row = 2
            for username in admin_hash_found:
                self._excel_object.write(self._worksheet, self._col, row, username)
                row += 1
            self._col += 1
            self._excel_object.save(self._workbook)


    ##################################################################
    ## Account Hashes that Expose Multiple Machines - By %age Tiers ##
    ##################################################################
    def multi_machine_hashes(self,multi_machine_hashes):
        if multi_machine_hashes is not False:
            tiers = ['> 95% Exposure','90-95% Exposure','80-90% Exposure','70-80% Exposure','60-70% Exposure',
                    '50-60% Exposure','40-50% Exposure','30-40% Exposure','20-30% Exposure','10-20% Exposure',
                    '< 10% Exposure']

            self._excel_object.write(self._worksheet, self._col, 1, 'Account Hashes that Expose Multiple Machines', 'header')

            for i in range(len(multi_machine_hashes)):
                    if len(multi_machine_hashes[i]) != 0:
                        self._excel_object.write(self._worksheet, self._col, 2, tiers[i], 'subheader')
                        row = 3
                        for username in multi_machine_hashes[i]:
                            self._excel_object.write(self._worksheet, self._col, row, username)
                            row += 1
                        self._col += 1

            self._excel_object.save(self._workbook)