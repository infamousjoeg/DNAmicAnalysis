from logzero import logger


class Metrics(object):

    ##########################
    ## WINDOWS SCAN METRICS ##
    ##########################

    def domain_max(sqlresults):
        domain_max_sorted = sorted(sqlresults,
                                    key=lambda sqlresults: sqlresults[3],
                                    reverse=True)
        logger.info("Ordered Non-Compliant Expired Domain Accounts ascending by Username")
        return domain_max_sorted


    def domain_avg(sqlresults):
        domain_avg_values = [x[3] for x in sqlresults]
        domain_avg_overall = sum(domain_avg_values) / len(domain_avg_values)
        logger.info("Calculated Overall Average Password Age for Expired Domain \
            Accounts using: {} / {}".format(
                sum(domain_avg_values),
                len(domain_avg_values)))
        return sum(domain_avg_values), len(domain_avg_values), domain_avg_overall


    @classmethod
    def domain_percent(cls, sqlresults, sqlcount, domain_max_sorted):
        domain_percent_overall = len(domain_max_sorted) / len(sqlcount)
        logger.info("Calulated Percentage Overall Non-Compliant Expired Domain \
            Accounts using: {} / {}".format(
                len(domain_max_sorted),
                len(sqlcount)))
        return len(domain_max_sorted), len(sqlcount), domain_percent_overall


    def local_max(sqlresults):
        local_max_sorted = sorted(sqlresults,
                                    key=lambda sqlresults: sqlresults[4],
                                    reverse=True)
        logger.info("Ordered Non-Compliant Expired Local Accounts ascending by Username")
        return local_max_sorted


    def local_avg(sqlresults):
        local_avg_values = [x[4] for x in sqlresults]
        local_avg_overall = sum(local_avg_values) / len(local_avg_values)
        logger.info("Calculated Overall Average Password Age for Expired Local \
            Accounts using: {} / {}".format(
                sum(local_avg_values),
                len(local_avg_values)))
        return sum(local_avg_values), len(local_avg_values), local_avg_overall


    @classmethod
    def local_percent(cls, sqlresults, sqlcount, local_max_sorted):
        local_percent_overall = len(local_max_sorted) / len(sqlcount)
        logger.info("Calulated Percentage Overall Non-Compliant Expired Local \
            Accounts using: {} / {}".format(
                len(local_max_sorted),
                len(sqlcount)))
        return len(local_max_sorted), len(sqlcount), local_percent_overall


    def password_age(sqlresults):
        # Declare variables
        avgPassword = 0
        count = 0
        output = {}
        return_dict = {}

        if not sqlresults:
            return
        elif len(sqlresults[0]) == 2:
            # Create a dictionary with a key of account and list of values of every password age
            for account,passwordage in sqlresults:
                if account in output:
                        output[account].append((passwordage))
                else:
                        output[account] = [(passwordage)]
        elif len(sqlresults[0]) == 3:
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,passwordage in sqlresults:
                if account in output:
                        output[account].append((passwordage))
                else:
                        output[account] = [(passwordage)]
        elif len(sqlresults[0]) == 4:
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,passwordage in sqlresults:
                if account in output:
                        output[account].append((passwordage))
                else:
                        output[account] = [(passwordage)]
        elif len(sqlresults[0]) == 5:
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,_,passwordage in sqlresults:
                if account in output:
                        output[account].append((passwordage))
                else:
                        output[account] = [(passwordage)]
        elif len(sqlresults[0]) == 6:
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,_,_,passwordage in sqlresults:
                if account in output:
                        output[account].append((passwordage))
                else:
                        output[account] = [(passwordage)]
        elif len(sqlresults[0]) == 7:
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,_,_,_,passwordage in sqlresults:
                if account in output:
                        output[account].append((passwordage))
                else:
                        output[account] = [(passwordage)]
        elif len(sqlresults[0]) == 8:
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,_,_,_,_,passwordage in sqlresults:
                if account in output:
                        output[account].append((passwordage))
                else:
                        output[account] = [(passwordage)]

        # Loop through created dict and average password age
        for account in output:
            for result in output[account]:
                if result is not None:
                    avgPassword += result
                count += 1
            return_dict[account] = avgPassword//len(output[account])
            avgPassword = 0
            count = 0
        
        return return_dict


    def local_expired_machines(local_max_sorted):
        # Take localMaxSorted first 2 values in each row and add to var
        local_max_pruned = [metric[0:2] for metric in local_max_sorted]
        # Create blank set
        local_max_grouped = {}
        # Group by account and add to set previously created
        for account, machine in local_max_pruned:
            if account in local_max_grouped:
                local_max_grouped[account].append((machine))
            else:
                local_max_grouped[account] = [(machine)]
        logger.info("Grouped Expired Local Admins Total w/ Machine Names by Username")
        return local_max_grouped


    def multi_machine_accts(sqlresults, sqlcount):
        percent95 = []; percent90 = []; percent80 = []; percent70 = []; percent60 = []
        percent50 = []; percent40 = []; percent30 = []; percent20 = []; percent10 = []
        percent0 = []
        for username in sqlresults:
            if (username[1] / sqlcount) >= 0.95:
                percent95.append(username[0])
            if (username[1] / sqlcount) >= 0.90 and (username[1] / sqlcount) < 0.95:
                percent90.append(username[0])
            if (username[1] / sqlcount) >= 0.80 and (username[1] / sqlcount) < 0.90:
                percent80.append(username[0])
            if (username[1] / sqlcount) >= 0.70 and (username[1] / sqlcount) < 0.80:
                percent70.append(username[0])
            if (username[1] / sqlcount) >= 0.60 and (username[1] / sqlcount) < 0.70:
                percent60.append(username[0])
            if (username[1] / sqlcount) >= 0.50 and (username[1] / sqlcount) < 0.60:
                percent50.append(username[0])
            if (username[1] / sqlcount) >= 0.40 and (username[1] / sqlcount) < 0.50:
                percent40.append(username[0])
            if (username[1] / sqlcount) >= 0.30 and (username[1] / sqlcount) < 0.40:
                percent30.append(username[0])
            if (username[1] / sqlcount) >= 0.20 and (username[1] / sqlcount) < 0.30:
                percent20.append(username[0])
            if (username[1] / sqlcount) >= 0.10 and (username[1] / sqlcount) < 0.20:
                percent10.append(username[0])
            if (username[1] / sqlcount) < 0.10:
                percent0.append(username[0])
        logger.info("Grouped Accounts w/ Multiple Machine Access by Percentage Tiers")
        return percent95, percent90, percent80, percent70, \
            percent60, percent50, percent40, percent30, \
            percent20, percent10, percent0


    def unique_domain_max(sqlresults):
            unique_domain_max_sorted = sorted(sqlresults,
                                        key=lambda sqlresults: sqlresults[3],
                                        reverse=True)
            logger.info("Ordered Non-Compliant Domain Admins ascending by Username")
            return unique_domain_max_sorted


    def unique_domain_avg(sqlresults):
        unique_domain_avg_values = [x[5] for x in sqlresults]
        unique_domain_avg_overall = sum(unique_domain_avg_values) / len(unique_domain_avg_values)
        logger.info("Calculated Overall Average Password Age for Unique Expired Domain \
            Admins using: {} / {}".format(
                sum(unique_domain_avg_values),
                len(unique_domain_avg_values)))
        return sum(unique_domain_avg_values), len(unique_domain_avg_values), \
            unique_domain_avg_overall


    @classmethod
    def unique_domain_percent(cls, sqlresults, sqlcount, unique_domain_max_sorted):
        unique_domain_percent_overall = len(unique_domain_max_sorted) / sqlcount
        logger.info("Calulated Percentage Overall Non-Compliant Expired Domain Admins \
            using: {} / {}".format(
                len(unique_domain_max_sorted),
                sqlcount))
        return len(unique_domain_max_sorted), sqlcount, unique_domain_percent_overall


    def unique_svc_max(sqlresults):
        unique_svc_max_sorted = sorted(sqlresults,
                                    key=lambda sqlresults: sqlresults[4],
                                    reverse=True)
        logger.info("Ordered Expired Services ascending by Service Name")
        return unique_svc_max_sorted


    def unique_svc_avg(sqlresults):
        unique_svc_avg_values = [x[4] for x in sqlresults]
        unique_svc_avg_overall = sum(unique_svc_avg_values) / len(unique_svc_avg_values)
        logger.info("Calculated Overall Average Password Age for Unique Expired Services \
            using: {} / {}".format(
                sum(unique_svc_avg_values),
                len(unique_svc_avg_values)))
        return sum(unique_svc_avg_values), len(unique_svc_avg_values), unique_svc_avg_overall


    @classmethod
    def unique_svc_percent(cls, sqlresults, sqlcount, unique_svc_count):
        unique_svc_percent_overall = unique_svc_count / sqlcount
        logger.info("Calulated Percentage Overall Expired Service using: {} / {}".format(
                unique_svc_count,
                sqlcount))
        return unique_svc_count, sqlcount, unique_svc_percent_overall


    def multi_machine_hashes(sqlresults, sqlcount):
        percent95 = []; percent90 = []; percent80 = []; percent70 = []; percent60 = []
        percent50 = []; percent40 = []; percent30 = []; percent20 = []; percent10 = []
        percent0 = []
        for username in sqlresults:
            if (username[1] / sqlcount) >= 0.95:
                percent95.append(username[0])
            if (username[1] / sqlcount) >= 0.90 and (username[1] / sqlcount) < 0.95:
                percent90.append(username[0])
            if (username[1] / sqlcount) >= 0.80 and (username[1] / sqlcount) < 0.90:
                percent80.append(username[0])
            if (username[1] / sqlcount) >= 0.70 and (username[1] / sqlcount) < 0.80:
                percent70.append(username[0])
            if (username[1] / sqlcount) >= 0.60 and (username[1] / sqlcount) < 0.70:
                percent60.append(username[0])
            if (username[1] / sqlcount) >= 0.50 and (username[1] / sqlcount) < 0.60:
                percent50.append(username[0])
            if (username[1] / sqlcount) >= 0.40 and (username[1] / sqlcount) < 0.50:
                percent40.append(username[0])
            if (username[1] / sqlcount) >= 0.30 and (username[1] / sqlcount) < 0.40:
                percent30.append(username[0])
            if (username[1] / sqlcount) >= 0.20 and (username[1] / sqlcount) < 0.30:
                percent20.append(username[0])
            if (username[1] / sqlcount) >= 0.10 and (username[1] / sqlcount) < 0.20:
                percent10.append(username[0])
            if (username[1] / sqlcount) < 0.10:
                percent0.append(username[0])
        logger.info("Grouped Accounts w/ Multiple Machine Hashes by Percentage Tiers")
        return percent95, percent90, percent80, percent70, \
            percent60, percent50, percent40, percent30, \
            percent20, percent10, percent0

    def number_of_machines(sqlresults, metric_name):
        # Declare variables
        output = dict()

        if not sqlresults:
            return
        elif metric_name == 'Unique Domain Admins' or metric_name == 'Personal Accounts Running Services' or metric_name == 'Risky Expired Service Principal Names':
            # Create a dictionary with a key of account and list of values of every password age
            for account,num_machines,_ in sqlresults:
                if account in output:
                        output[account].append((num_machines))
                else:
                        output[account] = [(num_machines)]
        elif metric_name == 'Expired Domain Privileged IDs' or metric_name == 'Accounts w Multiple Machine Access By Percentage Tiers' or metric_name == 'Non-Domain Admin Accounts w Multiple Machine Access By Percentage Tiers' or metric_name == 'Domain Admin Accounts w Multiple Machine Access By Percentage Tiers' or metric_name == 'Non-adm Accounts w Local Admin Rights on Systems':
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,num_machines,_ in sqlresults:
                if account in output:
                        output[account].append((num_machines))
                else:
                        output[account] = [(num_machines)]
        elif metric_name == 'Unique Expired Local Privileged IDs' or metric_name == 'Domain Abandoned Accounts' or metric_name == 'Unique Expired Service Accounts' or metric_name == 'Account Hashes that Expose Multiple Machines':
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,num_machines,_ in sqlresults:
                if account in output:
                        output[account].append((num_machines))
                else:
                        output[account] = [(num_machines)]
        elif metric_name == 'Unique Expired Domain Privileged IDs' or metric_name == 'Local Abandoned Accounts':
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,_,num_machines,_ in sqlresults:
                if account in output:
                        output[account].append((num_machines))
                else:
                        output[account] = [(num_machines)]
        elif metric_name == 'Hashes Found on Multiple Machines':
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,_,_,_,num_machines,_ in sqlresults:
                if account in output:
                        output[account].append((num_machines))
                else:
                        output[account] = [(num_machines)]
        
        return output


    #######################
    ## UNIX SCAN METRICS ##
    #######################

    def unix_number_of_machines(sqlresults, metric_name):
        # Declare variables
        output = dict()

        if not sqlresults:
            return
        elif metric_name == 'Expired Privileged Domain ID Passwords' or metric_name == 'Expired Privileged Local ID Passwords' or metric_name == 'Abandoned Local Accounts' or metric_name == 'Machines w/ Expired Root Public SSH Keys':
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,num_machines,_ in sqlresults:
                if account in output:
                        output[account].append((num_machines))
                else:
                        output[account] = [(num_machines)]
        elif metric_name == 'Abandoned Domain Accounts':
            # Create a dictionary with a key of account and list of values of every password age
            for account,_,_,num_machines,_ in sqlresults:
                if account in output:
                        output[account].append((num_machines))
                else:
                        output[account] = [(num_machines)]
        
        return output


    def unix_domain_max(sqlresults):
        u_domain_max_sorted = sorted(sqlresults,
                                    key=lambda sqlresults: sqlresults[3],
                                    reverse=True)
        logger.info("Ordered Non-Compliant Expired Domain Passwords ascending by Username")
        return u_domain_max_sorted


    def unix_domain_avg(sqlresults):
        u_domain_avg_values = [x[3] for x in sqlresults]
        u_domain_avg_overall = sum(u_domain_avg_values) / len(u_domain_avg_values)
        logger.info("Calculated Overall Average Password Age for Expired Domain \
            Passwords using: {} / {}".format(
                sum(u_domain_avg_values),
                len(u_domain_avg_values)))
        return sum(u_domain_avg_values), len(u_domain_avg_values), u_domain_avg_overall


    @classmethod
    def unix_domain_percent(cls, sqlresults, sqlcount, domain_max_sorted):
        u_domain_percent_overall = len(domain_max_sorted) / len(sqlcount)
        logger.info("Calulated Percentage Overall Non-Compliant Expired Domain \
            Passwords using: {} / {}".format(
                len(domain_max_sorted),
                len(sqlcount)))
        return len(domain_max_sorted), len(sqlcount), u_domain_percent_overall


    def unix_local_max(sqlresults):
        u_local_max_sorted = sorted(sqlresults,
                                    key=lambda sqlresults: sqlresults[3],
                                    reverse=True)
        logger.info("Ordered Non-Compliant Expired Local Passwords ascending by Username")
        return u_local_max_sorted


    def unix_local_avg(sqlresults):
        u_local_avg_values = [x[3] for x in sqlresults]
        u_local_avg_overall = sum(u_local_avg_values) / len(u_local_avg_values)
        logger.info("Calculated Overall Average Password Age for Expired Local \
            Passwords using: {} / {}".format(
                sum(u_local_avg_values),
                len(u_local_avg_values)))
        return sum(u_local_avg_values), len(u_local_avg_values), u_local_avg_overall


    @classmethod
    def unix_local_percent(cls, sqlresults, sqlcount, local_max_sorted):
        u_local_percent_overall = len(local_max_sorted) / len(sqlcount)
        logger.info("Calulated Percentage Overall Non-Compliant Expired Local \
            Passwords using: {} / {}".format(
                len(local_max_sorted),
                len(sqlcount)))
        return len(local_max_sorted), len(sqlcount), u_local_percent_overall