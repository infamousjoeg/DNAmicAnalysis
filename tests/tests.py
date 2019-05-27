from colorama import init, deinit, Fore, Style

def print_sorted(max_domain_sorted,avg_domain_overall,percent_domain_overall,max_local_sorted,avg_local_overall,percent_local_overall,count_local_accounts):
    """ Simply printing to output values for convenience """
    # Initialize colorama in case Windows OS
    init()

    print(Fore.CYAN + "==========================")
    print(Fore.RED + "Expired Domain Privileged IDs - Max Password Age")
    print(Fore.CYAN + "--------------------------")
    print(Fore.YELLOW + "Username: {}".format(max_domain_sorted[0][0]))
    print(Fore.YELLOW + "Max Password Age: {} days".format(max_domain_sorted[0][2]))
    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Expired Domain Privileged IDs - Average Password Age")
    print(Fore.CYAN + "--------------------------")
    print(Fore.YELLOW + "Total Avg Password Age: {} days".format(avg_domain_overall))
    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Expired Domain Privileged IDs - Non-Compliant Percentage")
    print(Fore.CYAN + "--------------------------")
    print(Fore.YELLOW + "Total Percent Non-Compliant: {:.1%}".format(percent_domain_overall))
    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Unique Expired Local Privileged IDs - Max Password Age")
    print(Fore.CYAN + "--------------------------")
    print(Fore.YELLOW + "Username: {}".format(max_local_sorted[0][0]))
    print(Fore.YELLOW + "Max Password Age: {} days".format(max_local_sorted[0][3]))
    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Unique Expired Local Privileged IDs - Average Password Age")
    print(Fore.CYAN + "--------------------------")
    print(Fore.YELLOW + "Total Percent Non-Compliant: {:.1%}".format(percent_local_overall))
    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Unique Expired Local Privileged IDs - Count of Accounts Non-Compliant")
    print(Fore.CYAN + "--------------------------")
    print(Fore.YELLOW + "Total Local Accounts Non-Compliant: {}".format(count_local_accounts))
    print(Fore.CYAN + "==========================")

    print(Style.RESET_ALL)
    deinit()


if __name__ == "__main__":
    print_sorted()