#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import asyncio

import aiohttp
import aiojobs
from aiohttp.client_exceptions import (ServerTimeoutError,
                                       ClientProxyConnectionError,
                                       ClientOSError)

from models import fetch_all_proxy, update_proxy, delete_proxy
from logs import logger


async def verify_ip_valid(session, proxy_item):
    try:
        async with session.get(
            'https://api.ipify.org?format=json',
            proxy='http://{}'.format(str(proxy_item)),
            timeout=30
        ) as resp:
            data = await resp.json()
            return proxy_item.ip == data['ip']
    except (ServerTimeoutError, ClientProxyConnectionError,
            ClientOSError):
        return False
    except Exception as exc:
        logger.warning('请求时发生错误, {}:{}'.format(type(exc), exc))


async def ip_check_task(session, proxy_item):
    pass_verify = await verify_ip_valid(session, proxy_item)
    logger.debug('proxy {} pass verify: {}'.format(
        proxy_item.ip, pass_verify
    ))
    if pass_verify is True:
        proxy_item.pass_verify()
    elif pass_verify is False:
        proxy_item.fail_verify()
    if proxy_item.weight < 0:
        await delete_proxy(proxy_item)
    else:
        await update_proxy(proxy_item)


async def main():
    scheduler = await aiojobs.create_scheduler()
    all_proxy = await fetch_all_proxy()

    async with aiohttp.ClientSession() as session:
        for proxy in all_proxy:
            task = ip_check_task(session, proxy)
            await scheduler.spawn(task)
        await asyncio.sleep(60)
