#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import asyncio
import logging

import aiojobs

from proxy_spider import *
from models import bulk_upsert_proxy
from logs import logger
from ipcheck import main as ip_check


async def wrap_task(loop, spider_coro):
    proxy_items = await spider_coro(loop)
    upsert_result = await bulk_upsert_proxy(proxy_items)
    logger.info("成功将爬取的proxy信息上传数据库: {}".format(upsert_result))


async def main(loop):
    scheduler = await aiojobs.create_scheduler()
    for spider_coro in (crawl_kuaidaili, crawl_xicidaili, crawl_data5u,
                        crawl_ip3366, crawl_66ip, crawl_usproxy,
                        crawl_proxydb, crawl_coolproxy, crawl_proxylist):
        task = wrap_task(loop, spider_coro)
        await scheduler.spawn(task)
    await asyncio.sleep(60)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_until_complete(ip_check())