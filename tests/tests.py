from colorama import init, deinit, Fore, Style


class Tests(object):

    def __init__(self):
        init()


    def domain_expired(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
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


    def local_expired(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall,sqlcount,unique_count):
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


    def local_expired_machines(max_grouped,count_accounts,percent_accounts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Expired Local Admins Total w/ Machine Addresses" + Fore.YELLOW)

        for value in max_grouped.items():
            for key in value:
                if not isinstance(key, str):
                    if isinstance(key, list):
                        for machine in key:
                            print('Machine Address: {}'.format(machine))
                else:
                    print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
                    print(Style.BRIGHT + 'Username: {}'.format(key) + Style.NORMAL)

        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + Style.BRIGHT + "Total Local Accounts Non-Compliant: {}".format(len(max_grouped)))
        print(Fore.CYAN + Style.NORMAL + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def local_abandoned(abandoned_accounts, count_accounts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Local Abandoned / Leftover Accounts")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {} / {}".format(abandoned_accounts, count_accounts))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def domain_abandoned(abandoned_accounts, count_accounts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Domain Abandoned / Leftover Accounts")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {} / {}".format(abandoned_accounts, count_accounts))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def multi_machine_accts(multi_machine_accts):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Accounts with Multiple Machine Access")
        print(Fore.CYAN + "----------------------------------------------------")
        if len(multi_machine_accts[0]) != 0:
            print(Fore.YELLOW + "> 95% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[0]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[0])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[1]) != 0:
            print(Fore.YELLOW + "90-95% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[1]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[1])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[2]) != 0:
            print(Fore.YELLOW + "80-90% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[2]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[2])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[3]) != 0:
            print(Fore.YELLOW + "70-80% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[3]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[3])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[4]) != 0:
            print(Fore.YELLOW + "60-70% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[4]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[4])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[5]) != 0:
            print(Fore.YELLOW + "50-60% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[5]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[5])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[6]) != 0:
            print(Fore.YELLOW + "40-50% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[6]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[6])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[7]) != 0:
            print(Fore.YELLOW + "30-40% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[7]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[7])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[8]) != 0:
            print(Fore.YELLOW + "20-30% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[8]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[8])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[9]) != 0:
            print(Fore.YELLOW + "10-20% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[9]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[9])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_accts[10]) != 0:
            print(Fore.YELLOW + "< 10% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_accts[10]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_accts[10])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def unique_domain_admins(sqlresults, svc_sqlresults, svc_domadm, svc_domadm2):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Unique Domain Admins")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Detected: {}".format(len(sqlresults)))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + Style.BRIGHT + "Total Potential Service Accounts: {}".format(len(svc_sqlresults)) + Style.NORMAL)
        for username in svc_domadm:
            print("Username: {}".format(username))
        for username2 in svc_domadm2:
            print("Username: {}".format(username2))
        print(Fore.CYAN + "====================================================")
        print(Style.RESET_ALL)
        deinit()


    def unique_domain_expired(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall,domain_admins):
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
        for username in domain_admins:
            print(Fore.YELLOW + "Username: {}".format(username))
        print(Fore.CYAN + "====================================================")
        print(Style.RESET_ALL)
        deinit()


    def personal_accts_running_svcs(total):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Personal Accounts Running Services")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Personal Accounts: {}".format(total))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def non_admin_with_local_admin(total):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Non-Admin Accounts w/ Local Admin to Systems")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Non-Admin Accounts: {}".format(total))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def unique_expired_svcs(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
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

        print(Style.RESET_ALL)
        deinit()


    def clear_text_ids(sqlcount, sqlresults):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Clear Text IDs")
        print(Fore.CYAN + "----------------------------------------------------")
        if sqlcount > 0:
            for x in range(len(sqlresults)):
                print(Fore.YELLOW + "Username: {}".format(sqlresults[x][0]))
                print(Fore.YELLOW + "Total Found: {}".format(sqlresults[x][1]))
                print(Fore.YELLOW + "Password Length: {}".format(sqlresults[x][2]))
                print(Fore.CYAN + "----------------------------------------------------")
            print(Fore.YELLOW + Style.BRIGHT + "Total Found Overall: {}".format(sqlcount))
        else:
            print(Fore.YELLOW + "No Clear Text IDs found.")
        print(Fore.CYAN + Style.NORMAL + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def apps_clear_text_passwords(sqlresults):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Applications with Clear Text Passwords")
        print(Fore.CYAN + "----------------------------------------------------")
        if len(sqlresults) > 0:
            app_names = []
            for x in range(len(sqlresults)):
                print(Fore.YELLOW + "Application Name: {}".format(sqlresults[x][0]))
                print(Fore.YELLOW + "Machine Address: {}".format(sqlresults[x][1]))
                print(Fore.CYAN + "----------------------------------------------------")
                app_names.append(sqlresults[x][0])
            print(Fore.YELLOW + Style.BRIGHT + "Total Unique Found Overall: {}".format(len(set(app_names))))
        else:
            print(Fore.YELLOW + "No Applications with Clear Text Passwords found.")
        print(Fore.CYAN + Style.NORMAL + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def risky_spns(riskycount, sqlcount):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Risky Expired Service Principal Names (SPN)")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Unique Expired over Total Overall: {} / {}".format(riskycount, sqlcount))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def hashes_found_on_multiple(uniquecount, admin_hash_found, totalsrv, totalwks):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Hashes Found on Multiple Machines")
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total Unique Accounts: {}".format(uniquecount))
        print(Fore.YELLOW + "Total Administrative Hashes Found: {}".format(len(admin_hash_found)))
        print(Fore.CYAN + "----------------------------------------------------")
        print(Fore.YELLOW + "Total on Workstations: {}".format(totalwks))
        print(Fore.YELLOW + "Total on Servers: {}".format(totalsrv))
        print(Fore.CYAN + "----------------------------------------------------")
        for username in admin_hash_found:
            print(Fore.YELLOW + "Username: {}".format(username))
        print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()


    def multi_machine_hashes(multi_machine_hashes):
        print(Fore.CYAN + "====================================================")
        print(Fore.RED + "Accounts with Multiple Machine Hashes")
        print(Fore.CYAN + "----------------------------------------------------")
        if len(multi_machine_hashes[0]) != 0:
            print(Fore.YELLOW + "> 95% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[0]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[0])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[1]) != 0:
            print(Fore.YELLOW + "90-95% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[1]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[1])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[2]) != 0:
            print(Fore.YELLOW + "80-90% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[2]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[2])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[3]) != 0:
            print(Fore.YELLOW + "70-80% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[3]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[3])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[4]) != 0:
            print(Fore.YELLOW + "60-70% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[4]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[4])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[5]) != 0:
            print(Fore.YELLOW + "50-60% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[5]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[5])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[6]) != 0:
            print(Fore.YELLOW + "40-50% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[6]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[6])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[7]) != 0:
            print(Fore.YELLOW + "30-40% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[7]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[7])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[8]) != 0:
            print(Fore.YELLOW + "20-30% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[8]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[8])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[9]) != 0:
            print(Fore.YELLOW + "10-20% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[9]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashehs[9])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")
        if len(multi_machine_hashes[10]) != 0:
            print(Fore.YELLOW + "< 10% Access")
            print(Fore.CYAN + "----------------------------------------------------" + Fore.YELLOW)
            for username in multi_machine_hashes[10]:
                print("Username: {}".format(username))
            print(Style.BRIGHT + "TOTAL ACCOUNTS: {}".format(len(multi_machine_hashes[10])) + Style.NORMAL)
            print(Fore.CYAN + "====================================================")

        print(Style.RESET_ALL)
        deinit()