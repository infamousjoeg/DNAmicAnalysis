# DNAmic Analysis :bar_chart:

Automation for CyberArk's Discovery & Audit (DNA) reports.

## Usage

```shell
$ ./DNAmicAnalysis.py -h
usage: DNAmicAnalysis.py [-h] [--debug] [-v] database_file

CyberArk DNA report generation utility

positional arguments:
  database_file  Path to the CyberArk DNA SQLite3 database file

optional arguments:
  -h, --help     show this help message and exit
  --debug        Sets DEBUG as the minimum log level [Default: INFO]
  -v, --version  Displays current version information
```

## Version

```shell
$ ./DNAmicAnalysis.py -v
DNAmicAnalysis.py (version 0.1.0)
```

## License

MIT