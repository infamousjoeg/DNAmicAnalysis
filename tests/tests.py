def print_sorted(max_domain_sorted,avg_domain_sorted,max_local_sorted,avg_local_sorted,count_local_accounts):
    """ Simply printing to output values for convenience """
    print("==========================")
    print("Expired Domain Privileged IDs - Max Password Age - Sorted Descending")
    print(max_domain_sorted)
    print("==========================")

    print("==========================")
    print("Expired Domain Privileged IDs - Average Password Age - Sorted Descending")
    print(avg_domain_sorted)
    print("==========================")

    print("==========================")
    print("Unique Expired Local Privileged IDs - Max Password Age - Sorted Descending")
    print(max_local_sorted)
    print("==========================")

    print("==========================")
    print("Unique Expired Local Privileged IDs - Average Password Age - Sorted Descending")
    print(avg_local_sorted)
    print("==========================")

    print("==========================")
    print("Unique Expired Local Privileged IDs - Count of Accounts")
    print(count_local_accounts)
    print("==========================")


if __name__ == "__main__":
    print_sorted()