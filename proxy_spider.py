#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
verifyIp: https://api.ipify.org?format=json

proxy list:
  - https://www.kuaidaili.com/free/intr/2/
  - http://www.xicidaili.com/nt/
  - http://www.data5u.com/free/gnpt/index.shtml
  - http://www.ip3366.net
  - http://www.66ip.cn/index.html
  - https://www.my-proxy.com/free-proxy-list.html           xxx
  - https://nordvpn.com/free-proxy-list/                    xxx
  - https://www.us-proxy.org
  - https://proxydb.net
  - https://www.cool-proxy.net/proxies/http_proxy_list/sort:update_time/direction:desc
  - https://proxylist.me/?sort=-updated
"""

__all__ = ['crawl_proxylist', 'crawl_coolproxy', 'crawl_proxydb',
           'crawl_usproxy', 'crawl_66ip', 'crawl_ip3366',
           'crawl_data5u', 'crawl_xicidaili', 'crawl_kuaidaili']

import asyncio
import base64
import codecs
import functools

import aiohttp
import parsel

from models import ProxyItem
from utlis import generate_random_header


CustomSession = functools.partial(aiohttp.ClientSession,
                                  headers=generate_random_header())


async def crawl_kuaidaili(loop):
    proxy_items = []

    # parse函数
    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_tr_elems = selector.css("table.table-bordered tbody tr")
        result = []
        for tr in all_tr_elems:
            ip = tr.css('td:nth-child(1)::text').extract_first()
            port = tr.css('td:nth-child(2)::text').extract_first()
            position = tr.css('td:nth-child(5)::text').extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        for url in ('https://www.kuaidaili.com/free/inha/',
                    'https://www.kuaidaili.com/free/intr/',):
            async with session.get(url) as resp:
                body = await resp.text()
                parsed_result = parse(body)
                proxy_items.extend(parsed_result)
                # 这个网站的连续访问必须有间隔，不然会返回一个"-10"的body
                await asyncio.sleep(2)

    return proxy_items


async def crawl_xicidaili(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_tr_elems = selector.css('table#ip_list tr')[1:]
        result = []
        for tr in all_tr_elems:
            ip = tr.css('td:nth-child(2)::text').extract_first()
            port = tr.css('td:nth-child(3)::text').extract_first()
            position = tr.css('td:nth-child(4) a::text').extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        for url in ('http://www.xicidaili.com/nn/',
                    'http://www.xicidaili.com/nt/',):
            async with session.get(url) as resp:
                body = await resp.text()
                parsed_result = parse(body)
                proxy_items.extend(parsed_result)

    return proxy_items


async def crawl_data5u(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_lines = selector.css('.l2')
        result = []
        for line in all_lines:
            ip = line.css('span:nth-child(1) li::text').extract_first()
            port = line.css('span:nth-child(2) li::text').extract_first()
            position = line.css('span:nth-child(5) li::text').extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        url = 'http://www.data5u.com/free/gnpt/index.shtml'
        async with session.get(url) as resp:
            body = await resp.text()
            parsed_result = parse(body)
            proxy_items.extend(parsed_result)

    return proxy_items


async def crawl_ip3366(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_tr_elems = selector.css('table.table-bordered tbody tr')
        result = []
        for tr in all_tr_elems:
            ip = tr.css('td:nth-child(1)::text').extract_first()
            port = tr.css('td:nth-child(2)::text').extract_first()
            position = tr.css('td:nth-child(6)::text').extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        url = 'http://www.ip3366.net/'
        async with session.get(url) as resp:
            body = await resp.text()
            parsed_result = parse(body)
            proxy_items.extend(parsed_result)

    return proxy_items


async def crawl_66ip(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_tr_elems = selector.css('table[border="2px"] tr')[1:]
        result = []
        for tr in all_tr_elems:
            ip = tr.css('td:nth-child(1)::text').extract_first()
            port = tr.css('td:nth-child(2)::text').extract_first()
            position = tr.css('td:nth-child(3)::text').extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        for url in ('http://www.66ip.cn/index.html',
                    'http://www.66ip.cn/2.html',
                    'http://www.66ip.cn/3.html'):
            async with session.get(url) as resp:
                body = await resp.text()
                parsed_result = parse(body)
                proxy_items.extend(parsed_result)

    return proxy_items


async def crawl_usproxy(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_tr_elems = selector.css('#proxylisttable tbody tr')
        result = []
        for tr in all_tr_elems:
            ip = tr.css('td:nth-child(1)::text').extract_first()
            port = tr.css('td:nth-child(2)::text').extract_first()
            position = tr.css('td:nth-child(4)::text').extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        url = 'https://www.us-proxy.org/'
        async with session.get(url) as resp:
            body = await resp.text()
            parsed_result = parse(body)
            proxy_items.extend(parsed_result)

    return proxy_items


async def crawl_proxydb(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_tr_elems = selector.css('table.table-hover tbody tr')
        # 这个数字用来计算端口号
        data_num = selector.css('html').re_first(
            r'<div style="display:none" data-[a-zA-Z]*="(\d+)"'
        )
        result = []

        for tr in all_tr_elems:
            position = tr.css('td:nth-child(4) div::text').extract_first()
            # 解析第一个td下面的script标签
            script_elem = tr.css('td:nth-child(1) script::text')

            # ip first part, is reversed form
            ip_first_part = script_elem.re_first(r'\'([\d\.]*)\'\.split')
            ip_first_part = ''.join(reversed(ip_first_part))

            # ip second part, is base64 encoded
            hex_list = script_elem.re(r'\\x([A-Za-z0-9]{2})')
            b64_string = bytearray.fromhex(''.join(hex_list)).decode()
            ip_second_part = base64.b64decode(b64_string).decode()

            ip = ip_first_part + ip_second_part

            # 获取页面中的port，然后加上data_num，就是实际的port
            raw_port = script_elem.re_first(r'var pp = \((\d+) -')
            port = int(raw_port) + int(data_num)

            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        for offset in range(0, 600, 15):
            params = [
                ('protocol', 'http'),
                ('protocol', 'https'),
                ('offset', str(offset))
            ]
            base_url = 'https://proxydb.net/'
            async with session.get(base_url, params=params) as resp:
                body = await resp.text()
                parsed_result = parse(body)
                proxy_items.extend(parsed_result)

    return proxy_items


async def crawl_coolproxy(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        result = []
        all_tr_elems = selector.css('table tr')[1:]
        for tr in all_tr_elems:
            secret_ip = tr.css('td:nth-child(1) script::text').re_first(
                r'rot13\(\"(.*?)\"'
            )
            if secret_ip is None:
                continue
            decoded_by_rot13 = codecs.decode(secret_ip, 'rot13')
            ip = base64.b64decode(decoded_by_rot13).decode()
            port = tr.css("td:nth-child(2)::text").extract_first()
            position = tr.css("td:nth-child(4)::text").extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)

        return result

    async with CustomSession(loop=loop) as session:
        base_url = 'https://www.cool-proxy.net/proxies/http_proxy_list/' \
                   'sort:update_time/direction:desc/page:{page}'
        for page in range(1, 16):
            url = base_url.format(page=page)
            async with session.get(url) as resp:
                body = await resp.text()
                parsed_result = parse(body)
                proxy_items.extend(parsed_result)

    return proxy_items


async def crawl_proxylist(loop):
    proxy_items = []

    def parse(resp_body):
        selector = parsel.Selector(text=resp_body)
        all_tr_elems = selector.css('#datatable-row-highlight tbody tr')
        result = []

        for tr in all_tr_elems:
            ip = tr.css('td:nth-child(1) a::text').extract_first()
            port = tr.css('td:nth-child(2)::text').extract_first()
            if port is None:
                continue
            position = tr.css('td:nth-child(5)::text').extract_first()
            item = ProxyItem(
                ip=ip, port=port, position=position
            )
            result.append(item)
        return result

    async with CustomSession(loop=loop) as session:
        base_url = 'https://proxylist.me/?page={page}&sort=-updated'
        for page in range(1, 15):
            url = base_url.format(page=page)
            async with session.get(url) as resp:
                body = await resp.text()
                parsed_result = parse(body)
                proxy_items.extend(parsed_result)

    return proxy_items


