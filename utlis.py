#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from fake_useragent import UserAgent

ua = UserAgent()


def generate_random_header():
    return {
        'User-Agent': ua.chrome,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7',
    }