#!/usr/bin/env python3
## Automation for CyberArk's Discovery & Audit (DNA) reports. ##

import argparse
import logging
import os
import time

import yaml

import logzero
from dnamic_analysis import Database, DomainCheck, Excel, Metrics
from logzero import logger
from tests import Tests

__author__ = "Joe Garcia, CISSP"
__version__ = "0.5.0-beta.4"
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
    tests = Tests(excel, workbook, worksheet, cfg['console_output'])

    # Declare svc, adm, and both arrays properly
    svc_array = cfg['account_regex']['service_account']
    adm_array = cfg['account_regex']['admin_account']
    regex_array = svc_array + adm_array

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

    expired_domain = db.exec_fromfile("data/sql/ExpiredDomainPrivID.sql")
    all_domain_count = db.exec_fromfile("data/sql/DomainAdminsPUCount.sql")

    domainMaxSorted = Metrics.domain_max(expired_domain)
    domainAverage = Metrics.domain_avg(expired_domain)
    domainPercent = Metrics.domain_percent(expired_domain, all_domain_count, domainMaxSorted)

    tests.domain_expired(
        domainMaxSorted,
        domainAverage[0],
        domainAverage[1],
        domainAverage[2],
        domainPercent[0],
        domainPercent[1],
        domainPercent[2])
    if cfg['test_mode'] is False or cfg['console_output'] is True:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    #########################################
    ## Unique Expired Local Privileged IDs ##
    #########################################

    expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql")
    all_local_count = db.exec_fromfile("data/sql/LocalAdministratorsCount.sql")

    all_local_unique_count = []
    for username in all_local_count:
        all_local_unique_count.append(username)

    localMaxSorted = Metrics.local_max(expired_local)
    localAverage = Metrics.local_avg(expired_local)
    localPercent = Metrics.local_percent(expired_local, all_local_count, localMaxSorted)

    tests.local_expired(
        localMaxSorted,
        localAverage[0],
        localAverage[1],
        localAverage[2],
        localPercent[0],
        localPercent[1],
        localPercent[2],
        len(all_local_count),
        len(set(all_local_unique_count)))
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    #####################################################
    ## Expired Local Admins Total w/ Machine Addresses ##
    #####################################################

    localMaxGrouped = Metrics.local_expired_machines(localMaxSorted)

    tests.local_expired_machines(localMaxGrouped, len(all_local_count), len(localMaxGrouped)/len(all_local_count))
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    ##############################
    ## Local Abandoned Accounts ##
    ##############################

    abandoned_local = db.exec_fromfile("data/sql/LocalAbandonedAccounts.sql")
    abandoned_local_count = db.exec_fromfile("data/sql/LocalAbandonedCount.sql")

    tests.local_abandoned(abandoned_local, len(abandoned_local_count))
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    ###############################
    ## Domain Abandoned Accounts ##
    ###############################

    abandoned_domain = db.exec_fromfile("data/sql/DomainAbandonedAccounts.sql")

    tests.domain_abandoned(abandoned_domain, len(all_domain_count))
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    #########################################################
    ## Accounts w/ Multiple Machine Access - By %age Tiers ##
    #########################################################

    multi_machine_accts = db.exec_fromfile("data/sql/MultipleMachineAccounts.sql")
    all_machines_count = db.exec_fromfile("data/sql/TotalMachinesCount.sql")

    if multi_machine_accts:
        multiMachineAccounts = Metrics.multi_machine_accts(multi_machine_accts, all_machines_count[0][0])
    else:
        multiMachineAccounts = False

    tests.multi_machine_accts(multiMachineAccounts)
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    ##########################
    ## Unique Domain Admins ##
    ##########################

    unique_domain_admins = db.exec_fromfile("data/sql/UniqueDomainAdmins.sql")
    unique_svcacct_domain_admins = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins.sql", True, svc_array)
    unique_svcacct_domain_admins2 = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins2.sql", True, svc_array)

    unique_svcacct_domadm_usernames = []
    if unique_svcacct_domain_admins:
        for username in unique_svcacct_domain_admins:
            unique_svcacct_domadm_usernames.append(username[0])

    unique_svcacct_domadm2_usernames = []
    if unique_svcacct_domain_admins2:
        for username in unique_svcacct_domain_admins2:
            unique_svcacct_domadm2_usernames.append(username[0])

    tests.unique_domain_admins(
        unique_domain_admins, (unique_svcacct_domain_admins+unique_svcacct_domain_admins2),
        set(unique_svcacct_domadm_usernames), set(unique_svcacct_domadm2_usernames))
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    ##########################################
    ## Unique Expired Domain Privileged IDs ##
    ##########################################

    unique_expired_domain = db.exec_fromfile("data/sql/UniqueExpiredDomainPrivID.sql")
    null_check = False

    if unique_expired_domain:
        uniqueDomainMaxSorted = Metrics.unique_domain_max(unique_expired_domain)
        uniqueDomainAverage = Metrics.unique_domain_avg(unique_expired_domain)
        uniqueDomainPercent = Metrics.unique_domain_percent(unique_expired_domain, len(unique_domain_admins), uniqueDomainMaxSorted)
    else:
        null_check = True

    if null_check is True:
        tests.unique_domain_expired_null()
    else:
        tests.unique_domain_expired(
            uniqueDomainMaxSorted,
            uniqueDomainAverage[0],
            uniqueDomainAverage[1],
            uniqueDomainAverage[2],
            uniqueDomainPercent[0],
            uniqueDomainPercent[1],
            uniqueDomainPercent[2])
        if cfg['test_mode'] is False or cfg['console_output']:
            try:
                input("Press ENTER to continue...")
            except EOFError:
                pass
            print()

    ########################################
    ## Personal Accounts Running Services ##
    ########################################

    personal_accts_running_svcs = db.exec_fromfile("data/sql/PersonalAccountsRunningSvcs.sql", True, svc_array)

    tests.personal_accts_running_svcs(
        personal_accts_running_svcs)
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    #######################################################
    ## Non-adm Accounts w/ Local Admin Rights on Systems ##
    #######################################################

    non_admin_with_local_admin = db.exec_fromfile("data/sql/NonAdmLocalAdminAccounts.sql", True, regex_array)

    tests.non_admin_with_local_admin(
        non_admin_with_local_admin)
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    #############################
    ## Unique Expired Services ##
    #############################

    unique_expired_svcs = db.exec_fromfile("data/sql/UniqueExpiredServiceAccounts.sql")
    svc_accts_count = db.exec_fromfile("data/sql/ServiceAccountsCount.sql")

    if unique_expired_svcs and svc_accts_count:
        uniqueSvcMaxSorted = Metrics.unique_svc_max(unique_expired_svcs)
        uniqueSvcAverage = Metrics.unique_svc_avg(unique_expired_svcs)
        uniqueSvcPercent = Metrics.unique_svc_percent(unique_expired_svcs, len(svc_accts_count), len(uniqueSvcMaxSorted))
    else:
        uniqueSvcMaxSorted = 'No services found.'
        uniqueSvcAverage = [0, 0, 0]
        uniqueSvcPercent = [0, 0, 0]

    tests.unique_expired_svcs(
        uniqueSvcMaxSorted,
        uniqueSvcAverage[0],
        uniqueSvcAverage[1],
        uniqueSvcAverage[2],
        uniqueSvcPercent[0],
        uniqueSvcPercent[1],
        uniqueSvcPercent[2])
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    ####################
    ## Clear Text IDs ##
    ####################

    clear_text_ids = db.exec_fromfile("data/sql/ClearTextIDs.sql")

    clear_text_ids_count = 0
    if clear_text_ids:
        for x in range(len(clear_text_ids)):
            clear_text_ids_count += clear_text_ids[x][1]

    tests.clear_text_ids(
        clear_text_ids_count,
        clear_text_ids)
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    ##########################################
    ## Applications w/ Clear Text Passwords ##
    ##########################################

    unique_clear_text_apps = db.exec_fromfile("data/sql/UniqueClearTextApps.sql")

    tests.apps_clear_text_passwords(
        unique_clear_text_apps)
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    #################################################
    ## Risky Expired Service Principal Names (SPN) ##
    #################################################

    risky_spns = db.exec_fromfile("data/sql/UniqueExpiredSPNAccounts.sql")
    spns_count = db.exec_fromfile("data/sql/TotalSPNs.sql")

    tests.risky_spns(
        risky_spns,
        spns_count[0][0])
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    #######################################
    ## Hashes Found on Multiple Machines ##
    #######################################

    hashes_found_on_multiple = db.exec_fromfile("data/sql/HashesFoundOnMultiple.sql")
    hashes_found_on_multiple_admins = db.exec_fromfile("data/sql/HashesFoundOnMultipleAdmins.sql")
    total_privileged_ids = db.exec_fromfile("data/sql/TotalPrivilegedIDs.sql")
    total_hash_srv = 0
    total_hash_wks = 0
    total_hash_name = []
    total_hash_admins_srv = 0
    total_hash_admins_wks = 0

    if hashes_found_on_multiple:
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
        if hashes_found_on_multiple_admins:
            for x in range(len(hashes_found_on_multiple_admins)):
                total_hash_admins_srv += hashes_found_on_multiple_admins[x][4]
                total_hash_admins_wks += hashes_found_on_multiple_admins[x][3]

        #admin_hash_sorted = sorted(admin_hash_found, key=str.lower)

    tests.hashes_found_on_multiple(
        len(unique_hash_name),
        sorted(admin_hash_found, key=str.lower),
        total_hash_srv,
        total_hash_wks,
        total_hash_admins_srv,
        total_hash_admins_wks)
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

    ##################################################################
    ## Accounts Hashes Exposed on Multiple Machines - By %age Tiers ##
    ##################################################################

    multi_machine_hashes = db.exec_fromfile("data/sql/MultipleMachineHashes.sql")

    multiMachineHashes = Metrics.multi_machine_hashes(multi_machine_hashes, all_machines_count[0][0])

    tests.multi_machine_hashes(multiMachineHashes)
    if cfg['test_mode'] is False or cfg['console_output']:
        try:
            input("Press ENTER to continue...")
        except EOFError:
            pass
        print()

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