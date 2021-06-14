# Introduction

### Welcome!

First off, thank you for considering contributing to DNAmic Analysis. It's people like you that make DNAmic Analysis such a great tool.

### Why am I reading this?

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

### Contributions we are accepting

DNAmic Analysis is an open source project and we love to receive contributions from our community — you! There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into DNAmic Analysis itself.

### Contributions we are NOT looking for

Please, don't use the issue tracker for support questions. If you have support issues, reach out to your manager to be connected with a DNAmic SME.

# Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
    - [Welcome!](#welcome)
    - [Why am I reading this?](#why-am-i-reading-this)
    - [Contributions we are accepting](#contributions-we-are-accepting)
    - [Contributions we are NOT looking for](#contributions-we-are-not-looking-for)
- [Ground Rules](#ground-rules)
    - [Responsibilities](#responsibilities)
- [Your First Contribution](#your-first-contribution)
- [Getting started](#getting-started)
    - [Walkthrough of how to submit contribution](#walkthrough-of-how-to-submit-contribution)
      - [Large or Metric Contributions](#large-or-metric-contributions)
      - [Small Contributions](#small-contributions)
      - [Metric Validation](#metric-validation)
- [How to report a bug](#how-to-report-a-bug)
    - [Security-Related Bugs](#security-related-bugs)
    - [Bug Reports](#bug-reports)
- [How to suggest a feature or enhancement](#how-to-suggest-a-feature-or-enhancement)
- [Code review process](#code-review-process)

# Ground Rules

### Responsibilities

* Ensure cross-platform compatibility for every change that's accepted. Windows, Mac, Debian & Ubuntu Linux. _This is typically done through this project's automated testing._
* Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get PAS Program Office & internal community feedback.
* Don't add any classes to the codebase unless absolutely needed. Err on the side of using functions.
* No further dependencies should be needed for the project. If your contribution requires introducing a new one, please make clear within the issue topic.
* Keep feature versions as small as possible, preferably one new feature per version.
* Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

# Your First Contribution

Do you have a metric you want to contribute to DNAmic Analysis and unsure how to get started?

1. Read the `data/` directory's [README.md](data/README.md) to learn how to create a supported SQL query to use against the DNA database file.
2. Read the `dnamic_analysis/` directory's [README.md](dnamic_analysis/README.md) to learn how to create metric calculations and output to Excel for the metric contributed.
3. Read the [DNAmicAnalysis.md]() to learn how to include the metric process into the main function.

Working on your first Pull Request? You can learn how from this *free* series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first :smile_cat:

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

# Getting started

### Walkthrough of how to submit contribution

#### Large or Metric Contributions

For something that is bigger than a one or two line fix:

1. Create your own fork of the code _(Note to Kevin: This could change depending on how this is released to the wild.)_
2. Do the changes in your fork
3. Validate returned metrics during testing are correct. Review the [Metric Validation](#metric-validation) section for more details.
4. If you like the change and think the project could use it:
    * Be sure you have followed the code style for the project.
    * Note the DNAmic Analysis Pull Request template checklist.
    * Send a pull request indicating that you have completed all items in the PR checklist.

#### Small Contributions

Small contributions such as fixing spelling errors, where the content is small enough to not be considered intellectual property, can be submitted by a contributor as a patch.

As a rule of thumb, changes are obvious fixes if they do not introduce any new functionality or creative thinking. As long as the change does not affect functionality, some likely examples include the following:
* Spelling / grammar fixes
* Typo correction, white space and formatting changes
* Comment clean up
* Bug fixes that change default return values or error codes stored in constants
* Adding logging messages or debugging output
* Changes to ‘metadata’ files like requirements.txt, .gitignore, build scripts, etc.
* Moving source files from one directory or package to another

#### Metric Validation

Prior to submitting a Pull Request to include metrics, please validate that the metrics are accurate.

1. Download the [Manual DNA Analysis Toolkit](https://cyberark365.sharepoint.com/:f:/s/PASProgramsOffice/Eh_tR51LtrdPlC27AhEYiXQB0CxXMDFn6z0CqZLxMnoRNA?e=JrBOb1).
2. Use the DNA Report associated with your test DNA database to complete a Manual Analysis to gather results.
   1. If you don't have a test DNA Report and database, you may run DNA on the demo environment in SkyTap to generate one.
3. Run `DNAmicAnalysis.py` against the test DNA database.
4. If the manual and automated metrics match, upload both the manual metrics and automated report as part of the Pull Request.

# How to report a bug

### Security-Related Bugs

If you find a security vulnerability, do NOT open an issue. Email [CyberArk PAS Programs Office](mailto:PASProgramsOffice@cyberark.com?Subject=DNAmic+Analysis+Security+Related+Bug+Identified) instead.

In order to determine whether you are dealing with a security issue, ask yourself these two questions:
* Can I access something that's not mine, or something I shouldn't have access to?
* Can I disable something for other people?

If the answer to either of those two questions are "yes", then you're probably dealing with a security issue. Note that even if you answer "no" to both questions, you may still be dealing with a security issue, so if you're unsure, just email us at [CyberArk PAS Programs Office](mailto:PASProgramsOffice@cyberark.com?Subject=DNAmic+Analysis+Security+Related+Bug+Identified).

### Bug Reports

Information on filing a bug report can be found on the main [README.md](README.md#issues--feature-requests) for the project.

# How to suggest a feature or enhancement

Features and enhancements are currently paused and will only be contributed if from the community.  You can still request one, but know that the maintainer's are no longer in active development on this project.

Information on filing a feature request can be found on the main [README.md](README.md#issues--feature-requests) for the project.

# Code review process

The CyberArk PAS Programs Office looks at Pull Requests on a regular basis. After feedback has been given we expect responses within two weeks. After two weeks we may close the pull request if it isn't showing any activity.

If feedback is responded to in a timely fashion and all automated tests pass, approval from the CyberArk PAS Programs Office can be expected.
