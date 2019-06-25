#!/usr/bin/env python3
## Automation for CyberArk's Discovery & Audit (DNA) reports. ##

import argparse
import logging

import logzero
from dnamic_analysis import Database
import dnamic_analysis.metrics as Metrics
from logzero import logger
from tests import Tests

__author__ = "Joe Garcia, CISSP"
__version__ = "0.1.0"
__license__ = "MIT"

LOGFILE = 'DNAmicAnalysis.log'

def config_logger(logfile):
    ## Configures logging of this application ##
    # Set a minimum log level
    logzero.loglevel(logging.INFO)

    # Set a logfile (all future log messages are also saved there), but disable the default stderr logging
    logzero.logfile(logfile, disableStderrLogger=True)

    # Set a custom formatter
    formatter = logging.Formatter('DNAmicAnalysis - %(asctime)-15s - %(levelname)s: %(message)s');
    logzero.formatter(formatter)


def main(args):
    ## Main entry point of the app ##

    logger.info("Arguments received: {}".format(args))

    db = Database(args.database_file)

    svc_array = args.svc_regex.replace(' ', '').split(',')

    ## Expired Domain Privileged IDs ##

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

    ## Unique Expired Local Privileged IDs ##

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

    ## Expired Local Admins Total w/ Machine Names ##

    localMaxGrouped = Metrics.local_expired_machines(localMaxSorted)
    
    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.local_expired_machines(localMaxGrouped, len(all_local_count))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ## Local Abandoned Accounts ##

    abandoned_local = db.exec_fromfile("data/sql/LocalAbandonedAccounts.sql")

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.local_abandoned(len(abandoned_local), len(all_local_count))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ## Domain Abandoned Accounts ##

    abandoned_domain = db.exec_fromfile("data/sql/DomainAbandonedAccounts.sql")

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.domain_abandoned(len(abandoned_domain), len(all_domain_count))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ## Accounts w/ Multiple Machine Access - By %age Tiers ##

    multi_machine_accts = db.exec_fromfile("data/sql/MultipleMachineAccounts.sql")
    all_machines_count = db.exec_fromfile("data/sql/TotalMachinesCount.sql")

    multiMachineAccounts = Metrics.multi_machine_accts(multi_machine_accts, all_machines_count[0][0])

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.multi_machine_accts(multiMachineAccounts)
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ## Unique Domain Admins ##

    unique_domain_admins = db.exec_fromfile("data/sql/UniqueDomainAdmins.sql")
    unique_svcacct_domain_admins = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins.sql", "svc", svc_array)
    unique_svcacct_domain_admins2 = db.exec_fromfile("data/sql/UniqueSvcDomainAdmins2.sql", "svc", svc_array)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.unique_domain_admins(unique_domain_admins, (unique_svcacct_domain_admins+unique_svcacct_domain_admins2))
        if args.test is False:
            input("Press ENTER to continue...")
        print()

    ## Unique Expired Domain Privileged IDs ##

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

    ## Personal Accounts Running Services ##

    personalAccountsRunningSvcs = db.exec_fromfile('data/sql/PersonalAccountsRunningSvcs.sql', "svc", svc_array)

    # If --output detected, make results verbose to console
    if args.output is True:
        Tests.personal_accts_running_svcs(
            len(personalAccountsRunningSvcs))
        if args.test is False:
            input("Press ENTER to continue...")
        print()


if __name__ == "__main__":
    ## This is executed when run from the command line ##

    # Configure logging
    config_logger(LOGFILE)
    logger.info("Application initialized successfully")

    # Create argument parsing object
    parser = argparse.ArgumentParser(description="CyberArk DNA report generation utility")

    # Create "required optional" argument group
    req_grp = parser.add_argument_group(title='required optional')

    # Required positional argument for database file to query against
    parser.add_argument(
        "database_file",
        help="path to the CyberArk DNA SQLite3 database file")

    # Required argument flag for service account regex
    req_grp.add_argument(
        "--svc-regex",
        dest="svc_regex",
        help="comma-delimited list of service account naming convention regex",
        default=True,
        required=True
    )

    # Optional argument flag for output results
    parser.add_argument(
        "--output",
        action="store_true",
        dest="output",
        help="output the results to the console",
        default=True
    )

    # Optional argument flag for testing
    parser.add_argument(
        "--test",
        action="store_true",
        dest="test",
        help="for testing purposes only",
        default=False
    )

    # Optional argument flag to output current version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
        help="shows current version information and exit")

    try:
        args = parser.parse_args()
    except:
        logger.error("Invalid argument(s) passed at initialization")
        raise

    main(args)
