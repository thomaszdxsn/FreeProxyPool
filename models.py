#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import attr
from motor.motor_asyncio import AsyncIOMotorClient


motor_client = AsyncIOMotorClient()
proxy_db = motor_client.proxy
proxy_coll = proxy_db.proxy_pool


@attr.s
class ProxyItem(object):
    ip = attr.ib()
    port = attr.ib(convert=int)
    position = attr.ib(default='')
    weight = attr.ib(default=1, convert=int)      # 权重，默认初始插入数据库时为0

    def __str__(self):
        return "{}:{}".format(self.ip, self.port)

    def pass_verify(self):
        self.weight += 1

    def fail_verify(self):
        self.weight -= 1


async def bulk_upsert_proxy(proxy_list):
    bulk = proxy_coll.initialize_ordered_bulk_op()

    for proxy_item in proxy_list:
        proxy_dict = attr.asdict(proxy_item)
        bulk.find(
            {"ip": proxy_dict['ip'], 'port': proxy_dict['port']}
        ).upsert().update({"$set": proxy_dict})
    result = await bulk.execute()
    return result


async def delete_proxy(proxy_item):
    await proxy_coll.find_one_and_delete({
        "ip": proxy_item.ip,
        "port": proxy_item.port
    })


async def update_proxy(proxy_item):
    await proxy_coll.update({
        "ip": proxy_item.ip,
        "port": proxy_item.port
    }, {"$set": attr.asdict(proxy_item)})


async def fetch_all_proxy():
    all_proxy = await proxy_coll.find().to_list(None)

    proxy_list = [
        ProxyItem(ip=p['ip'], port=p['port'],
                  position=p['position'],
                  weight=p['weight'])
        for p in all_proxy
    ]
    return proxy_list