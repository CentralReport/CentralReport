CentralReport News
===================

### Version Alpha 0.5.0 (March 4th, 2014)

- **Improvement [#77](https://github.com/CentralReport/CentralReport/pull/77)**: Added support for unit testing and behaviors tests

- **Improvement [#92](https://github.com/CentralReport/CentralReport/pull/92)**: Updated disk collector for Linux
    * Disks are now gotten by their UUID, and their Linux names are displayed.

- **Improvement [#52](https://github.com/CentralReport/CentralReport/pull/52)**: Many improvements
    * This pull request was initially dedicated to CentralReport Online. As this project will take a new start,
      all references to CRO was removed, and only important improvements was kept.

- **Improvement [#95](https://github.com/CentralReport/CentralReport/pull/95)**: NEWS file is now in markdown

- **Fix [#93](https://github.com/CentralReport/CentralReport/pull/93)**: Fixed uptime displayed on the web server
    * Seconds are now refreshed in uptime data

- **Fix [#94](https://github.com/CentralReport/CentralReport/pull/94)**: Added timezone management in the Javascript part

***

### Version Alpha 0.4.0 (November 22nd, 2013)

- **Improvement [#88](https://github.com/CentralReport/CentralReport/pull/88)**: New host module and fixed memory collector for OS X 10.9 Mavericks
    * The host data are now obtained in a specific module (host.py)
    * The memory collector works well on OS X 10.9, with the memory compression

***

### Version Alpha 0.3.0 (November 4th, 2013)

- **Feature [#58](https://github.com/CentralReport/CentralReport/pull/58)**: CentOS distributions Support

- **Feature [#67](https://github.com/CentralReport/CentralReport/pull/67)**: Travis CI and silent installer/uninstaller
    * Travis CI performs a Continuous Integration to ensure
      your codebase is never broken.
      (https://travis-ci.org/CentralReport/CentralReport)
    * New "-s" argument for the installer and the uninstaller scripts
      When it used, tasks are fully automated, no user interactions required.
      All confirmations are validated by default.
      Useful to perform tests or for deployments.

- **Feature [#70](https://github.com/CentralReport/CentralReport/pull/70)**: New online installer and uninstaller
    * Install and uninstall CentralReport with a single line in a terminal.
      One remote script is available for the installer and another one for
      the uninstaller. They are in charge to automatically download the related
      package and they are handling the magic for you.

- **Feature [#82](https://github.com/CentralReport/CentralReport/pull/82)**: New CLI Manager
    * A friendly way to modify the CentralReport configuration with
      interactive menus and checkboxes in the user terminal. No need
      to modify the configuration file manually!
      Can be used with the command "centralreport manager".
    * Called during the installation to ask to user the basic
      configuration, like the port for the interal web server. Not started
      when using the '-s' parameter (silent installation).

- **Improvement [#72](https://github.com/CentralReport/CentralReport/pull/72)**: Added a check for the webserver port availability
    * When the chosen port is already in use on the current host,
      the webserver isn't started and an error is logged.

- **Improvement [#74](https://github.com/CentralReport/CentralReport/pull/74)**: Bash functions cleaned
    * Removed unneeded code
    * Improved some variables

- **Fix [#73](https://github.com/CentralReport/CentralReport/pull/73)**: Removed old config.py script

- **Fix [#79](https://github.com/CentralReport/CentralReport/pull/79)**: Removed support for Python 2.5 and older

- **Fix [#81](https://github.com/CentralReport/CentralReport/pull/81)**: Removed flot.js library and 'dashboard_mac' template

- **Fix [#84](https://github.com/CentralReport/CentralReport/pull/84)**: Fixed "sudo -n" and "sudo -v" for OS X Mavericks

***

### Version Alpha 0.2.0 (April 24th, 2013)

- **Feature [#27](https://github.com/CentralReport/CentralReport/pull/27)**: Added "cr.system" module

- **Feature [#40](https://github.com/CentralReport/CentralReport/pull/40)**: Added this "News" file :-)

- **Feature [#44](https://github.com/CentralReport/CentralReport/pull/44)**: Improved security and integration on operating systems
    * Added system user and group to secure the CentralReport daemon
      ('centralreport' on Linux, '_centralreport' on Mac)
    * Added binary script in /usr/local/bin
      (CentralReport can be managed with the "centralreport" command in
      a terminal)
    * Moved all CR libraries in /usr/local/lib
    * All third party libraries are now included in CentralReport,
      in zip format (/usr/local/lib/centralreport/cr/libs)

- **Improvement [#25](https://github.com/CentralReport/CentralReport/pull/25)**: Improved the installer and the uninstaller
    * Lines displayed in the CLI are not exceeding 80 columns width
          (bash and config.py)
    * Added default values in config.py script
    * Added new a "lightbox" bash function to display beautiful messages

- **Improvement [#30](https://github.com/CentralReport/CentralReport/pull/30)**: Updated Bootstrap from 2.2.1 to 2.3.0

- **Improvement [#33](https://github.com/CentralReport/CentralReport/pull/33)**: Improved log functions
    * Python Logger is now automatically configured on the first call of
      one logging function
    * Added support for rotating log files. Each log file can't exceed 5 MB,
      and we keep a single backup

- **Improvement [#38](https://github.com/CentralReport/CentralReport/pull/38)**: PEP 8 refactors (code cleaning)
    * Removed CamelCase in methods and variables
    * Cleaned python imports in all scripts

- **Improvement [#45](https://github.com/CentralReport/CentralReport/pull/45)**: Added printBox function in bash

- **Improvement [#48](https://github.com/CentralReport/CentralReport/pull/48)**: Updated data collectors
    * Bash commands have been replaced by python functions when available
    * Checks unification removing duplicated code between Linux and Mac

- **Improvement [#63](https://github.com/CentralReport/CentralReport/pull/63)**: Removed "Routes" python library
    * Removed "setuptools" and "repoze.lru" libraries too

- **Fix [#39](https://github.com/CentralReport/CentralReport/pull/39)**: Improved install dev tools
    * Can now be used on both Linux and Mac OS
    * Script outputs use the same appearance as other bash scripts
      (Lightbox, colums width, error displays)

- **Fix [#50](https://github.com/CentralReport/CentralReport/pull/50)**: Removed "readme.md" file (duplicate content)

***

## Version Alpha 0.1.0 (January 30th, 2013)
Initial release of CentralReport, only for developing and testing purposes.
