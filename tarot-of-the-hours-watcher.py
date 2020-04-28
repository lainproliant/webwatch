#!/usr/bin/env python
# --------------------------------------------------------------------
# tarot-of-the-hours-watcher.py
#
# Author: Lain Musgrove (lain.proliant@gmail.com)
# Date: Tuesday April 28, 2020
#
# Distributed under terms of the MIT license.
# --------------------------------------------------------------------

import subprocess
from getpass import getpass

from bs4 import BeautifulSoup

from webwatch import Config, watch


# --------------------------------------------------------------------
def scanner(soup: BeautifulSoup):
    return not str(soup).find("this item is sold out")


# --------------------------------------------------------------------
def main():
    smtp_password = subprocess.check_output(["pass", "lain.proliant@gmail.com"]).decode('utf-8').strip()
    print(f'LRS-DEBUG: smtp_password = {smtp_password}')
    config = Config(
        name="Tarot of the Hours Product Page",
        url="https://www.etsy.com/uk/listing/774143958/tarot-of-the-hours?ref=shop_home_active_1",
        smtp_username="lain.proliant@gmail.com",
        smtp_password=smtp_password)

    watch(config, scanner)


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
