#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## Automation for CyberArk's Discovery & Audit (DNA) reports. ##

import argparse
import logging
import os
import platform
import sys
import threading
import time

import logzero
import yaml
from colorama import Fore, Style
from logzero import logger

from dnamic_analysis import Database, DomainCheck, Excel, Metrics, Output

__author__ = "Joe Garcia"
__version__ = "2.0.0"
__license__ = "MIT"

log_timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists('logs'):
    os.makedirs('logs')
LOGFILE = 'logs/DNAmicAnalysis_{}.log'.format(log_timestamp)

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

# Define your animated characters function
def animated_processing():
    chars = "/-\|"
    for char in chars:
        sys.stdout.write('\r'+Fore.RED+'Processing... '+char)
        time.sleep(.1)
        sys.stdout.flush()


def main(cfg):
    ## Main entry point of the app ##

    logger.info("Configuration values read: {}".format(cfg))

    # Check that database file exists
    if not os.path.isfile(cfg['database_file']):
        e = Exception("DNA database file located at {} does not exist.".format(cfg['database_file']))
        logger.exception(e)
        raise e
        
    # Database class init
    db = Database(cfg['database_file'], cfg['include_disabled_accts'], cfg['scan_datetime'], cfg['expiration_days'])

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

    print(status_pre + Fore.CYAN + ' Starting analysis' + status_post)

    #####################################
    ## LEGAL - Domain Compliance Check ##
    #####################################

    domain_names = db.exec_fromfile("data/sql/ADDomainCheck.sql")

    action = DomainCheck(cfg['test_mode']).check(cfg['domain'].lower(), domain_names)

    if action is False:
        e = Exception("{} does not want to proceed, exiting application".format(os.getenv('USER')))
        logger.exception(e)
        raise e

    ###################################
    ## Expired Domain Privileged IDs ##
    ###################################

    metric_name = 'Expired Domain Privileged IDs'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    expired_domain = db.exec_fromfile("data/sql/ExpiredDomainPrivID.sql")
    all_domain_count = db.exec_fromfile("data/sql/DomainAdminsPUCount.sql")

    if expired_domain and all_domain_count:
        domainMaxSorted = Metrics.domain_max(expired_domain)
        domainAverage = Metrics.domain_avg(expired_domain)
        domainPercent = Metrics.domain_percent(expired_domain, all_domain_count, domainMaxSorted)
        domainPasswordAge = Metrics.domain_password_age(expired_domain)
    else:
        domainMaxSorted = False
        domainAverage = [0, 0, 0]
        domainPercent = [0, 0, 0]
    
    process_domain_expired = threading.Thread(
        target=output.domain_expired,
        args=(
            domainMaxSorted,
            domainAverage[0],
            domainAverage[1],
            domainAverage[2],
            domainPercent[0],
            domainPercent[1],
            domainPercent[2],
            domainPasswordAge
        )
    )

    process_domain_expired.daemon = True
    process_domain_expired.start()

    while process_domain_expired.is_alive():
        animated_processing()
    # output.domain_expired(
    #     domainMaxSorted,
    #     domainAverage[0],
    #     domainAverage[1],
    #     domainAverage[2],
    #     domainPercent[0],
    #     domainPercent[1],
    #     domainPercent[2])
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #########################################
    ## Unique Expired Local Privileged IDs ##
    #########################################

    metric_name = 'Unique Expired Local Privileged IDs'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql")
    all_local_count = db.exec_fromfile("data/sql/LocalAdministratorsCount.sql")

    print(expired_local)

    if expired_local and all_local_count:
        all_local_unique_count = []
        for username in all_local_count:
            all_local_unique_count.append(username)

        localMaxSorted = Metrics.local_max(expired_local)
        localAverage = Metrics.local_avg(expired_local)
        localPercent = Metrics.local_percent(expired_local, all_local_count, localMaxSorted)
        localPasswordAge = Metrics.local_password_age(expired_local)
    else:
        localMaxSorted = False
        localAverage = [0, 0, 0]
        localPercent = [0, 0, 0]
        localPasswordAge = {}
        all_local_count = []
        all_local_unique_count = []

    process_local_expired = threading.Thread(
        target=output.local_expired,
        args=(
            localMaxSorted,
            localAverage[0],
            localAverage[1],
            localAverage[2],
            localPercent[0],
            localPercent[1],
            localPercent[2],
            len(all_local_count),
            len(set(all_local_unique_count)),
            localPasswordAge
        )
    )

    process_local_expired.daemon = True
    process_local_expired.start()

    while process_local_expired.is_alive():
        animated_processing()
    # output.local_expired(
    #     localMaxSorted,
    #     localAverage[0],
    #     localAverage[1],
    #     localAverage[2],
    #     localPercent[0],
    #     localPercent[1],
    #     localPercent[2],
    #     len(all_local_count),
    #     len(set(all_local_unique_count)))

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #####################################################
    ## Expired Local Admins Total w/ Machine Addresses ##
    #####################################################

    metric_name = 'Expired Local Admins Total w/ Machine Addresses'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    localMaxGrouped = None
    if localMaxSorted is not False:
        localMaxGrouped = Metrics.local_expired_machines(localMaxSorted)

    if localMaxGrouped and len(all_local_count) != 0:
        process_local_expired_machines = threading.Thread(
            target=output.local_expired_machines,
            args=(
                localMaxGrouped,
                len(all_local_count),
                len(localMaxGrouped)/len(all_local_count),
            )
        )

        process_local_expired_machines.daemon = True
        process_local_expired_machines.start()

        while process_local_expired_machines.is_alive():
            animated_processing()
        # output.local_expired_machines(
        #     localMaxGrouped,
        #     len(all_local_count),
        #     len(localMaxGrouped)/len(all_local_count))

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##############################
    ## Local Abandoned Accounts ##
    ##############################

    metric_name = 'Local Abandoned Accounts'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    abandoned_local = db.exec_fromfile("data/sql/LocalAbandonedAccounts.sql")
    abandoned_local_count = db.exec_fromfile("data/sql/LocalAbandonedCount.sql")

    if not abandoned_local and not abandoned_local_count:
        abandoned_local = False
        abandoned_local_count = []

    process_abandoned_local = threading.Thread(
        target=output.local_abandoned,
        args=(
            abandoned_local,
            len(abandoned_local_count),
        )
    )

    process_abandoned_local.daemon = True
    process_abandoned_local.start()

    while process_abandoned_local.is_alive():
        animated_processing()
    # output.local_abandoned(
    #     abandoned_local,
    #     len(abandoned_local_count))
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ###############################
    ## Domain Abandoned Accounts ##
    ###############################

    metric_name = 'Domain Abandoned Accounts'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    abandoned_domain = db.exec_fromfile("data/sql/DomainAbandonedAccounts.sql")

    if not abandoned_domain or not all_domain_count:
        abandoned_domain = False

    process_abandoned_domain = threading.Thread(
        target=output.domain_abandoned,
        args=(
            abandoned_domain,
            len(all_domain_count),
        )
    )

    process_abandoned_domain.daemon = True
    process_abandoned_domain.start()

    while process_abandoned_domain.is_alive():
        animated_processing()
    # output.domain_abandoned(
    #     abandoned_domain,
    #     len(all_domain_count))

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #########################################################
    ## Accounts w/ Multiple Machine Access - By %age Tiers ##
    #########################################################

    metric_name = 'Accounts w/ Multiple Machine Access - By Percentage Tiers'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    multi_machine_accts = db.exec_fromfile("data/sql/MultipleMachineAccounts.sql")
    all_machines_count = db.exec_fromfile("data/sql/TotalMachinesCount.sql")

    if multi_machine_accts and all_machines_count:
        multiMachineAccounts = Metrics.multi_machine_accts(multi_machine_accts, all_machines_count[0][0])
    else:
        multiMachineAccounts = False

    process_multi_machine_accts = threading.Thread(
        target=output.multi_machine_accts,
        args=(multiMachineAccounts,)
    )

    process_multi_machine_accts.daemon = True
    process_multi_machine_accts.start()

    while process_multi_machine_accts.is_alive():
        animated_processing()
    # output.multi_machine_accts(multiMachineAccounts)

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##########################
    ## Unique Domain Admins ##
    ##########################

    metric_name = 'Unique Domain Admins'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_domain_admins = db.exec_fromfile("data/sql/UniqueDomainAdmins.sql")
    unique_svcacct_domain_admins = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins.sql", True, svc_array)
    unique_svcacct_domain_admins2 = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins2.sql", True, svc_array)

    if unique_domain_admins or unique_svcacct_domain_admins or unique_svcacct_domain_admins2:
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

    process_unique_domain_admins = threading.Thread(
        target=output.unique_domain_admins,
        args=(
            unique_domain_admins,
            (unique_svcacct_domain_admins+unique_svcacct_domain_admins2),
            set(unique_svcacct_domadm_usernames),
            set(unique_svcacct_domadm2_usernames),
        )
    )

    process_unique_domain_admins.daemon = True
    process_unique_domain_admins.start()

    while process_unique_domain_admins.is_alive():
        animated_processing()
    # output.unique_domain_admins(
    #     unique_domain_admins,
    #     (unique_svcacct_domain_admins+unique_svcacct_domain_admins2),
    #     set(unique_svcacct_domadm_usernames),
    #     set(unique_svcacct_domadm2_usernames))

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##########################################
    ## Unique Expired Domain Privileged IDs ##
    ##########################################

    metric_name = 'Unique Expired Domain Privileged IDs'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_expired_domain = db.exec_fromfile("data/sql/UniqueExpiredDomainPrivID.sql")

    if unique_expired_domain and unique_domain_admins is not False:
        uniqueDomainMaxSorted = Metrics.unique_domain_max(unique_expired_domain)
        uniqueDomainAverage = Metrics.unique_domain_avg(unique_expired_domain)
        uniqueDomainPercent = Metrics.unique_domain_percent(unique_expired_domain, len(unique_domain_admins), uniqueDomainMaxSorted)
    else:
        uniqueDomainMaxSorted = False
        uniqueDomainAverage = [0, 0, 0]
        uniqueDomainPercent = [0, 0, 0]

    process_unique_expired_domain = threading.Thread(
        target=output.unique_domain_expired,
        args=(uniqueDomainMaxSorted,
            uniqueDomainAverage[0],
            uniqueDomainAverage[1],
            uniqueDomainAverage[2],
            uniqueDomainPercent[0],
            uniqueDomainPercent[1],
            uniqueDomainPercent[2],
        )
    )

    process_unique_expired_domain.daemon = True
    process_unique_expired_domain.start()

    while process_unique_expired_domain.is_alive():
        animated_processing()
    # output.unique_domain_expired(
    #     uniqueDomainMaxSorted,
    #     uniqueDomainAverage[0],
    #     uniqueDomainAverage[1],
    #     uniqueDomainAverage[2],
    #     uniqueDomainPercent[0],
    #     uniqueDomainPercent[1],
    #     uniqueDomainPercent[2])

    print(status_pre + Fore.GREEN + ' Completed Expired Domain Privileged IDs' + status_post)

    ########################################
    ## Personal Accounts Running Services ##
    ########################################

    metric_name = 'Personal Accounts Running Services'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    personal_accts_running_svcs = db.exec_fromfile("data/sql/PersonalAccountsRunningSvcs.sql", True, svc_array)

    if not personal_accts_running_svcs:
        personal_accts_running_svcs = False

    process_personal_accts_running_svcs = threading.Thread(
        target=output.personal_accts_running_svcs,
        args=(personal_accts_running_svcs,)
    )

    process_personal_accts_running_svcs.daemon = True
    process_personal_accts_running_svcs.start()

    while process_personal_accts_running_svcs.is_alive():
        animated_processing()
    # output.personal_accts_running_svcs(
    #     personal_accts_running_svcs)
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #######################################################
    ## Non-adm Accounts w/ Local Admin Rights on Systems ##
    #######################################################

    metric_name = 'Non-adm Accounts w/ Local Admin Rights on Systems'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    non_admin_with_local_admin = db.exec_fromfile("data/sql/NonAdmLocalAdminAccounts.sql", True, regex_array)

    if not non_admin_with_local_admin:
        non_admin_with_local_admin = False

    process_non_admin_with_local_admin = threading.Thread(
        target=output.non_admin_with_local_admin,
        args=(non_admin_with_local_admin,)
    )

    process_non_admin_with_local_admin.daemon = True
    process_non_admin_with_local_admin.start()

    while process_non_admin_with_local_admin.is_alive():
        animated_processing()
    # output.non_admin_with_local_admin(
    #     non_admin_with_local_admin)

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #####################################
    ## Unique Expired Service Accounts ##
    #####################################

    metric_name = 'Unique Expired Service Accounts'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_expired_svcs_domain = db.exec_fromfile("data/sql/UniqueExpiredServiceAccountsDomain.sql")
    unique_expired_svcs_local = db.exec_fromfile("data/sql/UniqueExpiredServiceAccountsLocal.sql")
    svc_accts_count = db.exec_fromfile("data/sql/ServiceAccountsCount.sql")

    if (unique_expired_svcs_domain or unique_expired_svcs_local) and svc_accts_count:
        unique_expired_svcs = unique_expired_svcs_domain + unique_expired_svcs_local
        uniqueSvcMaxSorted = Metrics.unique_svc_max(unique_expired_svcs)
        uniqueSvcAverage = Metrics.unique_svc_avg(unique_expired_svcs)
        uniqueSvcPercent = Metrics.unique_svc_percent(unique_expired_svcs, len(svc_accts_count), len(uniqueSvcMaxSorted))
    else:
        uniqueSvcMaxSorted = False
        uniqueSvcAverage = [0, 0, 0, 0]
        uniqueSvcPercent = [0, 0, 0, 0]

    process_unique_expired_svc_acct = threading.Thread(
        target=output.unique_expired_svcs,
        args=(
            uniqueSvcMaxSorted,
            uniqueSvcAverage[0],
            uniqueSvcAverage[1],
            uniqueSvcAverage[2],
            uniqueSvcPercent[0],
            uniqueSvcPercent[1],
            uniqueSvcPercent[2],
        )
    )

    process_unique_expired_svc_acct.daemon = True
    process_unique_expired_svc_acct.start()

    while process_unique_expired_svc_acct.is_alive():
        animated_processing()
    # output.unique_expired_svcs(
    #     uniqueSvcMaxSorted,
    #     uniqueSvcAverage[0],
    #     uniqueSvcAverage[1],
    #     uniqueSvcAverage[2],
    #     uniqueSvcPercent[0],
    #     uniqueSvcPercent[1],
    #     uniqueSvcPercent[2])

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ####################
    ## Clear Text IDs ##
    ####################

    metric_name = 'Clear Text IDs'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    clear_text_ids = db.exec_fromfile("data/sql/ClearTextIDs.sql")

    if clear_text_ids:
        clear_text_ids_count = 0
        if clear_text_ids:
            for x in range(len(clear_text_ids)):
                clear_text_ids_count += clear_text_ids[x][1]
    else:
        clear_text_ids_count = False
        clear_text_ids = []

    process_clear_text_ids = threading.Thread(
        target=output.clear_text_ids,
        args=(
            clear_text_ids_count,
            clear_text_ids,
        )
    )

    process_clear_text_ids.daemon = True
    process_clear_text_ids.start()

    while process_clear_text_ids.is_alive():
        animated_processing()
    # output.clear_text_ids(
    #     clear_text_ids_count,
    #     clear_text_ids)
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##########################################
    ## Applications w/ Clear Text Passwords ##
    ##########################################

    metric_name = 'Applications w/ Clear Text Passwords'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_clear_text_apps = db.exec_fromfile("data/sql/UniqueClearTextApps.sql")

    if not unique_clear_text_apps:
        unique_clear_text_apps = False

    process_unique_clear_test_apps = threading.Thread(
        target=output.apps_clear_text_passwords,
        args=(unique_clear_text_apps,)
    )

    process_unique_clear_test_apps.daemon = True
    process_unique_clear_test_apps.start()

    while process_unique_clear_test_apps.is_alive():
        animated_processing()
    # output.apps_clear_text_passwords(
    #     unique_clear_text_apps)
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #################################################
    ## Risky Expired Service Principal Names (SPN) ##
    #################################################

    metric_name = 'Risky Expired Service Principal Names'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    risky_spns = db.exec_fromfile("data/sql/UniqueExpiredSPNAccounts.sql")
    spns_count = db.exec_fromfile("data/sql/TotalSPNs.sql")

    if not risky_spns and not spns_count:
        risky_spns = False
        spns_count[0][0] = None

    process_risky_spns = threading.Thread(
        target=output.risky_spns,
        args=(risky_spns,spns_count[0][0],)
    )

    process_risky_spns.daemon = True
    process_risky_spns.start()

    while process_risky_spns.is_alive():
        animated_processing()
    # output.risky_spns(
    #     risky_spns,
    #     spns_count[0][0])
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #######################################
    ## Hashes Found on Multiple Machines ##
    #######################################

    metric_name = 'Hashes Found on Multiple Machines'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    hashes_found_on_multiple = db.exec_fromfile("data/sql/HashesFoundOnMultiple.sql")
    hashes_found_on_multiple_admins = db.exec_fromfile("data/sql/HashesFoundOnMultipleAdmins.sql")
    total_privileged_ids = db.exec_fromfile("data/sql/TotalPrivilegedIDs.sql")

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

    process_hashes_found_on_multiple = threading.Thread(
        target=output.hashes_found_on_multiple,
        args=(
            len(unique_hash_name),
            sorted(admin_hash_found, key=str.lower),
            total_hash_srv,
            total_hash_wks,
            total_hash_admins_srv,
            total_hash_admins_wks,
        )
    )

    process_hashes_found_on_multiple.daemon = True
    process_hashes_found_on_multiple.start()

    while process_hashes_found_on_multiple.is_alive():
        animated_processing()
    # output.hashes_found_on_multiple(
    #     len(unique_hash_name),
    #     sorted(admin_hash_found, key=str.lower),
    #     total_hash_srv,
    #     total_hash_wks,
    #     total_hash_admins_srv,
    #     total_hash_admins_wks)

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##################################################################
    ## Account Hashes that Expose Multiple Machines - By %age Tiers ##
    ##################################################################

    metric_name = 'Account Hashes that Expose Multiple Machines'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    multi_machine_hashes = db.exec_fromfile("data/sql/MultipleMachineHashes.sql")

    if multi_machine_hashes and all_machines_count:
        multiMachineHashes = Metrics.multi_machine_hashes(multi_machine_hashes, all_machines_count[0][0])
    else:
        multiMachineHashes = False

    process_multiple_machine_hashes = threading.Thread(
        target=output.multi_machine_hashes,
        args=(multiMachineHashes,)
    )

    process_multiple_machine_hashes.daemon = True
    process_multiple_machine_hashes.start()

    while process_multiple_machine_hashes.is_alive():
        animated_processing()

    # output.multi_machine_hashes(multiMachineHashes)

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    print('\r\n' + status_pre + Fore.CYAN + ' DNAmic Analysis has completed!' + status_post)

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
