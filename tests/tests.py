import os
import sys

from colorama import Fore, Style, deinit, init

sys.path.append(os.path.abspath('..'))
from dnamic_analysis import Excel


class Tests(object):

    def __init__(self, excel_object, workbook, worksheet):
        self.excel_object = excel_object
        self.workbook = workbook
        self.worksheet = worksheet
        self.col = 0


    def domain_expired(self,max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Expired Domain Privileged IDs")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Oldest Non-Compliant Username: {}".format(max_sorted[0][0]))
        print(Fore.YELLOW + "Max Password Age: {} days ({:.1f} years)".format(max_sorted[0][2],max_sorted[0][2]/365))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Avg Password Age: {:.2f} / {} = {:.2f} days ({:.1f} years)".format(avg_sum,avg_len,avg_overall,avg_overall/365))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.2%}".format(percent_len,all_len,percent_overall))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        # Write bulk data to Excel workbook
        self.excel_object.write(self.worksheet, self.col, 0, 'Expired Domain Privileged IDs', 'header')
        row = 1
        for username,_,_ in max_sorted:
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        self.col += 1
        self.excel_object.save(self.workbook)


    def local_expired(self,max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall,sqlcount,unique_count):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Unique Expired Local Privileged IDs")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Oldest Non-Compliant Username: {}".format(max_sorted[0][0]))
        print(Fore.YELLOW + "Max Password Age: {} days ({:.1f} years)".format(max_sorted[0][3],max_sorted[0][3]/365))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Avg Password Age: {:.2f} / {} = {:.2f} days ({:.1f} years)".format(avg_sum,avg_len,avg_overall,avg_overall/365))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.2%}".format(percent_len,all_len,percent_overall))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Unique Local Privileged IDs: {}".format(sqlcount))
        print(Fore.YELLOW + "Total Unique Local Privileged ID Names: {}".format(unique_count))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        # Write bulk data to Excel workbook
        self.excel_object.write(self.worksheet, self.col, 0, 'Unique Expired Local Privileged IDs', 'header')
        row = 1
        used_usernames = []
        for username,_,_,_ in max_sorted:
            if username not in used_usernames:
                self.excel_object.write(self.worksheet, self.col, row, username)
                used_usernames.append(username)
                row += 1
        self.col += 1
        self.excel_object.save(self.workbook)


    def local_expired_machines(self,max_grouped,count_accounts,percent_accounts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Expired Local Admins Total w/ Machine Addresses" + Fore.YELLOW)

        self.excel_object.write(self.worksheet, self.col, 0, 'Expired Local Admins Total w/ Machine Addresses', 'header')
        count = 0
        row = 1
        for value in max_grouped.items():
            for key in value:
                if not isinstance(key, str):
                    if isinstance(key, list):
                        for machine in key:
                            print('Machine Address: {}'.format(machine))
                            self.excel_object.write(self.worksheet, self.col, row, machine)
                            count = len(key)
                            row += 1
                else:
                    if count:
                        print(Fore.YELLOW + Style.BRIGHT + "Total Machines for User: {}".format(count) + Style.NORMAL)
                    print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
                    print(Style.BRIGHT + 'Username: {}'.format(key) + Style.NORMAL)
                    self.excel_object.write(self.worksheet, self.col, row, key, 'subheader')
                    row += 1

        print(Fore.YELLOW + Style.BRIGHT + "Total Machines for User: {}".format(count) + Style.NORMAL)
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + Style.BRIGHT + "Total Local Accounts Non-Compliant: {}".format(len(max_grouped)))
        print(Fore.CYAN + Style.NORMAL + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        self.col += 1
        self.excel_object.save(self.workbook)


    def local_abandoned(self,abandoned_accounts, count_accounts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Local Abandoned / Leftover Accounts")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {} / {}".format(len(abandoned_accounts), count_accounts))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        # Write bulk data to Excel workbook
        self.excel_object.write(self.worksheet, self.col, 0, 'Local Abandoned / Leftover Accounts', 'header')
        row = 1
        for username,_,_,_ in abandoned_accounts:
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        self.col += 1
        self.excel_object.save(self.workbook)


    def domain_abandoned(self,abandoned_accounts, count_accounts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Domain Abandoned / Leftover Accounts")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {} / {}".format(len(abandoned_accounts), count_accounts))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        # Write bulk data to Excel workbook
        self.excel_object.write(self.worksheet, self.col, 0, 'Domain Abandoned / Leftover Accounts', 'header')
        row = 1
        for username,_,_,_ in abandoned_accounts:
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        self.col += 1
        self.excel_object.save(self.workbook)


    def multi_machine_accts(self,multi_machine_accts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Accounts with Multiple Machine Access")
        print(Fore.CYAN + "----------------------------------------------------")
        self.excel_object.write(self.worksheet, 5, 0, 'Accounts with Multiple Machine Access', 'header')
        if len(multi_machine_accts[0]) != 0:
            print(Fore.YELLOW + "> 95% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '> 95% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[0]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            self.col += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[0])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[1]) != 0:
            print(Fore.YELLOW + "90-95% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '90-95% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[1]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[1])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[2]) != 0:
            print(Fore.YELLOW + "80-90% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '80-90% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[2]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[2])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[3]) != 0:
            print(Fore.YELLOW + "70-80% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '70-80% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[3]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[3])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[4]) != 0:
            print(Fore.YELLOW + "60-70% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '60-70% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[4]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[4])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[5]) != 0:
            print(Fore.YELLOW + "50-60% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '50-60% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[5]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[5])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[6]) != 0:
            print(Fore.YELLOW + "40-50% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '40-50% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[6]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[6])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[7]) != 0:
            print(Fore.YELLOW + "30-40% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '30-40% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[7]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[7])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[8]) != 0:
            print(Fore.YELLOW + "20-30% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '20-30% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[8]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[8])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[9]) != 0:
            print(Fore.YELLOW + "10-20% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '10-20% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[9]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[9])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_accts[10]) != 0:
            print(Fore.YELLOW + "< 10% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '< 10% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_accts[10]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[10])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1

        print(Style.RESET_ALL)
        deinit()

        self.excel_object.save(self.workbook)


    def unique_domain_admins(self,sqlresults, svc_sqlresults, svc_domadm, svc_domadm2):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Unique Domain Admins")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {}".format(len(sqlresults)))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + Style.BRIGHT + "Total Potential Service Accounts: {}".format(len(svc_sqlresults)) + Style.NORMAL)
        self.excel_object.write(self.worksheet, self.col, 0, 'Unique Domain Admins', 'header')
        self.excel_object.write(self.worksheet, self.col, 1, 'Total Detected', 'subheader')
        row = 2
        for username in sqlresults:
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        self.col += 1
        self.excel_object.write(self.worksheet, self.col, 1, 'Potential Service Accounts', 'subheader')
        row = 2
        for username in svc_domadm:
            print("Username: {}".format(username))
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        for username2 in svc_domadm2:
            print("Username: {}".format(username2))
            self.excel_object.write(self.worksheet, self.col, row, username2)
            row += 1
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        self.col += 1
        self.excel_object.save(self.workbook)


    def unique_domain_expired(self,max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Unique Expired Domain Admins")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Oldest Non-Compliant Username: {}".format(max_sorted[0][0]))
        print(Fore.YELLOW + "Max Password Age: {} days ({:.1f} years)".format(max_sorted[0][3],max_sorted[0][3]/365))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Avg Password Age: {} / {} = {:.2f} days ({:.1f} years)".format(avg_sum,avg_len,avg_overall,avg_overall/365))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.2%}".format(percent_len,all_len,percent_overall))
        print(Fore.CYAN + "----------------------------------------------------")
        self.excel_object.write(self.worksheet, self.col, 0, 'Unique Expired Domain Admins', 'header')
        row = 1
        for username,_,_,_,_ in max_sorted:
            print(Fore.YELLOW + "Username: {}".format(username))
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        self.col += 1
        self.excel_object.save(self.workbook)


    def unique_domain_expired_null(self):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Unique Expired Domain Admins")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "No unique expired domain admins returned.")
        print(Fore.CYAN + "====================================================")
        print(Style.RESET_ALL)
        deinit()


    def personal_accts_running_svcs(self,sqlresults):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Personal Accounts Running Services")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Personal Accounts: {}".format(len(sqlresults)))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        # Write bulk data to Excel workbook
        self.excel_object.write(self.worksheet, self.col, 0, 'Personal Accounts Running Services', 'header')
        row = 1
        for username in sqlresults:
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        self.col += 1
        self.excel_object.save(self.workbook)


    def non_admin_with_local_admin(self,sqlresults):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Non-Admin Accounts w/ Local Admin to Systems")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Non-Admin Accounts: {}".format(len(sqlresults)))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        # Write bulk data to Excel workbook
        self.excel_object.write(self.worksheet, self.col, 0, 'Non-Admin Accounts w/ Local Admin to Systems', 'header')
        row = 1
        for username,_ in sqlresults:
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        self.col += 1
        self.excel_object.save(self.workbook)


    def unique_expired_svcs(self,max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
        if max_sorted == 'No services found.':
            print(Fore.CYAN + "====================================================")
            print(Fore.RED + "Unique Expired Services *(Check against manual report)*")
            print(Fore.CYAN + "----------------------------------------------------")
            print(Fore.YELLOW + max_sorted)
            print(Fore.CYAN + "====================================================")
        else:
            print(Fore.CYAN + "====================================================")
            print(Fore.RED + "Unique Expired Services *(Check against manual report)*")
            print(Fore.CYAN + "----------------------------------------------------")
            print(Fore.YELLOW + "Oldest Non-Compliant Service: {}".format(max_sorted[0][0]))
            print(Fore.YELLOW + "Max Password Age: {} days ({:.1f} years)".format(max_sorted[0][2],max_sorted[0][2]/365))
            print(Fore.CYAN + "----------------------------------------------------")
            print(Fore.YELLOW + "Total Avg Password Age: {} / {} = {:.2f} days ({:.1f} years)".format(avg_sum,avg_len,avg_overall,avg_overall/365))
            print(Fore.CYAN + "----------------------------------------------------")
            print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.2%}".format(percent_len,all_len,percent_overall))
            print(Fore.CYAN + "====================================================")

            # Write bulk data to Excel workbook
            self.excel_object.write(self.worksheet, self.col, 0, 'Unique Expired Services', 'header')
            row = 1
            for username,_,_ in max_sorted:
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            self.col += 1
            self.excel_object.save(self.workbook)

        print(Style.RESET_ALL)
        deinit()

        


    def clear_text_ids(self,sqlcount, sqlresults):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Clear Text IDs")
        print(Fore.CYAN + "----------------------------------------------------")
        self.excel_object.write(self.worksheet, self.col, 0, 'Clear Text IDs', 'header')
        row = 1
        if sqlcount > 0:
            for username,total,length in sqlresults:
                print(Fore.YELLOW + "Username: {}".format(username))
                print(Fore.YELLOW + "Total Found: {}".format(total))
                print(Fore.YELLOW + "Password Length: {}".format(length))
                print(Fore.CYAN + "----------------------------------------------------")
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1

            print(Fore.YELLOW + Style.BRIGHT + "Total Found Overall: {}".format(sqlcount))
        else:
            print(Fore.YELLOW + "No Clear Text IDs found.")
        print(Fore.CYAN + Style.NORMAL + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        self.col += 1
        self.excel_object.save(self.workbook)


    def apps_clear_text_passwords(self,sqlresults):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Applications with Clear Text Passwords")
        print(Fore.CYAN + "----------------------------------------------------")
        self.excel_object.write(self.worksheet, self.col, 0, 'Applications with Clear Text Passwords', 'header')
        row = 1
        if len(sqlresults) > 0:
            app_names = []
            for app_name,machine_address in sqlresults:
                print(Fore.YELLOW + "Application Name: {}".format(app_name))
                print(Fore.YELLOW + "Machine Address: {}".format(machine_address))
                print(Fore.CYAN + "----------------------------------------------------")
                app_names.append(app_name)
            print(Fore.YELLOW + Style.BRIGHT + "Total Unique Found Overall: {}".format(len(set(app_names))))
            for app_name in set(app_names):
                self.excel_object.write(self.worksheet, self.col, row, app_name)
                row += 1
        else:
            print(Fore.YELLOW + "No Applications with Clear Text Passwords found.")
        print(Fore.CYAN + Style.NORMAL + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        self.col += 1
        self.excel_object.save(self.workbook)


    def risky_spns(self,risky_spns, sqlcount):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Risky Expired Service Principal Names (SPN)")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Unique Expired over Total Overall: {} / {}".format(len(risky_spns), sqlcount))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        # Write bulk data to Excel workbook
        self.excel_object.write(self.worksheet, self.col, 0, 'Risky Expired Service Principal Names', 'header')
        row = 1
        for username,_ in risky_spns:
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        self.col += 1
        self.excel_object.save(self.workbook)


    def hashes_found_on_multiple(self,uniquecount, admin_hash_found, totalsrv, totalwks, totaladminsrv, totaladminwks):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Hashes Found on Multiple Machines")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Unique Accounts: {}".format(uniquecount))
        print(Fore.YELLOW + "Total Administrative Hashes Found: {}".format(len(admin_hash_found)))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total on Workstations: {}".format(totalwks))
        print(Fore.YELLOW + "Total on Servers: {}".format(totalsrv))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Admin Hashes on Workstations: {}".format(totaladminwks))
        print(Fore.YELLOW + "Total Admin Hashes on Servers: {}".format(totaladminsrv))
        print(Fore.CYAN + "----------------------------------------------------")
        self.excel_object.write(self.worksheet, self.col, 0, 'Hashes Found on Multiple Machines', 'header')
        row = 1
        for username in admin_hash_found:
            print(Fore.YELLOW + "Username: {}".format(username))
            self.excel_object.write(self.worksheet, self.col, row, username)
            row += 1
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()

        self.col += 1
        self.excel_object.save(self.workbook)


    def multi_machine_hashes(self,multi_machine_hashes):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Accounts with Multiple Machine Hashes")
        print(Fore.CYAN + "----------------------------------------------------")
        self.excel_object.write(self.worksheet, self.col, 0, 'Accounts with Multiple Machine Hashes', 'header')
        if len(multi_machine_hashes[0]) != 0:
            print(Fore.YELLOW + "> 95% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '> 95% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[0]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[0])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[1]) != 0:
            print(Fore.YELLOW + "90-95% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '90-95% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[1]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[1])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[2]) != 0:
            print(Fore.YELLOW + "80-90% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '80-90% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[2]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[2])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[3]) != 0:
            print(Fore.YELLOW + "70-80% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '70-80% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[3]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[3])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[4]) != 0:
            print(Fore.YELLOW + "60-70% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '60-70% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[4]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[4])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[5]) != 0:
            print(Fore.YELLOW + "50-60% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '50-60% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[5]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[5])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[6]) != 0:
            print(Fore.YELLOW + "40-50% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '40-50% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[6]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[6])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[7]) != 0:
            print(Fore.YELLOW + "30-40% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '30-40% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[7]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[7])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[8]) != 0:
            print(Fore.YELLOW + "20-30% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '20-30% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[8]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[8])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[9]) != 0:
            print(Fore.YELLOW + "10-20% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '10-20% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[9]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashehs[9])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1
        if len(multi_machine_hashes[10]) != 0:
            print(Fore.YELLOW + "< 10% Access")
            self.excel_object.write(self.worksheet, self.col, 1, '< 10% Access', 'subheader')
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            row = 2
            for username in multi_machine_hashes[10]:
                print("Username: {}".format(username))
                self.excel_object.write(self.worksheet, self.col, row, username)
                row += 1
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[10])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
            self.col += 1

        print(Style.RESET_ALL)
        deinit()

        self.excel_object.save(self.workbook)