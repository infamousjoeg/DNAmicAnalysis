import logzero
from logzero import logger


def domain_max(sqlresults):
    domain_max_sorted = sorted(sqlresults,
                                key=lambda sqlresults: sqlresults[2],
                                reverse=True)
    return domain_max_sorted


def domain_avg(sqlresults):
    domain_avg_values = [x[3] for x in sqlresults]
    domain_avg_overall = sum(domain_avg_values) / len(domain_avg_values)
    logger.info("Calculated Overall Average Password Age for Expired Domain Accounts using: {} / {}".format(
        sum(domain_avg_values),
        len(domain_avg_values)))
    return sum(domain_avg_values), len(domain_avg_values), domain_avg_overall


def domain_percent(sqlresults, sqlcount, domain_max_sorted):
    domain_percent_overall = len(domain_max_sorted) / len(sqlcount)
    logger.info("Calulated Percentage Overall Non-Compliant Expired Domain Accounts using: {} / {}".format(
        len(domain_max_sorted),
        len(sqlcount)))
    return len(domain_max_sorted), len(sqlcount), domain_percent_overall


def local_max(sqlresults):
    local_max_sorted = sorted(sqlresults,
                                key=lambda expired_local: sqlresults[2],
                                reverse=False)
    return local_max_sorted


def local_avg(sqlresults):
    local_avg_values = [x[4] for x in sqlresults]
    local_avg_overall = sum(local_avg_values) / len(local_avg_values)
    logger.info("Calculated Overall Average Password Age for Expired Local Accounts using: {} / {}".format(
        sum(local_avg_values),
        len(local_avg_values)))
    return sum(local_avg_values), len(local_avg_values), local_avg_overall


def local_percent(sqlresults, sqlcount, local_max_sorted):
    local_percent_overall = len(local_max_sorted) / len(sqlcount)
    logger.info("Calulated Percentage Overall Non-Compliant Expired Local Accounts using: {} / {}".format(
        len(local_max_sorted),
        len(sqlcount)))
    return len(local_max_sorted), len(sqlcount), local_percent_overall