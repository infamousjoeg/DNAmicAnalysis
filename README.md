# :bar_chart: DNAmic Analysis

[![Build Status](https://travis-ci.com/infamousjoeg/DNAmicAnalysis.svg?branch=master)](https://travis-ci.com/infamousjoeg/DNAmicAnalysis) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=infamousjoeg/DNAmicAnalysis&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&utm_medium=referral&utm_content=infamousjoeg/DNAmicAnalysis&utm_campaign=Badge_Coverage)

Automation for CyberArk's Discovery & Audit (DNA) reports.

## Installation

```shell
$ git clone git@github.com/infamousjoeg/DNAmicAnalysis.git
$ cd DNAmicAnalysis
$ pip install -r requirements.txt
$ ./DNAmicAnalysis.py --version
```

### Using Pipenv

```shell
$ git clone git@github.com/infamousjoeg/DNAmicAnalysis.git
$ cd DNAmicAnalysis
$ pip install pipenv
$ pipenv install
$ pipenv run ./DNAmicAnalysis --version
```

## Usage

_NOTE: Until a release is available, this is considered a BETA. In a BETA state, the `--output` argument will be default. It will not be required to be provided during this phase. Attempting to not display output will not help you in anyway.  Your attempts are futile._

![](img/cli-help.png)

### Required Paramters

* `database_file` - the SQLite3 database file should have an unaltered filename.  **This application relies on the date and time stamped in the filename for metrics.**
* `--svc-regex` - this is a quote-encapsulated, comma-delimited list of regex terms denoting a service account.  See [Example Output](#Example-Output) for an example.
* `--adm-regex` - this is a quote-encapsulated, comma-delimited list of regex terms denoting an administrator account.  See [Example Output](#Example-Output) for an example.

### Optional Parameters

* `-h, --help` - displays the available arguments for this application
* `--output` - **Enabled by default while in BETA***.  This displays the metrics to the console.
* `--disabled` - Include all disabled accounts in the metrics.  Disabled accounts are not included by default.
* `--version` - Reports the version of this application
* `--test` - Suppresses the "Press ENTER to continue" requirement of `--output` for automated testing

## Version

```shell
$ ./DNAmicAnalysis.py --version
DNAmicAnalysis.py (version 0.2.0)
```

## Example Output

```plaintext
$ ./DNAmicAnalysis.py data/test/DNA_2019-05-21_08-57-43-PM.db --svc-regex "svc, service" --adm-regex "adm, admin"
====================================================
Expired Domain Privileged IDs
----------------------------------------------------
Oldest Non-Compliant Username: Mike
Max Password Age: 546 days
----------------------------------------------------
Total Avg Password Age: 3127.00 / 8 = 390.88 days
----------------------------------------------------
Total Percent Non-Compliant: 8 / 24 = 33.33%
====================================================

Press ENTER to continue...

====================================================
Unique Expired Local Privileged IDs
----------------------------------------------------
Oldest Non-Compliant Username: shadow
Max Password Age: 514 days
----------------------------------------------------
Total Avg Password Age: 932.00 / 3 = 310.67 days
----------------------------------------------------
Total Percent Non-Compliant: 3 / 12 = 25.00%
====================================================

Press ENTER to continue...

====================================================
Expired Local Admins Total w/ Machine Addresses
----------------------------------------------------
Machine Address: client.CyberArkDemo.com
Username: shadow
----------------------------------------------------
Machine Address: epmsvr.CyberArkDemo.com
Username: LocalAdmin
----------------------------------------------------
Machine Address: components.CyberArkDemo.com
Username: Administrator
----------------------------------------------------
Total Local Accounts Non-Compliant: 3 / 12
====================================================

Press ENTER to continue...

====================================================
Local Abandoned / Leftover Accounts
----------------------------------------------------
Total Detected: 0 / 12
====================================================

Press ENTER to continue...

====================================================
Domain Abandoned / Leftover Accounts
----------------------------------------------------
Total Detected: 0 / 24
====================================================

Press ENTER to continue...

====================================================
Accounts with Multiple Machine Access
----------------------------------------------------
60-70% Access
----------------------------------------------------
Username: Administrator
Username: Contractor_1
Username: Contractor_2
Username: g_s_admin
Username: g_x_admin
Username: h_admin
Username: John_Admin
Username: Mike
Username: pta_monitor
Username: reconcile
Username: Robert
Username: rogueadmin
Username: s_admin
Username: svc_bizapp
Username: svc_mgmt
Username: svc_sched
Username: svc_sql
Username: svc_webapp
Username: u_admin
Username: Vendor_1
Username: Vendor_2
Username: x_admin
TOTAL ACCOUNTS: 22
====================================================
40-50% Access
----------------------------------------------------
Username: John
TOTAL ACCOUNTS: 1
====================================================

Press ENTER to continue...

====================================================
Unique Domain Admins
----------------------------------------------------
Total Detected: 22
----------------------------------------------------
Total Potential Service Accounts: 6
====================================================

Press ENTER to continue...

====================================================
Unique Expired Domain Admins
----------------------------------------------------
Oldest Non-Compliant Username: Administrator
Max Password Age: 398 days
----------------------------------------------------
Total Avg Password Age: 3127.0 / 8 = 390.88 days
----------------------------------------------------
Total Percent Non-Compliant: 8 / 22 = 36.36%
====================================================

Press ENTER to continue...

====================================================
Personal Accounts Running Services
----------------------------------------------------
Total Personal Accounts: 1
====================================================

Press ENTER to continue...

====================================================
Non-Admin Accounts w/ Local Admin to Systems
----------------------------------------------------
Total Non-Admin Accounts: 23
====================================================

Press ENTER to continue...

====================================================
Unique Expired Services
----------------------------------------------------
Oldest Non-Compliant Service: Mike
Max Password Age: 546 days
----------------------------------------------------
Total Avg Password Age: 935 / 2 = 467.50 days
----------------------------------------------------
Total Percent Non-Compliant: 2 / 6 = 33.33%
====================================================

Press ENTER to continue...

====================================================
Clear Text IDs
----------------------------------------------------
No Clear Text IDs found.
====================================================

Press ENTER to continue...

====================================================
Applications with Clear Text Passwords
----------------------------------------------------
No Applications with Clear Text Passwords found.
====================================================

Press ENTER to continue...

====================================================
Risky Expired Service Principal Names (SPN)
----------------------------------------------------
Total Unique Expired over Total Overall: 1 / 1
====================================================

Press ENTER to continue...

====================================================
Hashes Found on Multiple Machines
----------------------------------------------------
Total Unique Accounts over Total Found Overall: 5 / 8
----------------------------------------------------
Total Workstations Found: 0
Total Servers Found: 8
====================================================

Press ENTER to continue...

====================================================
Accounts with Multiple Machine Access
----------------------------------------------------
60-70% Access
----------------------------------------------------
Username: Administrator
Username: Contractor_1
Username: Contractor_2
Username: g_s_admin
Username: g_x_admin
Username: h_admin
Username: John_Admin
Username: Mike
Username: pta_monitor
Username: reconcile
Username: Robert
Username: rogueadmin
Username: s_admin
Username: svc_bizapp
Username: svc_mgmt
Username: svc_sched
Username: svc_sql
Username: svc_webapp
Username: u_admin
Username: Vendor_1
Username: Vendor_2
Username: x_admin
TOTAL ACCOUNTS: 22
====================================================
40-50% Access
----------------------------------------------------
Username: John
TOTAL ACCOUNTS: 1
====================================================

Press ENTER to continue...
```

## License

MIT
