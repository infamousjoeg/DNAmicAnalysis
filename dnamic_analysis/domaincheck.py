from colorama import Fore, Style, deinit, init

from logzero import logger


class DomainCheck(object):

    def __init__(self, test_flag):
        # Initialize colorama
        init()

        self._test = test_flag


    def yes_or_no(self, question):
        if self._test is False:
            answer = input(Fore.RED + Style.BRIGHT + question + " (y/n): " + Style.NORMAL).lower().strip()
        else:
            answer = "y"

        while not(answer == "y" or answer == "yes" or \
        answer == "n" or answer == "no"):
            print()
            print(Fore.YELLOW + "Please enter " + Style.BRIGHT + "(y) or (n)" + Style.NORMAL + " to proceed.")
            print()
            if self._test is False:
                answer = input(Fore.RED + Style.BRIGHT + question + " (y/n): " + Style.NORMAL).lower().strip()
            else:
                answer = "y"
            if answer[:1] == "y":
                return True
            else:
                return False


    def check(self, domain, domain_names):
        if [d for d in domain_names if domain in d]:
            if len(domain_names) == 1:
                print(Fore.CYAN + "====================================================")
                print(Fore.YELLOW + "Found " + Style.BRIGHT + "{}".format(domain) + Style.NORMAL + " in the provided DNA scan database.")
                print(Style.BRIGHT + "Press ENTER to continue..." + Style.NORMAL)
                if self._test is False:
                    input(Fore.CYAN + "====================================================")
                else:
                    print(Fore.CYAN + "====================================================")
                print(Style.RESET_ALL)
                deinit()
                return True
            else:
                print(Fore.CYAN + "====================================================")
                print(Fore.YELLOW + "Found " + Style.BRIGHT + "{}".format(domain) + Style.NORMAL + " out of {} total domains".format(len(domain_names)))
                print("in the provided DNA scan database.")
                print(Style.BRIGHT + "Press ENTER to continue..." + Style.NORMAL)
                if self._test is False:
                    input(Fore.CYAN + "====================================================")
                else:
                    print(Fore.CYAN + "====================================================")
                print(Style.RESET_ALL)
                deinit()
                return True
        else:
            print(Fore.RED + "====================================================")
            print("Did not find " + Style.BRIGHT + "{}".format(domain) + Style.NORMAL + " in the scanned domains list.")
            print("----------------------------------------------------")
            print(Fore.YELLOW + Style.BRIGHT + 'Domains found:' + Style.NORMAL)
            for x in range(len(domain_names)):
                print(domain_names[x][0])
            print(Fore.RED + "----------------------------------------------------")
            answer = DomainCheck(self._test).yes_or_no("Would you still like to proceed?")
            print(Style.RESET_ALL)
            deinit()
            return answer