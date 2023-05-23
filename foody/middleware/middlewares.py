# -*- coding: utf-8 -*-

from scrapy.http import HtmlResponse, Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
import random


from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings['HTTP_PROXY']

class RandomUserAgentMiddleware(object):
    def process_request(self, request,spider):
        userAgent = random.choice(settings['USER_AGENT_LIST'])
        if userAgent:
            request.headers.setdefault("User-Agent", userAgent)

