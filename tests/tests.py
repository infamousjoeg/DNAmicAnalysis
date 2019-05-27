from colorama import init, deinit, Fore, Style

def print_sorted(max_domain_sorted,avg_domain_sorted,max_local_sorted,avg_local_sorted,count_local_accounts):
    """ Simply printing to output values for convenience """
    # Initialize colorama in case Windows OS
    init()

    print(Fore.CYAN + "==========================")
    print(Fore.RED + "Expired Domain Privileged IDs - Max Password Age - Sorted Descending")
    
    for result in max_domain_sorted:
        print(Fore.CYAN + "--------------------------")
        print(Fore.YELLOW + "Username: {}".format(result[0]))
        print(Fore.YELLOW + "Max Password Age: {}".format(result[2]))


    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Expired Domain Privileged IDs - Average Password Age - Sorted Descending")

    for result in avg_domain_sorted:
        print(Fore.CYAN + "--------------------------")
        print(Fore.YELLOW + "Username: {}".format(result[0]))
        print(Fore.YELLOW + "Avg Password Age: {}".format(result[3]))


    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Unique Expired Local Privileged IDs - Max Password Age - Sorted Descending")

    for result in max_local_sorted:
        print(Fore.CYAN + "--------------------------")
        print(Fore.YELLOW + "Username: {}".format(result[0]))
        print(Fore.YELLOW + "Address: {}".format(result[1]))
        print(Fore.YELLOW + "Max Password Age: {}".format(result[3]))


    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Unique Expired Local Privileged IDs - Average Password Age - Sorted Descending")

    for result in avg_local_sorted:
        print(Fore.CYAN + "--------------------------")
        print(Fore.YELLOW + "Username: {}".format(result[0]))
        print(Fore.YELLOW + "Address: {}".format(result[1]))
        print(Fore.YELLOW + "Avg Password Age: {}".format(result[4]))


    print(Fore.CYAN + "==========================")
    print()

    print("==========================")
    print(Fore.RED + "Unique Expired Local Privileged IDs - Count of Accounts")
    print(Fore.CYAN + "--------------------------")
    print(Fore.YELLOW + "Total Local Accounts: {}".format(count_local_accounts))
    print(Fore.CYAN + "==========================")

    print(Style.RESET_ALL)
    deinit()


if __name__ == "__main__":
    print_sorted()