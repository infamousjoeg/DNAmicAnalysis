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