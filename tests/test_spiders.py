#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from proxy_spider import (crawl_kuaidaili, crawl_xicidaili, crawl_data5u,
                          crawl_ip3366, crawl_66ip, crawl_usproxy,
                          crawl_proxydb, crawl_coolproxy, crawl_proxylist)
from models import ProxyItem


async def test_crawl_kuaidaili(loop):
    result = await crawl_kuaidaili(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_xicidaili(loop):
    result = await crawl_xicidaili(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_data5u(loop):
    result = await crawl_data5u(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_ip3366(loop):
    result = await crawl_ip3366(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_66ip(loop):
    result = await crawl_66ip(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_usproxy(loop):
    result = await crawl_usproxy(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_proxydb(loop):
    result = await crawl_proxydb(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_coolproxy(loop):
    result = await crawl_coolproxy(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)


async def test_crawl_proxylist(loop):
    result = await crawl_proxylist(loop)
    assert len(result) > 0
    assert isinstance(result[1], ProxyItem)