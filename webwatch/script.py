# --------------------------------------------------------------------
# webwatch/script.py
#
# Based on the script by Chris Albon at:
# https://chrisalbon.com/python/web_scraping/monitor_a_website/
#
# Author: Lain Musgrove (lain.proliant@gmail.com)
# Date: Tuesday April 28, 2020
#
# Distributed under terms of the MIT license.
# --------------------------------------------------------------------

import smtplib
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from bs4 import BeautifulSoup

import requests


# --------------------------------------------------------------------
@dataclass
class Config:
    url: str
    smtp_username: str
    smtp_password: str
    from_addr: str
    callback: Callable[[BeautifulSoup], bool]
    to_addrs: Optional[List[str]] = None
    timeout: int = 60
    subject: str = "Page has been updated: {url}"
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 "
        "Safari/537.36"
    }


# --------------------------------------------------------------------
def watch(config: Config, scanner: Callable[[BeautifulSoup], bool]):
    while True:
        # set the url as VentureBeat,
        # set the headers like we are a browser,
        # download the homepage
        response = requests.get(config.url, headers=config.headers)
        # parse the downloaded homepage and grab all text, then,
        soup = BeautifulSoup(response.text, "lxml")

        if scanner(soup):
            # setup the email server,
            server = smtplib.SMTP(config.smtp_host, config.smtp_port)
            server.starttls()

            # add account login name and password
            server.login(config.smtp_username, config.smtp_password)

            # send the email
            server.sendmail(config.from_addr, config.to_addrs or [config.from_addr],
                            config.subject.format(**config.__dict__))
            server.quit()

        time.sleep(config.timeout)

