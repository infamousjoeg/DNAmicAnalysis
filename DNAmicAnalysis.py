#!/usr/bin/env python3
## Automation for CyberArk's Discovery & Audit (DNA) reports. ##

import argparse
import logging
import os
import platform
import time

import yaml
from colorama import Fore, Style

import logzero
from alive_progress import alive_bar, config_handler, print_chars
from dnamic_analysis import Database, DomainCheck, Excel, Metrics, Output
from logzero import logger

__author__ = "Joe Garcia"
__version__ = "1.0.4"
__license__ = "MIT"

log_timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists('logs'):
    os.makedirs('logs')
LOGFILE = 'logs/DNAmicAnalysis_{}.log'.format(log_timestamp)

# Set alive_progress bar theme
config_handler.set_global(theme="smooth", enrich_print=False)

def config_logger(logfile):
    ## Configures logging of this application ##
    # Set a minimum log level
    logzero.loglevel(logging.INFO)

    # Set a logfile (all future log messages are also saved there), but disable
    # the default stderr logging
    logzero.logfile(logfile, disableStderrLogger=True)

    # Set a custom formatter
    formatter = logging.Formatter('DNAmicAnalysis - %(asctime)-15s - %(levelname)s: %(message)s');
    logzero.formatter(formatter)


def main(cfg):
    ## Main entry point of the app ##

    logger.info("Configuration values read: {}".format(cfg))

    # Check that database file exists
    if not os.path.isfile(cfg['database_file']):
        e = Exception("DNA database file located at {} does not exist.".format(cfg['database_file']))
        logger.exception(e)
        raise e
        
    # Database class init
    db = Database(cfg['database_file'], cfg['include_disabled_accts'], cfg['scan_datetime'])

    # Excel class init
    excel = Excel(cfg['domain'].lower())
    workbook = excel.create()
    worksheet = excel.add(workbook, cfg['domain'].lower())

    # Tests class init
    output = Output(excel, workbook, worksheet)

    # Declare svc, adm, and both arrays properly
    svc_array = cfg['account_regex']['service_account']
    adm_array = cfg['account_regex']['admin_account']
    regex_array = svc_array + adm_array

    # Declare status message formatting
    status_pre = '\r\n' + Fore.YELLOW + Style.BRIGHT + '==>' + Style.NORMAL + ' '
    status_post = Fore.WHITE + '\r\n'
    if platform.uname().system == 'Windows':
        status_start = ''
        status_step = ''
        status_finish = ''
    else:
        status_start = '🧪'
        status_step = '✅'
        status_finish = '🏁'

    print(status_pre + status_start + Fore.CYAN + ' Starting analysis' + status_post)

    #####################################
    ## LEGAL - Domain Compliance Check ##
    #####################################

    with alive_bar(1) as bar:
        bar('Querying database...')
        domain_names = db.exec_fromfile("data/sql/ADDomainCheck.sql")

    action = DomainCheck(cfg['test_mode']).check(cfg['domain'].lower(), domain_names)

    if action is False:
        e = Exception("{} does not want to proceed, exiting application".format(os.getenv('USER')))
        logger.exception(e)
        raise e

    ###################################
    ## Expired Domain Privileged IDs ##
    ###################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        expired_domain = db.exec_fromfile("data/sql/ExpiredDomainPrivID.sql")
        all_domain_count = db.exec_fromfile("data/sql/DomainAdminsPUCount.sql")

        bar('Processing metrics...')
        if expired_domain and all_domain_count:
            domainMaxSorted = Metrics.domain_max(expired_domain)
            domainAverage = Metrics.domain_avg(expired_domain)
            domainPercent = Metrics.domain_percent(expired_domain, all_domain_count, domainMaxSorted)
        else:
            domainMaxSorted = False
            domainAverage = [0, 0, 0]
            domainPercent = [0, 0, 0]

        bar('Output to Excel spreadsheet...')
        output.domain_expired(
            domainMaxSorted,
            domainAverage[0],
            domainAverage[1],
            domainAverage[2],
            domainPercent[0],
            domainPercent[1],
            domainPercent[2])
        
    print(status_pre + status_step + Fore.GREEN + ' Completed Expired Domain Privileged IDs' + status_post)

    #########################################
    ## Unique Expired Local Privileged IDs ##
    #########################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql")
        all_local_count = db.exec_fromfile("data/sql/LocalAdministratorsCount.sql")

        bar('Processing metrics...')
        if expired_local and all_local_count:
            all_local_unique_count = []
            for username in all_local_count:
                all_local_unique_count.append(username)

            localMaxSorted = Metrics.local_max(expired_local)
            localAverage = Metrics.local_avg(expired_local)
            localPercent = Metrics.local_percent(expired_local, all_local_count, localMaxSorted)
        else:
            localMaxSorted = False
            localAverage = [0, 0, 0]
            localPercent = [0, 0, 0]
            all_local_count = []
            all_local_unique_count = []

        bar('Output to Excel spreadsheet...')
        output.local_expired(
            localMaxSorted,
            localAverage[0],
            localAverage[1],
            localAverage[2],
            localPercent[0],
            localPercent[1],
            localPercent[2],
            len(all_local_count),
            len(set(all_local_unique_count)))

    print(status_pre + status_step + Fore.GREEN + ' Completed Unique Expired Local Privileged IDs' + status_post)

    #####################################################
    ## Expired Local Admins Total w/ Machine Addresses ##
    #####################################################

    with alive_bar(2) as bar:
        bar('Processing metrics...')
        localMaxGrouped = None
        if localMaxSorted is not False:
            localMaxGrouped = Metrics.local_expired_machines(localMaxSorted)

        bar('Output to Excel spreadsheet...')
        if localMaxGrouped and len(all_local_count) != 0:
            output.local_expired_machines(
                localMaxGrouped,
                len(all_local_count),
                len(localMaxGrouped)/len(all_local_count))

    print(status_pre + status_step + Fore.GREEN + ' Completed Expired Local Admins Total w/ Machine Addresses' + status_post)

    ##############################
    ## Local Abandoned Accounts ##
    ##############################

    with alive_bar(3) as bar:
        bar('Querying database...')
        abandoned_local = db.exec_fromfile("data/sql/LocalAbandonedAccounts.sql")
        abandoned_local_count = db.exec_fromfile("data/sql/LocalAbandonedCount.sql")

        bar('Processing metrics...')
        if not abandoned_local and not abandoned_local_count:
            abandoned_local = False
            abandoned_local_count = []

        bar('Output to Excel spreadsheet...')
        output.local_abandoned(
            abandoned_local,
            len(abandoned_local_count))
        
    print(status_pre + status_step + Fore.GREEN + ' Completed Local Abandoned Accounts' + status_post)

    ###############################
    ## Domain Abandoned Accounts ##
    ###############################

    with alive_bar(3) as bar:
        bar('Querying database...')
        abandoned_domain = db.exec_fromfile("data/sql/DomainAbandonedAccounts.sql")

        bar('Processing metrics...')
        if not abandoned_domain or not all_domain_count:
            abandoned_domain = False

        bar('Output to Excel spreadsheet...')
        output.domain_abandoned(
            abandoned_domain,
            len(all_domain_count))

    print(status_pre + status_step + Fore.GREEN + ' Completed Domain Abandoned Accounts' + status_post)

    #########################################################
    ## Accounts w/ Multiple Machine Access - By %age Tiers ##
    #########################################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        multi_machine_accts = db.exec_fromfile("data/sql/MultipleMachineAccounts.sql")
        all_machines_count = db.exec_fromfile("data/sql/TotalMachinesCount.sql")

        bar('Processing metrics...')
        if multi_machine_accts and all_machines_count:
            multiMachineAccounts = Metrics.multi_machine_accts(multi_machine_accts, all_machines_count[0][0])
        else:
            multiMachineAccounts = False

        bar('Output to Excel spreadsheet...')
        output.multi_machine_accts(multiMachineAccounts)

    print(status_pre + status_step + Fore.GREEN + ' Completed Accounts w/ Multiple Machine Access - By Percentage Tiers' + status_post)

    ##########################
    ## Unique Domain Admins ##
    ##########################

    with alive_bar(3) as bar:
        bar('Querying database...')
        unique_domain_admins = db.exec_fromfile("data/sql/UniqueDomainAdmins.sql")
        unique_svcacct_domain_admins = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins.sql", True, svc_array)
        unique_svcacct_domain_admins2 = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins2.sql", True, svc_array)

        bar('Processing metrics...')
        if unique_domain_admins and unique_svcacct_domain_admins and unique_svcacct_domain_admins2:
            unique_svcacct_domadm_usernames = []
            if unique_svcacct_domain_admins:
                for username in unique_svcacct_domain_admins:
                    unique_svcacct_domadm_usernames.append(username[0])

            unique_svcacct_domadm2_usernames = []
            if unique_svcacct_domain_admins2:
                for username in unique_svcacct_domain_admins2:
                    unique_svcacct_domadm2_usernames.append(username[0])
        else:
            unique_domain_admins = False
            unique_svcacct_domain_admins = []
            unique_svcacct_domain_admins2 = []
            unique_svcacct_domadm2_admins = []
            unique_svcacct_domadm_usernames = []
            unique_svcacct_domadm2_usernames = []

        bar('Output to Excel spreadsheet...')
        output.unique_domain_admins(
            unique_domain_admins,
            (unique_svcacct_domain_admins+unique_svcacct_domain_admins2),
            set(unique_svcacct_domadm_usernames),
            set(unique_svcacct_domadm2_usernames))

    print(status_pre + status_step + Fore.GREEN + ' Completed Unique Domain Admins' + status_post)

    ##########################################
    ## Unique Expired Domain Privileged IDs ##
    ##########################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        unique_expired_domain = db.exec_fromfile("data/sql/UniqueExpiredDomainPrivID.sql")

        bar('Processing metrics...')
        if unique_expired_domain and unique_domain_admins is not False:
            uniqueDomainMaxSorted = Metrics.unique_domain_max(unique_expired_domain)
            uniqueDomainAverage = Metrics.unique_domain_avg(unique_expired_domain)
            uniqueDomainPercent = Metrics.unique_domain_percent(unique_expired_domain, len(unique_domain_admins), uniqueDomainMaxSorted)
        else:
            uniqueDomainMaxSorted = False
            uniqueDomainAverage = [0, 0, 0]
            uniqueDomainPercent = [0, 0, 0]

        bar('Output to Excel spreadsheet...')
        output.unique_domain_expired(
            uniqueDomainMaxSorted,
            uniqueDomainAverage[0],
            uniqueDomainAverage[1],
            uniqueDomainAverage[2],
            uniqueDomainPercent[0],
            uniqueDomainPercent[1],
            uniqueDomainPercent[2])

    print(status_pre + status_step + Fore.GREEN + ' Completed Expired Domain Privileged IDs' + status_post)

    ########################################
    ## Personal Accounts Running Services ##
    ########################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        personal_accts_running_svcs = db.exec_fromfile("data/sql/PersonalAccountsRunningSvcs.sql", True, svc_array)

        bar('Processing metrics...')
        if not personal_accts_running_svcs:
            personal_accts_running_svcs = False

        bar('Output to Excel spreadsheet...')
        output.personal_accts_running_svcs(
            personal_accts_running_svcs)
        
    print(status_pre + status_step + Fore.GREEN + ' Completed Personal Accounts Running Services' + status_post)

    #######################################################
    ## Non-adm Accounts w/ Local Admin Rights on Systems ##
    #######################################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        non_admin_with_local_admin = db.exec_fromfile("data/sql/NonAdmLocalAdminAccounts.sql", True, regex_array)

        bar('Processing metrics...')
        if not non_admin_with_local_admin:
            non_admin_with_local_admin = False

        bar('Output to Excel spreadsheet...')
        output.non_admin_with_local_admin(
            non_admin_with_local_admin)

    print(status_pre + status_step + Fore.GREEN + ' Completed Non-adm Accounts w/ Local Admin Rights on Systems' + status_post)

    #####################################
    ## Unique Expired Service Accounts ##
    #####################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        unique_expired_svcs_domain = db.exec_fromfile("data/sql/UniqueExpiredServiceAccountsDomain.sql")
        unique_expired_svcs_local = db.exec_fromfile("data/sql/UniqueExpiredServiceAccountsLocal.sql")
        svc_accts_count = db.exec_fromfile("data/sql/ServiceAccountsCount.sql")

        bar('Processing metrics...')
        if (unique_expired_svcs_domain or unique_expired_svcs_local) and svc_accts_count:
            unique_expired_svcs = unique_expired_svcs_domain + unique_expired_svcs_local
            uniqueSvcMaxSorted = Metrics.unique_svc_max(unique_expired_svcs)
            uniqueSvcAverage = Metrics.unique_svc_avg(unique_expired_svcs)
            uniqueSvcPercent = Metrics.unique_svc_percent(unique_expired_svcs, len(svc_accts_count), len(uniqueSvcMaxSorted))
        else:
            uniqueSvcMaxSorted = False
            uniqueSvcAverage = [0, 0, 0, 0]
            uniqueSvcPercent = [0, 0, 0, 0]

        bar('Output to Excel spreadsheet...')
        output.unique_expired_svcs(
            uniqueSvcMaxSorted,
            uniqueSvcAverage[0],
            uniqueSvcAverage[1],
            uniqueSvcAverage[2],
            uniqueSvcPercent[0],
            uniqueSvcPercent[1],
            uniqueSvcPercent[2])

    print(status_pre + status_step + Fore.GREEN + ' Completed Unique Expired Service Accounts' + status_post)

    ####################
    ## Clear Text IDs ##
    ####################

    with alive_bar(3) as bar:
        bar('Querying database...')
        clear_text_ids = db.exec_fromfile("data/sql/ClearTextIDs.sql")

        bar('Processing metrics...')
        if clear_text_ids:
            clear_text_ids_count = 0
            if clear_text_ids:
                for x in range(len(clear_text_ids)):
                    clear_text_ids_count += clear_text_ids[x][1]
        else:
            clear_text_ids_count = False
            clear_text_ids = []

        bar('Output to Excel spreadsheet...')
        output.clear_text_ids(
            clear_text_ids_count,
            clear_text_ids)
        
    print(status_pre + status_step + Fore.GREEN + ' Completed Clear Text IDs' + status_post)

    ##########################################
    ## Applications w/ Clear Text Passwords ##
    ##########################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        unique_clear_text_apps = db.exec_fromfile("data/sql/UniqueClearTextApps.sql")

        bar('Processing metrics...')
        if not unique_clear_text_apps:
            unique_clear_text_apps = False

        bar('Output to Excel spreadsheet...')
        output.apps_clear_text_passwords(
            unique_clear_text_apps)
        
    print(status_pre + status_step + Fore.GREEN + ' Completed Applications w/ Clear Text Passwords' + status_post)

    #################################################
    ## Risky Expired Service Principal Names (SPN) ##
    #################################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        risky_spns = db.exec_fromfile("data/sql/UniqueExpiredSPNAccounts.sql")
        spns_count = db.exec_fromfile("data/sql/TotalSPNs.sql")

        bar('Processing metrics...')
        if not risky_spns and not spns_count:
            risky_spns = False
            spns_count[0][0] = None

        bar('Output to Excel spreadsheet...')
        output.risky_spns(
            risky_spns,
            spns_count[0][0])
        
    print(status_pre + status_step + Fore.GREEN + ' Completed Risky Expired Service Principal Names' + status_post)

    #######################################
    ## Hashes Found on Multiple Machines ##
    #######################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        hashes_found_on_multiple = db.exec_fromfile("data/sql/HashesFoundOnMultiple.sql")
        hashes_found_on_multiple_admins = db.exec_fromfile("data/sql/HashesFoundOnMultipleAdmins.sql")
        total_privileged_ids = db.exec_fromfile("data/sql/TotalPrivilegedIDs.sql")

        bar('Processing metrics...')
        if hashes_found_on_multiple and hashes_found_on_multiple_admins and total_privileged_ids:
            total_hash_srv = 0
            total_hash_wks = 0
            total_hash_name = []
            total_hash_admins_srv = 0
            total_hash_admins_wks = 0

            for x in range(len(hashes_found_on_multiple)):
                total_hash_srv += hashes_found_on_multiple[x][4]
                total_hash_wks += hashes_found_on_multiple[x][3]
                total_hash_name.append(hashes_found_on_multiple[x][0])
            unique_hash_name = set(total_hash_name)

            admin_hash_found = []
            for hash_name in unique_hash_name:
                for x in range(len(total_privileged_ids)):
                    if hash_name == total_privileged_ids[x][0]:
                        admin_hash_found.append(hash_name)

            # This is looking for hashes returned that are in the Domain Group "Domain Admins"
            for x in range(len(hashes_found_on_multiple_admins)):
                total_hash_admins_srv += hashes_found_on_multiple_admins[x][4]
                total_hash_admins_wks += hashes_found_on_multiple_admins[x][3]
        else:
            unique_hash_name = []
            admin_hash_found = []
            total_hash_srv = False
            total_hash_wks = 0
            total_hash_admins_srv = 0
            total_hash_admins_wks = 0

        bar('Output to Excel spreadsheet...')
        output.hashes_found_on_multiple(
            len(unique_hash_name),
            sorted(admin_hash_found, key=str.lower),
            total_hash_srv,
            total_hash_wks,
            total_hash_admins_srv,
            total_hash_admins_wks)

    print(status_pre + status_step + Fore.GREEN + ' Completed Hashes Found on Multiple Machines' + status_post)

    ##################################################################
    ## Account Hashes that Expose Multiple Machines - By %age Tiers ##
    ##################################################################

    with alive_bar(3) as bar:
        bar('Querying database...')
        multi_machine_hashes = db.exec_fromfile("data/sql/MultipleMachineHashes.sql")

        bar('Processing metrics...')
        if multi_machine_hashes and all_machines_count:
            multiMachineHashes = Metrics.multi_machine_hashes(multi_machine_hashes, all_machines_count[0][0])
        else:
            multiMachineHashes = False

        bar('Output to Excel spreadsheet...')
        output.multi_machine_hashes(multiMachineHashes)

    print(status_pre + status_step + Fore.GREEN + ' Completed Account Hashes that Expose Multiple Machines' + status_post)

    print('\r\n' + status_pre + status_finish + Fore.CYAN + ' DNAmic Analysis has completed!' + status_post)

##########
## Main ##
##########

if __name__ == "__main__":
    ## This is executed when run from the command line ##

    # Configure logging
    config_logger(LOGFILE)
    logger.info("Application initialized successfully")

    # Create argument parsing object
    parser = argparse.ArgumentParser(
        description="CyberArk DNA report generation utility")

    # Required positional argument for database file to query against
    parser.add_argument(
        "config_file",
        help="filename of config.yml file to use from configs directory")

    # Optional argument flag to output current version
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
        help="shows current version information and exit")

    # Parse all arguments
    args = parser.parse_args()

    # Read configuration file from config/ that was provided in argument
    config_filename = "config/" + args.config_file
    with open(config_filename, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    main(cfg)
