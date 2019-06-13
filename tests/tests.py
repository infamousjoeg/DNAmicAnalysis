from colorama import init, deinit, Fore, Style


class Tests(object):

    def __init__(self):
        init()


    def domain_expired(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
        """ Simply printing to output values for convenience """

        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Expired Domain Privileged IDs")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Oldest Non-Compliant Username: {}".format(max_sorted[0][0]))
        print(Fore.YELLOW + "Max Password Age: {} days".format(max_sorted[0][2]))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Avg Password Age: {} / {} = {:.2f} days".format(avg_sum,avg_len,avg_overall))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.1%}".format(percent_len,all_len,percent_overall))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def local_expired(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
        """ Simply printing to output values for convenience """

        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Unique Expired Local Privileged IDs")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Oldest Non-Compliant Username: {}".format(max_sorted[0][0]))
        print(Fore.YELLOW + "Max Password Age: {} days".format(max_sorted[0][3]))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Avg Password Age: {} / {} = {:.2f} days".format(avg_sum,avg_len,avg_overall))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.1%}".format(percent_len,all_len,percent_overall))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def local_expired_machines(max_grouped,count_accounts):
        """ Simply printing to output values for convenience """

        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Expired Local Admins Total w/ Machine Names" + Fore.YELLOW)
        
        for value in max_grouped.items():
            for key in value:
                if not isinstance(key, str):
                    if isinstance(key, list):
                        for username in key:
                            print('Username: {}'.format(username))
                else:
                    print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
                    print('Machine Name: {}'.format(key))

        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Local Accounts Non-Compliant: {} / {}".format(len(max_grouped),count_accounts))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def local_abandoned(abandoned_accounts, count_accounts):
        """ Simply printing to output values for convenience """

        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Local Abandoned / Leftover Accounts")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {} / {}".format(abandoned_accounts, count_accounts))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def domain_abandoned(abandoned_accounts, count_accounts):
        """ Simply printing to output values for convenience """

        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Domain Abandoned / Leftover Accounts")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {} / {}".format(abandoned_accounts, count_accounts))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def multi_machine_accts(multi_machine_accts):
        """ Simply printing to output values for convenience """

        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Accounts with Multiple Machine Access")
        print(Fore.CYAN + "----------------------------------------------------")
        if len(multi_machine_accts[0]) != 0:
            print(Fore.YELLOW + "> 95% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[0]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[1]) != 0:
            print(Fore.YELLOW + "90-95% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[1]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[2]) != 0:
            print(Fore.YELLOW + "80-90% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[2]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[3]) != 0:
            print(Fore.YELLOW + "70-80% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[3]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[4]) != 0:
            print(Fore.YELLOW + "60-70% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[4]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[5]) != 0:
            print(Fore.YELLOW + "50-60% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[5]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[6]) != 0:
            print(Fore.YELLOW + "40-50% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[6]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[7]) != 0:
            print(Fore.YELLOW + "30-40% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[7]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[8]) != 0:
            print(Fore.YELLOW + "20-30% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[8]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[9]) != 0:
            print(Fore.YELLOW + "10-20% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[9]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[10]) != 0:
            print(Fore.YELLOW + "< 10% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[10]:
                print("Username: {}".format(username))
            print("TOTAL ACCOUNTS: {}".format(len(username)))
            print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def unique_domain_admins(sqlresults, svc_sqlresults):
        """ Simply printing to output values for convenience """

        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Unique Domain Admins")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {}".format(len(sqlresults)))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Potential Service Accounts: {}".format(len(svc_sqlresults)))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()