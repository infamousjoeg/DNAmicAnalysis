from colorama import init, deinit, Fore, Style

def domain_print_sorted(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall):
    """ Simply printing to output values for convenience """
    # Initialize colorama in case Windows OS
    init()

    print(Fore.CYAN + "====================================================")
    print(Fore.RED + "Expired Domain Privileged IDs")
    print(Fore.CYAN + "----------------------------------------------------")
    print(Fore.YELLOW + "Username: {}".format(max_sorted[0][0]))
    print(Fore.YELLOW + "Max Password Age: {} days".format(max_sorted[0][2]))
    print(Fore.CYAN + "----------------------------------------------------")
    print(Fore.YELLOW + "Total Avg Password Age: {} / {} = {:.2f} days".format(avg_sum,avg_len,avg_overall))
    print(Fore.CYAN + "----------------------------------------------------")
    print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.1%}".format(percent_len,all_len,percent_overall))
    print(Fore.CYAN + "====================================================")

    print(Style.RESET_ALL)
    deinit()

def local_print_sorted(max_sorted,avg_sum,avg_len,avg_overall,percent_len,all_len,percent_overall,count_accounts):
    """ Simply printing to output values for convenience """
    # Initialize colorama in case Windows OS
    init()

    print(Fore.CYAN + "====================================================")
    print(Fore.RED + "Unique Expired Local Privileged IDs")
    print(Fore.CYAN + "----------------------------------------------------")
    print(Fore.YELLOW + "Username: {}".format(max_sorted[0][0]))
    print(Fore.YELLOW + "Max Password Age: {} days".format(max_sorted[0][3]))
    print(Fore.CYAN + "----------------------------------------------------")
    print(Fore.YELLOW + "Total Avg Password Age: {} / {} = {:.2f} days".format(avg_sum,avg_len,avg_overall))
    print(Fore.CYAN + "----------------------------------------------------")
    print(Fore.YELLOW + "Total Percent Non-Compliant: {} / {} = {:.1%}".format(percent_len,all_len,percent_overall))
    print(Fore.CYAN + "----------------------------------------------------")
    print(Fore.YELLOW + "Total Local Accounts Non-Compliant: {}".format(count_accounts))
    print(Fore.CYAN + "====================================================")

    print(Style.RESET_ALL)
    deinit()