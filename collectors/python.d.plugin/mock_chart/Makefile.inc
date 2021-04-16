# SPDX-License-Identifier: GPL-3.0-or-later

# THIS IS NOT A COMPLETE Makefile
# IT IS INCLUDED BY ITS PARENT'S Makefile.am
# IT IS REQUIRED TO REFERENCE ALL FILES RELATIVE TO THE PARENT

# install these files
dist_python_DATA       += mock_chart/mock.chart.py
dist_pythonconfig_DATA += mock_chart/mock_chart.conf

# do not install these files, but include them in the distribution
dist_noinst_DATA       += mock_chart/README.md mock_chart/Makefile.inc

