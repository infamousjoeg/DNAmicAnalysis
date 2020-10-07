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

from dnamic_analysis import Database, DomainCheck, Xlsx, Metrics, Output

__author__ = "Joe Garcia"
__version__ = "2.1.1"
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
    formatter = logging.Formatter('DNAmicAnalysis - %(asctime)-15s - %(levelname)s: %(message)s')
    logzero.formatter(formatter)


def main(cfg):
    ## Main entry point of the app ##

    logger.info("Configuration values read: {}".format(cfg))

    # Check that database file exists
    for dbfile in cfg['database_files']:
        if not os.path.isfile(dbfile):
            e = Exception("DNA database file located at {} does not exist.".format(dbfile))
            logger.exception(e)
            raise e
        
    # Database class init
    db = Database(cfg['database_files'], cfg['include_disabled_accts'], cfg['scan_datetime'], cfg['expiration_days'])

    # Xlsx class init
    xlsx = Xlsx(cfg['domain'].lower())
    workbook = xlsx.create_workbook()

    # Tests class init
    output = Output(xlsx, workbook)

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

    domain_names = db.exec_fromfile("data/sql/ADDomainCheck.sql", "Domain Compliance Check")

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

    expired_domain = db.exec_fromfile("data/sql/ExpiredDomainPrivID.sql", "Expired Domain Privileged IDs")
    all_domain_count = db.exec_fromfile("data/sql/DomainAdminsPUCount.sql", "Domain Admins Total Count")

    if expired_domain and all_domain_count:
        domainMaxSorted = Metrics.domain_max(expired_domain)
        domainAverage = Metrics.domain_avg(expired_domain)
        domainPercent = Metrics.domain_percent(expired_domain, all_domain_count, domainMaxSorted)
        domainPasswordAge = Metrics.password_age(expired_domain)
        domainNumMachines = Metrics.number_of_machines(expired_domain, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        worksheet = None
        domainMaxSorted = False
        domainAverage = [0, 0, 0]
        domainPercent = [0, 0, 0]
        domainPasswordAge = None
        domainNumMachines = None
    output.domain_expired(
        worksheet,
        domainMaxSorted,
        domainAverage[0],
        domainAverage[1],
        domainAverage[2],
        domainPercent[0],
        domainPercent[1],
        domainPercent[2],
        domainPasswordAge,
        domainNumMachines
    )
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #########################################
    ## Unique Expired Local Privileged IDs ##
    #########################################

    metric_name = 'Unique Expired Local Privileged IDs'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql", "Unique Expired Local Privileged IDs")
    all_local_count = db.exec_fromfile("data/sql/LocalAdministratorsCount.sql", "Local Administrator Total Count")

    if expired_local and all_local_count:
        print(expired_local)
        all_local_unique_count = []
        for username in all_local_count:
            all_local_unique_count.append(username)

        localMaxSorted = Metrics.local_max(expired_local)
        localAverage = Metrics.local_avg(expired_local)
        localPercent = Metrics.local_percent(expired_local, all_local_count, localMaxSorted)
        localPasswordAge = Metrics.password_age(expired_local)
        localNumMachines = Metrics.number_of_machines(expired_local, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        localMaxSorted = False
        localAverage = [0, 0, 0]
        localPercent = [0, 0, 0]
        localPasswordAge = None
        localNumMachines = None
        all_local_count = []
        all_local_unique_count = []
        worksheet = None

    output.local_expired(
        worksheet,
        localMaxSorted,
        localAverage[0],
        localAverage[1],
        localAverage[2],
        localPercent[0],
        localPercent[1],
        localPercent[2],
        len(all_local_count),
        len(set(all_local_unique_count)),
        localPasswordAge,
        localNumMachines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #####################################################
    ## Expired Local Admins Total w/ Machine Addresses ##
    #####################################################

    metric_name = 'Expired Local Admins Total w Machine Addresses'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    localMaxGrouped = None
    if localMaxSorted is not False:
        localMaxGrouped = Metrics.local_expired_machines(localMaxSorted)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])

    if localMaxGrouped and len(all_local_count) != 0:
        output.local_expired_machines(
            worksheet,
            localMaxGrouped,
            len(all_local_count),
            len(localMaxGrouped)/len(all_local_count),
        )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##############################
    ## Local Abandoned Accounts ##
    ##############################

    metric_name = 'Local Abandoned Accounts'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    abandoned_local = db.exec_fromfile("data/sql/LocalAbandonedAccounts.sql", "Local Abandoned Accounts")
    abandoned_local_count = db.exec_fromfile("data/sql/LocalAbandonedCount.sql", "Local Abandoned Total Count")

    if not abandoned_local:
        abandoned_local = False
        abandoned_local_count = []
        abandoned_local_passwordage = None
        abandoned_local_num_machines = None
        worksheet = None
    else:
        abandoned_local_passwordage = Metrics.password_age(abandoned_local)
        abandoned_local_num_machines = Metrics.number_of_machines(abandoned_local, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])

    output.local_abandoned(
        worksheet,
        abandoned_local,
        len(abandoned_local_count),
        abandoned_local_passwordage,
        abandoned_local_num_machines
    )
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ###############################
    ## Domain Abandoned Accounts ##
    ###############################

    metric_name = 'Domain Abandoned Accounts'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    abandoned_domain = db.exec_fromfile("data/sql/DomainAbandonedAccounts.sql", "Domain Abandoned Accounts")

    if not abandoned_domain or not all_domain_count:
        abandoned_domain = False
        abandoned_domain_passwordage = None
        abandoned_domain_num_machines = None
        worksheet = None
    else:
        abandoned_domain_passwordage = Metrics.password_age(abandoned_domain)
        abandoned_domain_num_machines = Metrics.number_of_machines(abandoned_domain, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])

    output.domain_abandoned(
        worksheet,
        abandoned_domain,
        len(all_domain_count),
        abandoned_domain_passwordage,
        abandoned_domain_num_machines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #########################################################
    ## Accounts w/ Multiple Machine Access - By %age Tiers ##
    #########################################################

    metric_name = 'Accounts w Multiple Machine Access By Percentage Tiers'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    multi_machine_accts = db.exec_fromfile("data/sql/MultipleMachineAccounts.sql", "Multiple Machine Accounts")
    all_machines_count = db.exec_fromfile("data/sql/TotalMachinesCount.sql", "Total Machines Count")

    if multi_machine_accts and all_machines_count:
        multiMachineAccounts = Metrics.multi_machine_accts(multi_machine_accts, all_machines_count[0][0])
        multiMachinePasswordAge = Metrics.password_age(multi_machine_accts)
        multiMachineNumMachines = Metrics.number_of_machines(multi_machine_accts, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        multiMachineAccounts = False
        multiMachinePasswordAge = None
        multiMachineNumMachines = None
        worksheet = None

    output.multi_machine_accts(
        worksheet,
        multiMachineAccounts,
        multiMachinePasswordAge,
        multiMachineNumMachines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #########################################################
    ## Domain Admin Accounts w/ Multiple Machine Access - By %age Tiers ##
    #########################################################

    metric_name = 'Domain Admin Accounts w Multiple Machine Access By Percentage Tiers'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    multi_machine_accts_da = db.exec_fromfile("data/sql/MultipleMachineAccountsDA.sql", "Multiple Machine Accounts DA")

    if multi_machine_accts_da and all_machines_count:
        multiMachineAccountsDA = Metrics.multi_machine_accts(multi_machine_accts_da, all_machines_count[0][0])
        multiMachinePasswordAgeDA = Metrics.password_age(multi_machine_accts_da)
        multiMachineNumMachinesDA = Metrics.number_of_machines(multi_machine_accts_da, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        multiMachineAccountsDA = False
        multiMachinePasswordAgeDA = None
        multiMachineNumMachinesDA = None
        worksheet = None

    output.multi_machine_accts(
        worksheet,
        multiMachineAccountsDA,
        multiMachinePasswordAgeDA,
        multiMachineNumMachinesDA
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #########################################################
    ## Domain Admin Accounts w/ Multiple Machine Access - By %age Tiers ##
    #########################################################

    metric_name = 'Non-Domain Admin Accounts w Multiple Machine Access By Percentage Tiers'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    multi_machine_accts_nonda = db.exec_fromfile("data/sql/MultipleMachineAccountsNonDA.sql", "Multiple Machine Accounts Non-DA")

    if multi_machine_accts_da and all_machines_count:
        multiMachineAccountsNonDA = Metrics.multi_machine_accts(multi_machine_accts_nonda, all_machines_count[0][0])
        multiMachinePasswordAgeNonDA = Metrics.password_age(multi_machine_accts_nonda)
        multiMachineNumMachinesNonDA = Metrics.number_of_machines(multi_machine_accts_nonda, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        multiMachineAccountsNonDA = False
        multiMachinePasswordAgeNonDA = None
        multiMachineNumMachinesNonDA = None
        worksheet = None

    output.multi_machine_accts(
        worksheet,
        multiMachineAccountsNonDA,
        multiMachinePasswordAgeNonDA,
        multiMachineNumMachinesNonDA
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##########################
    ## Unique Domain Admins ##
    ##########################

    metric_name = 'Unique Domain Admins'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_domain_admins = db.exec_fromfile("data/sql/UniqueDomainAdmins.sql", "Unique Domain Admins")
    unique_svcacct_domain_admins = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins.sql", "Unique Service Account Domain Admins - 1", True, svc_array)
    unique_svcacct_domain_admins2 = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins2.sql", "Unique Service Account Domain Admins - 2", True, svc_array)

    if unique_domain_admins or unique_svcacct_domain_admins or unique_svcacct_domain_admins2:
        unique_svcacct_domadm_usernames = []
        if unique_svcacct_domain_admins:
            for username in unique_svcacct_domain_admins:
                unique_svcacct_domadm_usernames.append(username[0])

        unique_svcacct_domadm2_usernames = []
        if unique_svcacct_domain_admins2:
            for username in unique_svcacct_domain_admins2:
                unique_svcacct_domadm2_usernames.append(username[0])
        
        unique_domain_combined = []
        if unique_domain_admins:
            unique_domain_combined += unique_domain_admins
        elif unique_svcacct_domain_admins:
            unique_domain_combined += unique_svcacct_domain_admins
        elif unique_svcacct_domain_admins2:
            unique_domain_combined += unique_svcacct_domain_admins2
        unique_domain_passwordage = Metrics.password_age(unique_domain_combined)
        unique_domain_num_machines = Metrics.number_of_machines(unique_domain_combined, metric_name)

        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
        
    else:
        unique_domain_admins = False
        unique_svcacct_domain_admins = []
        unique_svcacct_domain_admins2 = []
        unique_svcacct_domadm2_admins = []
        unique_svcacct_domadm_usernames = []
        unique_svcacct_domadm2_usernames = []
        unique_domain_passwordage = None
        unique_domain_num_machines = None
        worksheet = None

    output.unique_domain_admins(
        worksheet,
        unique_domain_admins,
        (unique_svcacct_domain_admins+unique_svcacct_domain_admins2),
        set(unique_svcacct_domadm_usernames),
        set(unique_svcacct_domadm2_usernames),
        unique_domain_passwordage,
        unique_domain_num_machines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##########################################
    ## Unique Expired Domain Privileged IDs ##
    ##########################################

    metric_name = 'Unique Expired Domain Privileged IDs'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_expired_domain = db.exec_fromfile("data/sql/UniqueExpiredDomainPrivID.sql", "Unique Expired Domain Privileged IDs")

    if unique_expired_domain and unique_domain_admins is not False:
        uniqueDomainMaxSorted = Metrics.unique_domain_max(unique_expired_domain)
        uniqueDomainAverage = Metrics.unique_domain_avg(unique_expired_domain)
        uniqueDomainPercent = Metrics.unique_domain_percent(unique_expired_domain, len(unique_domain_admins), uniqueDomainMaxSorted)
        uniqueDomainPasswordAge = Metrics.password_age(unique_expired_domain)
        uniqueDomainNumMachines = Metrics.number_of_machines(unique_expired_domain, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        uniqueDomainMaxSorted = False
        uniqueDomainAverage = [0, 0, 0]
        uniqueDomainPercent = [0, 0, 0]
        uniqueDomainPasswordAge = None
        uniqueDomainNumMachines = None
        worksheet = None

    output.unique_domain_expired(
        worksheet,
        uniqueDomainMaxSorted,
        uniqueDomainAverage[0],
        uniqueDomainAverage[1],
        uniqueDomainAverage[2],
        uniqueDomainPercent[0],
        uniqueDomainPercent[1],
        uniqueDomainPercent[2],
        uniqueDomainPasswordAge,
        uniqueDomainNumMachines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed Expired Domain Privileged IDs' + status_post)

    ########################################
    ## Personal Accounts Running Services ##
    ########################################

    metric_name = 'Personal Accounts Running Services'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    personal_accts_running_svcs = db.exec_fromfile("data/sql/PersonalAccountsRunningSvcs.sql", "Personal Accounts Running Services", True, svc_array)

    if not personal_accts_running_svcs:
        personal_accts_running_svcs = False
        personal_accts_passwordage = None
        personal_accts_num_machines = None
        worksheet = None
    else:
        personal_accts_passwordage = Metrics.password_age(personal_accts_running_svcs)
        personal_accts_num_machines = Metrics.number_of_machines(personal_accts_running_svcs, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])

    output.personal_accts_running_svcs(
        worksheet,
        personal_accts_running_svcs,
        personal_accts_passwordage,
        personal_accts_num_machines
    )
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #######################################################
    ## Non-adm Accounts w/ Local Admin Rights on Systems ##
    #######################################################

    metric_name = 'Non-adm Accounts w Local Admin Rights on Systems'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    non_admin_with_local_admin = db.exec_fromfile("data/sql/NonAdmLocalAdminAccounts.sql", "Non-Admin Accounts w/ Local Admin", True, regex_array)

    if not non_admin_with_local_admin:
        non_admin_with_local_admin = False
        non_admin_passwordage = None
        non_admin_num_machines = None
        worksheet = None
    else:
        non_admin_passwordage = Metrics.password_age(non_admin_with_local_admin)
        non_admin_num_machines = Metrics.number_of_machines(non_admin_with_local_admin, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])

    output.non_admin_with_local_admin(
        worksheet,
        non_admin_with_local_admin,
        non_admin_passwordage,
        non_admin_num_machines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #####################################
    ## Unique Expired Service Accounts ##
    #####################################

    metric_name = 'Unique Expired Service Accounts'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_expired_svcs_domain = db.exec_fromfile("data/sql/UniqueExpiredServiceAccountsDomain.sql", "Unique Expired Domain Service Accounts")
    unique_expired_svcs_local = db.exec_fromfile("data/sql/UniqueExpiredServiceAccountsLocal.sql", "Unique Expired Local Service Accounts")
    svc_accts_count = db.exec_fromfile("data/sql/ServiceAccountsCount.sql", "Service Accounts Total Count")

    if (unique_expired_svcs_domain or unique_expired_svcs_local) and svc_accts_count:
        unique_expired_svcs = unique_expired_svcs_domain + unique_expired_svcs_local
        uniqueSvcMaxSorted = Metrics.unique_svc_max(unique_expired_svcs)
        uniqueSvcAverage = Metrics.unique_svc_avg(unique_expired_svcs)
        uniqueSvcPercent = Metrics.unique_svc_percent(unique_expired_svcs, len(svc_accts_count), len(uniqueSvcMaxSorted))
        
        uniqueSvcCombined = []
        if unique_expired_svcs_domain:
            uniqueSvcCombined += unique_expired_svcs_domain
        elif unique_expired_svcs_local:
            uniqueSvcCombined += unique_expired_svcs_local
        uniqueSvcPasswordAge = Metrics.password_age(unique_expired_svcs)
        uniqueSvcNumMachines = Metrics.number_of_machines(unique_expired_svcs, metric_name)

        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        uniqueSvcMaxSorted = False
        uniqueSvcAverage = [0, 0, 0, 0]
        uniqueSvcPercent = [0, 0, 0, 0]
        uniqueSvcPasswordAge = None
        uniqueSvcNumMachines = None
        worksheet = None

    output.unique_expired_svcs(
        worksheet,
        uniqueSvcMaxSorted,
        uniqueSvcAverage[0],
        uniqueSvcAverage[1],
        uniqueSvcAverage[2],
        uniqueSvcPercent[0],
        uniqueSvcPercent[1],
        uniqueSvcPercent[2],
        uniqueSvcPasswordAge,
        uniqueSvcNumMachines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ####################
    ## Clear Text IDs ##
    ####################

    metric_name = 'Clear Text IDs'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    clear_text_ids = db.exec_fromfile("data/sql/ClearTextIDs.sql", "Clear Text IDs")

    if clear_text_ids:
        clear_text_ids_count = 0
        if clear_text_ids:
            for x in range(len(clear_text_ids)):
                clear_text_ids_count += clear_text_ids[x][1]
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        clear_text_ids_count = False
        clear_text_ids = []
        worksheet = None

    output.clear_text_ids(
        worksheet,
        clear_text_ids_count,
        clear_text_ids,
    )
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##########################################
    ## Applications w/ Clear Text Passwords ##
    ##########################################

    metric_name = 'Applications w Clear Text Passwords'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    unique_clear_text_apps = db.exec_fromfile("data/sql/UniqueClearTextApps.sql", "Unique Applications w/ Clear Text Passwords")

    if not unique_clear_text_apps:
        unique_clear_text_apps = False
        worksheet = None
    else:
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])

    output.apps_clear_text_passwords(
        worksheet,
        unique_clear_text_apps,
    )
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #################################################
    ## Risky Expired Service Principal Names (SPN) ##
    #################################################

    metric_name = 'Risky Expired Service Principal Names'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    risky_spns = db.exec_fromfile("data/sql/UniqueExpiredSPNAccounts.sql", "Unique Expired SPN Accounts")
    spns_count = db.exec_fromfile("data/sql/TotalSPNs.sql", "Total SPN Count")

    if not risky_spns and not spns_count:
        risky_spns = False
        spns_count[0][0] = None
        spns_passwordage = None
        spns_num_machines = None
        worksheet = None
    else:
        spns_passwordage = Metrics.password_age(risky_spns)
        spns_num_machines = Metrics.number_of_machines(risky_spns, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])

    output.risky_spns(
        worksheet,
        risky_spns,
        spns_count[0][0],
        spns_passwordage,
        spns_num_machines
    )
        
    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    #######################################
    ## Hashes Found on Multiple Machines ##
    #######################################

    metric_name = 'Hashes Found on Multiple Machines'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    hashes_found_on_multiple = db.exec_fromfile("data/sql/HashesFoundOnMultiple.sql", "Hashes Found on Multiple Machines")
    hashes_found_on_multiple_admins = db.exec_fromfile("data/sql/HashesFoundOnMultipleAdmins.sql", "Hashes Found on Multiple Admins")
    total_privileged_ids = db.exec_fromfile("data/sql/TotalPrivilegedIDs.sql", "Total Privileged ID Count")

    if hashes_found_on_multiple and hashes_found_on_multiple_admins and total_privileged_ids:
        total_hash_srv = 0
        total_hash_wks = 0
        total_hash_name = []
        total_hash_admins_srv = 0
        total_hash_admins_wks = 0
        total_hash_combined = hashes_found_on_multiple + hashes_found_on_multiple_admins

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

        total_hash_passwordage = Metrics.password_age(total_hash_combined)
        total_hash_num_machines = Metrics.number_of_machines(total_hash_combined, metric_name)

        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        unique_hash_name = []
        admin_hash_found = []
        total_hash_srv = False
        total_hash_wks = 0
        total_hash_admins_srv = 0
        total_hash_admins_wks = 0
        total_hash_passwordage = None
        total_hash_num_machines = None
        worksheet = None

    output.hashes_found_on_multiple(
        worksheet,
        len(unique_hash_name),
        sorted(admin_hash_found, key=str.lower),
        total_hash_srv,
        total_hash_wks,
        total_hash_admins_srv,
        total_hash_admins_wks,
        total_hash_passwordage,
        total_hash_num_machines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    ##################################################################
    ## Account Hashes that Expose Multiple Machines - By %age Tiers ##
    ##################################################################

    metric_name = 'Account Hashes that Expose Multiple Machines'

    print(status_pre + Fore.YELLOW + ' Starting ' + metric_name + status_post)

    multi_machine_hashes = db.exec_fromfile("data/sql/MultipleMachineHashes.sql", "Hashes Exposed on Multiple Machines")

    if multi_machine_hashes and all_machines_count:
        multiMachineHashes = Metrics.multi_machine_hashes(multi_machine_hashes, all_machines_count[0][0])
        multiMachinePasswordAge = Metrics.password_age(multi_machine_hashes)
        multiMachineNumMachines = Metrics.number_of_machines(multi_machine_hashes, metric_name)
        worksheet = xlsx.add_worksheet(workbook, metric_name[:31])
    else:
        multiMachineHashes = False
        multiMachinePasswordAge = None
        multiMachineNumMachines = None
        worksheet = None

    output.multi_machine_hashes(
        worksheet,
        multiMachineHashes,
        multiMachinePasswordAge,
        multiMachineNumMachines
    )

    print('\r\n' + status_pre + Fore.GREEN + ' Completed ' + metric_name + status_post)

    xlsx.close_workbook(workbook)

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
