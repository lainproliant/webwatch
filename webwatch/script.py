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
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

import requests


# --------------------------------------------------------------------
@dataclass
class Config:
    name: str
    url: str
    smtp_username: str
    smtp_password: str
    from_addr: Optional[str] = None
    to_addrs: Optional[List[str]] = None
    timeout: int = 60
    subject: str = "Page has been updated: {name}"
    contents: str = "Click here to check the page: {url}"
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    headers: Dict[str, str] = field(default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 "
        "Safari/537.36"
    })

    @property
    def from_address(self) -> str:
        return self.from_addr or self.smtp_username

    @property
    def to_addresses(self) -> List[str]:
        return self.to_addrs or [self.from_address]


# --------------------------------------------------------------------
def watch(config: Config, scanner: Callable[[BeautifulSoup], bool]):
    while True:
        response = requests.get(config.url, headers=config.headers)
        soup = BeautifulSoup(response.text, "lxml")

        if scanner(soup):
            print("Scanner detected a change, sending email now...")

            # setup the email server
            server = smtplib.SMTP(config.smtp_host, config.smtp_port)
            server.starttls()

            # add account login name and password
            server.login(config.smtp_username, config.smtp_password)

            msg = MIMEText(config.contents.format(**config.__dict__))
            msg['Subject'] = config.subject.format(**config.__dict__)
            msg['From'] = config.from_address
            msg['To'] = ', '.join(config.to_addresses)

            print(msg)

            server.sendmail(config.from_address, config.to_addresses, msg.as_string())
            server.quit()
            return

        time.sleep(config.timeout)
