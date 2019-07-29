#!/usr/bin/env python3
## Automation for CyberArk's Discovery & Audit (DNA) reports. ##

import argparse
import logging
import os

import logzero
from dnamic_analysis import Database, DomainCheck, Metrics
from logzero import logger
from tests import Tests

__author__ = "Joe Garcia, CISSP"
__version__ = "0.2.0"
__license__ = "MIT"

LOGFILE = 'DNAmicAnalysis.log'

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


def main(args):
    ## Main entry point of the app ##

    logger.info("Arguments received: {}".format(args))

    db = Database(args.database_file, args.disabled)

    svc_array = args.svc_regex.replace(' ', '').split(',')
    adm_array = args.adm_regex.replace(' ', '').split(',')
    regex_array = svc_array + adm_array

    #####################################
    ## LEGAL - Domain Compliance Check ##
    #####################################

    domain_names = db.exec_fromfile("data/sql/ADDomainCheck.sql")

    action = DomainCheck(args.test).check(args.domain.lower(), domain_names)

    if action is False:
        info.logger("{} does not want to proceed, exiting application".format(os.getenv(USER)))
        exit()

    ###################################
    ## Expired Domain Privileged IDs ##
    ###################################

    expired_domain = db.exec_fromfile("data/sql/ExpiredDomainPrivID.sql")
    all_domain_count = db.exec_fromfile("data/sql/DomainAdminsPUCount.sql")

    domainMaxSorted = Metrics.domain_max(expired_domain)
    domainAverage = Metrics.domain_avg(expired_domain)
    domainPercent = Metrics.domain_percent(expired_domain, all_domain_count, domainMaxSorted)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.domain_expired(
            domainMaxSorted,
            domainAverage[0],
            domainAverage[1],
            domainAverage[2],
            domainPercent[0],
            domainPercent[1],
            domainPercent[2])
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #########################################
    ## Unique Expired Local Privileged IDs ##
    #########################################

    expired_local = db.exec_fromfile("data/sql/UniqueExpiredLocalPrivID.sql")
    all_local_count = db.exec_fromfile("data/sql/LocalAdministratorsCount.sql")

    localMaxSorted = Metrics.local_max(expired_local)
    localAverage = Metrics.local_avg(expired_local)
    localPercent = Metrics.local_percent(expired_local, all_local_count, localMaxSorted)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.local_expired(
            localMaxSorted,
            localAverage[0],
            localAverage[1],
            localAverage[2],
            localPercent[0],
            localPercent[1],
            localPercent[2])
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #####################################################
    ## Expired Local Admins Total w/ Machine Addresses ##
    #####################################################

    localMaxGrouped = Metrics.local_expired_machines(localMaxSorted)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.local_expired_machines(localMaxGrouped, len(all_local_count), len(localMaxGrouped)/len(all_local_count))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ##############################
    ## Local Abandoned Accounts ##
    ##############################

    abandoned_local = db.exec_fromfile("data/sql/LocalAbandonedAccounts.sql")

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.local_abandoned(len(abandoned_local), len(all_local_count))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ###############################
    ## Domain Abandoned Accounts ##
    ###############################

    abandoned_domain = db.exec_fromfile("data/sql/DomainAbandonedAccounts.sql")

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.domain_abandoned(len(abandoned_domain), len(all_domain_count))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #########################################################
    ## Accounts w/ Multiple Machine Access - By %age Tiers ##
    #########################################################

    multi_machine_accts = db.exec_fromfile("data/sql/MultipleMachineAccounts.sql")
    all_machines_count = db.exec_fromfile("data/sql/TotalMachinesCount.sql")

    multiMachineAccounts = Metrics.multi_machine_accts(multi_machine_accts, all_machines_count[0][0])

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.multi_machine_accts(multiMachineAccounts)
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ##########################
    ## Unique Domain Admins ##
    ##########################

    unique_domain_admins = db.exec_fromfile("data/sql/UniqueDomainAdmins.sql")
    unique_svcacct_domain_admins = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins.sql", True, svc_array)
    unique_svcacct_domain_admins2 = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins2.sql", True, svc_array)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.unique_domain_admins(
            unique_domain_admins, (unique_svcacct_domain_admins+unique_svcacct_domain_admins2))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ##########################################
    ## Unique Expired Domain Privileged IDs ##
    ##########################################

    unique_expired_domain = db.exec_fromfile("data/sql/UniqueExpiredDomainPrivID.sql")

    uniqueDomainMaxSorted = Metrics.unique_domain_max(unique_expired_domain)
    uniqueDomainAverage = Metrics.unique_domain_avg(unique_expired_domain)
    uniqueDomainPercent = Metrics.unique_domain_percent(unique_expired_domain, len(unique_domain_admins), uniqueDomainMaxSorted)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.unique_domain_expired(
            uniqueDomainMaxSorted,
            uniqueDomainAverage[0],
            uniqueDomainAverage[1],
            uniqueDomainAverage[2],
            uniqueDomainPercent[0],
            uniqueDomainPercent[1],
            uniqueDomainPercent[2])
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ########################################
    ## Personal Accounts Running Services ##
    ########################################

    personal_accts_running_svcs = db.exec_fromfile("data/sql/PersonalAccountsRunningSvcs.sql", True, svc_array)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.personal_accts_running_svcs(
            len(personal_accts_running_svcs))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #######################################################
    ## Non-adm Accounts w/ Local Admin Rights on Systems ##
    #######################################################

    non_admin_with_local_admin = db.exec_fromfile("data/sql/NonAdmLocalAdminAccounts.sql", True, regex_array)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.non_admin_with_local_admin(
            len(non_admin_with_local_admin))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #############################
    ## Unique Expired Services ##
    #############################

    unique_expired_svcs = db.exec_fromfile("data/sql/UniqueExpiredServiceAccounts.sql")
    svc_accts_count = db.exec_fromfile("data/sql/ServiceAccountsCount.sql")

    uniqueSvcMaxSorted = Metrics.unique_svc_max(unique_expired_svcs)
    uniqueSvcAverage = Metrics.unique_svc_avg(unique_expired_svcs)
    uniqueSvcPercent = Metrics.unique_svc_percent(unique_expired_svcs, len(svc_accts_count), len(uniqueSvcMaxSorted))

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.unique_expired_svcs(
            uniqueSvcMaxSorted,
            uniqueSvcAverage[0],
            uniqueSvcAverage[1],
            uniqueSvcAverage[2],
            uniqueSvcPercent[0],
            uniqueSvcPercent[1],
            uniqueSvcPercent[2])
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ####################
    ## Clear Text IDs ##
    ####################

    clear_text_ids = db.exec_fromfile("data/sql/ClearTextIDs.sql")

    clear_text_ids_count = 0
    if clear_text_ids:
        for x in range(len(clear_text_ids)):
            clear_text_ids_count += clear_text_ids[x][1]

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.clear_text_ids(
            clear_text_ids_count,
            clear_text_ids)
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ##########################################
    ## Applications w/ Clear Text Passwords ##
    ##########################################

    unique_clear_text_apps = db.exec_fromfile("data/sql/UniqueClearTextApps.sql")

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.apps_clear_text_passwords(
            unique_clear_text_apps)
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #################################################
    ## Risky Expired Service Principal Names (SPN) ##
    #################################################

    risky_spns = db.exec_fromfile("data/sql/UniqueExpiredSPNAccounts.sql")
    spns_count = db.exec_fromfile("data/sql/TotalSPNs.sql")

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.risky_spns(
            len(risky_spns),
            spns_count[0][0])
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #######################################
    ## Hashes Found on Multiple Machines ##
    #######################################

    hashes_found_on_multiple = db.exec_fromfile("data/sql/HashesFoundOnMultiple.sql")
    total_hash_srv = 0
    total_hash_wks = 0
    total_hash_name = []

    if hashes_found_on_multiple:
        for x in range(len(hashes_found_on_multiple)):
            total_hash_srv += hashes_found_on_multiple[x][4]
            total_hash_wks += hashes_found_on_multiple[x][3]
            total_hash_name.append(hashes_found_on_multiple[x][0])
        
        unique_hash_name = set(total_hash_name)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.hashes_found_on_multiple(
            len(unique_hash_name),
            len(total_hash_name),
            total_hash_srv,
            total_hash_wks)
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    #######################################################
    ## Hashes w/ Multiple Machine Access - By %age Tiers ##
    #######################################################

    multi_machine_hashes = db.exec_fromfile("data/sql/MultipleMachineHashes.sql")

    multiMachineHashes = Metrics.multi_machine_hashes(multi_machine_hashes, all_machines_count[0][0])

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.multi_machine_accts(multiMachineHashes)
        if args.test is False:
            input("Press ENTER to continue...")
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

    # Create "required optional" argument group
    req_grp = parser.add_argument_group(title='required optional')

    # Required positional argument for database file to query against
    parser.add_argument(
        "database_file",
        help="path to the CyberArk DNA SQLite3 database file")

    # Required argument flag for domain confirmation
    req_grp.add_argument(
        "--domain",
        "-d",
        dest="domain",
        help="the AD domain name included in the scan for confirmation",
        required=True
    )

    # Required argument flag for service account regex
    req_grp.add_argument(
        "--svc-regex",
        "-s",
        dest="svc_regex",
        help="comma-delimited list of service account naming convention regex",
        required=True
    )

    # Required argument flag for admin account regex
    req_grp.add_argument(
        "--adm-regex",
        "-a",
        dest="adm_regex",
        help="comma-delimited list of admin account naming convention regex",
        required=True
    )

    # Optional argument flag for output results
    parser.add_argument(
        "--output",
        "-o",
        action="store_true",
        dest="output",
        help="output the results to the console",
        default=True
    )

    # Optional argument flag for including disabled accounts in results
    parser.add_argument(
        "--disabled",
        action="store_true",
        dest="disabled",
        help="include disabled accounts in results returned",
        default=False
    )

    # Optional argument flag for testing
    parser.add_argument(
        "--test",
        "-t",
        action="store_true",
        dest="test",
        help="for testing purposes only",
        default=False
    )

    # Optional argument flag to output current version
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
        help="shows current version information and exit")

    try:
        args = parser.parse_args()
    except:
        logger.error("Invalid argument(s) passed at initialization")
        raise

    main(args)
