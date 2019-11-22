# :bar_chart: DNAmic Analysis <!-- omit in toc -->

[![](https://github.com/infamousjoeg/DNAmicAnalysis/workflows/DNAmic%20Analysis%20Windows%20Test/badge.svg)](https://github.com/infamousjoeg/DNAmicAnalysis/actions?workflow=DNAmic+Analysis+Windows+Test) [![](https://github.com/infamousjoeg/DNAmicAnalysis/workflows/DNAmic%20Analysis%20Ubuntu%20Test/badge.svg)](https://github.com/infamousjoeg/DNAmicAnalysis/actions?workflow=DNAmic+Analysis+Ubuntu+Test) [![](https://github.com/infamousjoeg/DNAmicAnalysis/workflows/DNAmic%20Analysis%20MacOS%20Test/badge.svg)](https://github.com/infamousjoeg/DNAmicAnalysis/actions?workflow=DNAmic+Analysis+MacOS+Test)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=infamousjoeg/DNAmicAnalysis&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&utm_medium=referral&utm_content=infamousjoeg/DNAmicAnalysis&utm_campaign=Badge_Coverage) [![GitHub issues](https://img.shields.io/github/issues/infamousjoeg/DNAmicAnalysis)](https://github.com/infamousjoeg/DNAmicAnalysis/issues) [![GitHub license](https://img.shields.io/github/license/infamousjoeg/DNAmicAnalysis)](https://github.com/infamousjoeg/DNAmicAnalysis/blob/master/LICENSE)

Automation for CyberArk's Discovery & Audit (DNA) deep dive analysis reports.

## Table of Contents <!-- omit in toc -->

- [About](#about)
  - [Project Info](#project-info)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
    - [RHEL/CentOS](#rhelcentos)
    - [Ubuntu/Debian](#ubuntudebian)
  - [MacOS](#macos)
- [Pre-Requisites](#pre-requisites)
- [Usage](#usage)
  - [Output](#output)
- [Version](#version)
- [Example Output](#example-output)
  - [Video Example](#video-example)
  - [Plaintext Example](#plaintext-example)

## About

This project is for the PAS Programs Office of [CyberArk](https://cyberark.com).  It is open-sourced for anyone to utilize, however it is _strongly recommended_ for customers to reach out to your CyberArk Account Team or people without CyberArk to reach out via [CyberArk.com](https://cyberark.com) for a proper deep dive analysis and presentation.

### Project Info

DNAmic Analysis is an application written in Python 3 for OS independence.

The metrics presented from this application were chosen based on deep dive analysis presentations the PAS Programs Office conducts on a frequent basis.  If you have a metric you'd like added, please feel free to add it to this codebase by opening a Pull Request to have your contribution added.

The metrics reported in this application are based on SQL queries ran on the DNA SQLite3 database produced during its scans.  An unmodified DNA SQLite3 database is required for this application to work.  If your DNA SQLite3 database filename is modified, you will need to update the configuration file to accept a manual scan date & time (explained in more detail below).

## Installation

### Windows

1. Download & install the latest version of [Python 3 for Windows executable installer](https://www.python.org/downloads/).
2. Download the source code zip of the [latest DNAmic Analysis release](https://github.com/infamousjoeg/DNAmicAnalysis/releases).
3. Unpack the source code zip file and start a command prompt from within the directory.

   **Note:** _Holding `Shift` while right-clicking will bring up a context menu with the option "Open Command Prompt here"._
4. `pip install -r requirements.txt`

   ![](img/windows-pipinstall.png)

5. Run the application with valid arguments as outlined in the [Usage](#usage) section below. 

   ![](img/windows-runpy.png)

### Linux

#### RHEL/CentOS

1. Install EPEL Release repository.
   
   `$ sudo yum install epel-release -y`

2. Install Python 3.6 from EPEL.
   
   `$ sudo yum install python36 -y`

3. Upgrade PIP to latest version.
   
   `$ sudo python3 -m pip install --upgrade pip`
   
4. Clone GitHub repository for DNAmic Analysis.
   
   `$ git clone https://github.com/infamousjoeg/DNAmicAnalysis.git`
   
5. Change directory to newly cloned GitHub repo directory.
   
   `$ cd DNAmicAnalysis/`
   
6. Install requirements.txt dependencies. 
   
   `$ sudo python3 -m pip install -r requirements.txt`

7. Run DNAmicAnalysis with proper arguments as outlined in the [Usage](#usage) section below.
   
   `$ python3 DNAmicAnalysis.py template_config.yml`

#### Ubuntu/Debian

1. Install Python 3.6.
   
   `$ sudo apt install python3.6 -y`

2. Install PIP for Python 3.6.
   
   `$ sudo python36 -m ensurepip`

3. Upgrade PIP to latest version.
   
   `$ python36 -m pip install --upgrade pip`
   
4. Clone GitHub repository for DNAmic Analysis.
   
   `$ git clone https://github.com/infamousjoeg/DNAmicAnalysis.git`
   
5. Change directory to newly cloned GitHub repo directory.
   
   `$ cd DNAmicAnalysis/`
   
6. Install requirements.txt dependencies. 
   
   `$ python36 -m pip install -r requirements.txt`

7. Run DNAmicAnalysis with proper arguments as outlined in the [Usage](#usage) section below.
   
   `$ python36 DNAmicAnalysis.py template_config.yml`

### MacOS

1. Install Python 3.7.4.

   `$ brew install python`

2. Clone GitHub repository for DNAmic Analysis.
   
   `$ git clone https://github.com/infamousjoeg/DNAmicAnalysis.git`
   
3. Change directory to newly cloned GitHub repo directory.
   
   `$ cd DNAmicAnalysis/`
   
4. Install requirements.txt dependencies. 
   
   `$ pip install -r requirements.txt`

5. Run DNAmicAnalysis with proper arguments as outlined in the [Usage](#usage) section below.
   
   `$ ./DNAmicAnalysis.py template_config.yml`

## Pre-Requisites

* [Python 3.x.x](https://www.python.org/downloads/)
* Application dependencies installed
  * `$ pip3 install -r requirements.txt`
* A DNA database file from a CyberArk DNA scan
  * Please do not obfuscate the database file
  * In order to save the SQLite3 database, adjust the following key/value pair:
    * Open `dna.exe.config` for editing:

      `DeleteDB=no`

## Usage

* Copy [config/template_config.yml](config/template_config.yml) and rename it to something like `customer_config.yml`.
* Update the values within the YAML config file to match those given to you by the customer for the scan analysis.
* Use `^` as a wildcard when declaring regex in the `account_regex` section.

```yaml
---
# path to where the DNA database file is located
database_file: /Users/joegarcia/Git/infamousjoeg/DNAmicAnalysis/data/test/DNA_2019-05-21_08-57-43-PM.db
# domain name of one scanned domain that can be detected
domain: cyberarkdemo.com
# privileged account patterns to match
account_regex:
  service_account:
    - svc^
    - ^service
  admin_account:
    - adm^
    - ^admin
# yes or no: whether to output metrics to console
console_output: yes
# yes or no: whether to include disabled accounts in metrics
include_disabled_accts: no
# yes or no: activate test mode... do not adjust unless you
  # know what you are doing
test_mode: yes
# DNA scan date & time settings
scan_datetime:
  # yes or no: override the timestamped DNA.db filename with the manual_scan_datetime
  override: yes
  # Use 24-hour format for the time e.g. 2019-05-21 20:57:43 for 08:57:43 PM
  manual_scan_datetime: "2019-05-21 20:57:43"
```

**Windows**

`> python.exe DNAmicAnalysis.py template_config.yml`

**UNIX or MacOS**

`$ ./DNAmicAnalysis.py template_config.yml`

### Output

If the configuration file has the key `console_output` set to `yes`, the metrics will be output to STDOUT on the console.  In addition, an Excel workbook in .xls format will be created and will contain the bulk data of the metrics' output.  The file is created in the same directory that the `DNAmicAnalysis.py` executable is run from.

The format for the Excel filename is `DNAmicAnalysis_<domain>_<date>_<time>.xls`.

## Version

**Windows**
```shell
> python.exe DNAmicAnalysis.py --version
DNAmicAnalysis (version 0.6.0-beta.5)
```

**UNIX or MacOS**
```shell
$ ./DNAmicAnalysis --version
DNAmicAnalysis (version 0.6.0-beta.5)
```

## Example Output

### Video Example

[![asciicast](https://asciinema.org/a/268844.svg)](https://asciinema.org/a/268844)

### Plaintext Example

```plaintext
====================================================
Found cyberarkdemo.com in the provided DNA scan database.
Press ENTER to continue...
====================================================

====================================================
Expired Domain Privileged IDs
----------------------------------------------------
Oldest Non-Compliant Username: Mike
Max Password Age: 546 days (1.5 years)
----------------------------------------------------
Total Avg Password Age: 3127.00 / 8 = 390.88 days (1.1 years)
----------------------------------------------------
Total Percent Non-Compliant: 8 / 24 = 33.33%
====================================================


====================================================
Unique Expired Local Privileged IDs
----------------------------------------------------
Oldest Non-Compliant Username: shadow
Max Password Age: 514 days (1.4 years)
----------------------------------------------------
Total Avg Password Age: 932.00 / 3 = 310.67 days (0.9 years)
----------------------------------------------------
Total Percent Non-Compliant: 3 / 12 = 25.00%
----------------------------------------------------
Total Unique Local Privileged IDs: 12
Total Unique Local Privileged ID Names: 10
====================================================


====================================================
Expired Local Admins Total w/ Machine Addresses
----------------------------------------------------
Username: shadow
Machine Address: client.CyberArkDemo.com
Total Machines for User: 1
----------------------------------------------------
Username: localadmin
Machine Address: epmsvr.CyberArkDemo.com
Total Machines for User: 1
----------------------------------------------------
Username: administrator
Machine Address: components.CyberArkDemo.com
Total Machines for User: 1
----------------------------------------------------
Total Local Accounts Non-Compliant: 3
====================================================


====================================================
Local Abandoned / Leftover Accounts
----------------------------------------------------
Total Detected: 0 / 9
====================================================


====================================================
Domain Abandoned / Leftover Accounts
----------------------------------------------------
Total Detected: 0 / 24
====================================================


====================================================
Accounts with Multiple Machine Access
----------------------------------------------------
> 95% Access
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


====================================================
Unique Domain Admins
----------------------------------------------------
Total Detected: 22
----------------------------------------------------
Total Potential Service Accounts: 6
Username: svc_webapp
Username: svc_sched
Username: svc_bizapp
Username: svc_mgmt
Username: svc_sql
Username: Mike
====================================================


====================================================
Unique Expired Domain Admins
----------------------------------------------------
Oldest Non-Compliant Username: Administrator
Max Password Age: 398 days (1.1 years)
----------------------------------------------------
Total Avg Password Age: 3127.0 / 8 = 390.88 days (1.1 years)
----------------------------------------------------
Total Percent Non-Compliant: 8 / 22 = 36.36%
----------------------------------------------------
Username: Administrator
Username: h_admin
Username: Mike
Username: Robert
Username: rogueadmin
Username: svc_mgmt
Username: svc_sql
Username: Vendor_1
====================================================


====================================================
Personal Accounts Running Services
----------------------------------------------------
Total Personal Accounts: 1
====================================================


====================================================
Non-Admin Accounts w/ Local Admin to Systems
----------------------------------------------------
Total Non-Admin Accounts: 16
====================================================


====================================================
Unique Expired Services *(Check against manual report)*
----------------------------------------------------
Oldest Non-Compliant Service: Mike
Max Password Age: 546 days (1.5 years)
----------------------------------------------------
Total Avg Password Age: 935 / 2 = 467.50 days (1.3 years)
----------------------------------------------------
Total Percent Non-Compliant: 2 / 6 = 33.33%
====================================================


====================================================
Clear Text IDs
----------------------------------------------------
No Clear Text IDs found.
====================================================


====================================================
Applications with Clear Text Passwords
----------------------------------------------------
No Applications with Clear Text Passwords found.
====================================================


====================================================
Risky Expired Service Principal Names (SPN)
----------------------------------------------------
Total Unique Expired over Total Overall: 2 / 3
====================================================


====================================================
Hashes Found on Multiple Machines
----------------------------------------------------
Total Unique Accounts: 5
Total Administrative Hashes Found: 5
----------------------------------------------------
Total on Workstations: 0
Total on Servers: 5
----------------------------------------------------
Total Admin Hashes on Workstations: 0
Total Admin Hashes on Servers: 5
----------------------------------------------------
Username: Mike
Username: svc_bizapp
Username: svc_sched
Username: svc_sql
Username: svc_webapp
====================================================


====================================================
Accounts with Multiple Machine Hashes
----------------------------------------------------
> 95% Access
----------------------------------------------------
Username: Mike
Username: svc_bizapp
Username: svc_sched
Username: svc_sql
Username: svc_webapp
TOTAL ACCOUNTS: 5
====================================================
```
