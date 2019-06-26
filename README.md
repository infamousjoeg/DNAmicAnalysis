# :bar_chart: DNAmic Analysis

[![Build Status](https://travis-ci.com/infamousjoeg/DNAmicAnalysis.svg?branch=master)](https://travis-ci.com/infamousjoeg/DNAmicAnalysis) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=infamousjoeg/DNAmicAnalysis&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c3c0f19291884a5fb58199644618b420)](https://www.codacy.com/app/infamousjoeg/DNAmicAnalysis?utm_source=github.com&utm_medium=referral&utm_content=infamousjoeg/DNAmicAnalysis&utm_campaign=Badge_Coverage)

Automation for CyberArk's Discovery & Audit (DNA) reports.

## Installation

```shell
git clone git@github.com/infamousjoeg/DNAmicAnalysis.git
cd DNAmicAnalysis
pip install -r requirements.txt
./DNAmicAnalysis.py --version
```

## Usage

_NOTE: Until a release is available, this is considered a BETA. In a BETA state, the `--output` argument will be default. It will not be required to be provided during this phase. Not displaying output will not help you in anyway._

```shell
$ ./DNAmicAnalysis.py -h
usage: DNAmicAnalysis.py [-h] --svc-regex SVC_REGEX [--output] [--test]
                         [--version]
                         database_file

CyberArk DNA report generation utility

positional arguments:
  database_file         path to the CyberArk DNA SQLite3 database file

optional arguments:
  -h, --help            show this help message and exit
  --output              output the results to the console
  --test                for testing purposes only
  --version             shows current version information and exit

required optional:
  --svc-regex SVC_REGEX
                        comma-delimited list of service account naming
                        convention regex
```

## Version

```shell
$ ./DNAmicAnalysis.py --version
DNAmicAnalysis.py (version 0.1.0)
```

## Example Output

![](img/output.png)

## License

MIT
