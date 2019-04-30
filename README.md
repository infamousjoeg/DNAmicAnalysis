# DNAmic Analysis :bar_chart:

Automation for CyberArk's Discovery & Audit (DNA) reports.

## Installation

```shell
$ git clone git@github.com/infamousjoeg/DNAmicAnalysis.git
$ cd DNAmicAnalysis
$ pip install -r requirements.txt
$ ./DNAmicAnalysis.py --version
```

## Usage

```shell
$ ./DNAmicAnalysis.py -h
usage: DNAmicAnalysis.py [-h] [-t] [-v] database_file

CyberArk DNA report generation utility

positional arguments:
  database_file  Path to the CyberArk DNA SQLite3 database file

optional arguments:
  -h, --help     show this help message and exit
  -t, --test     For testing purposes only
  --version  Displays current version information
```

## Version

```shell
$ ./DNAmicAnalysis.py --version
DNAmicAnalysis.py (version 0.1.0)
```

## License

MIT