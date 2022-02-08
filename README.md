# :bar_chart: DNAmic Analysis <!-- omit in toc -->

**PROJECT IS NO LONGER BEING ACTIVELY DEVELOPED OR SUPPORTED**

[![](https://github.com/infamousjoeg/DNAmicAnalysis/workflows/DNAmic%20Analysis%20Lint%20%26%20OS%20Tests/badge.svg)](https://github.com/infamousjoeg/DNAmicAnalysis/actions?workflow=DNAmic+Analysis+Lint+%26+OS+Tests)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=infamousjoeg/DNAmicAnalysis&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&utm_medium=referral&utm_content=infamousjoeg/DNAmicAnalysis&utm_campaign=Badge_Coverage) [![GitHub issues](https://img.shields.io/github/issues/infamousjoeg/DNAmicAnalysis)](https://github.com/infamousjoeg/DNAmicAnalysis/issues) [![GitHub license](https://img.shields.io/github/license/infamousjoeg/DNAmicAnalysis)](https://github.com/infamousjoeg/DNAmicAnalysis/blob/main/LICENSE)

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

5. Run the application with valid arguments as outlined in the [Usage](#usage) section below. 

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
# path to where the DNA database file(s) is located
# use ONLY forward slashes - the application will correct for Windows
# list as many DNA database files as you'd like reported
database_files:
  - data/test/DNA_2019-05-21_08-57-43-PM.db
  - data/test/DNA_2020-09-28_05-29-30-PM.db
# domain name of one scanned domain that can be detected
domain: cyberarkdemo.com
# privileged account patterns to match
# to include a wildcard, use ^
# e.g. - adm^ (this will include all usernames STARTING with adm)
account_regex:
  service_account:
    - svc^
    - ^service
  admin_account:
    - adm^
    - ^admin
# OS Platform: windows or unix
platform: windows
# account expiration period in days to calculate compliance
expiration_days: 90
# yes or no: whether to include disabled accounts in metrics
include_disabled_accts: no
# yes or no: activate test mode... do not adjust unless you
  # know what you are doing
test_mode: no
# DNA scan date & time settings
scan_datetime:
  # yes or no: override the timestamped DNA.db filename with the manual_scan_datetime
  override: no
  # Use 24-hour format for the time e.g. 2019-05-21 20:57:43 for 08:57:43 PM
  # YYYY-MM-DD HH:MM:SS
  manual_scan_datetime: "2019-05-21 20:57:43"
```

**Windows**

`> python.exe DNAmicAnalysis.py template_config.yml`

**UNIX or MacOS**

`$ ./DNAmicAnalysis.py template_config.yml`

### Output

An Excel workbook in .xlsx format will be created and will contain the bulk data of the metrics' output.  The file is created in a `reports/` directory that the `DNAmicAnalysis.py` executable is run from.

The format for the Excel filename is `DNAmicAnalysis_<domain>_<date>_<time>.xlsx`.

## Version

**Windows**
```shell
> python.exe DNAmicAnalysis.py --version
DNAmicAnalysis (version 3.0.1)
```

**UNIX or MacOS**
```shell
$ ./DNAmicAnalysis --version
DNAmicAnalysis (version 3.0.1)
```
