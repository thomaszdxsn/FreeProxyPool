#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import asyncio
import logging

from aiohttp import web


async def index_handler(request):
    ip = request.remote
    return web.json_response(
        {"ip": ip}
    )


async def init_app(app):
    app.add_routes([
        web.route('GET', '/', index_handler)
    ])
    return app


def main(loop):
    app = web.Application(loop=loop)
    app = init_app(app)
    web.run_app(app, port=8888)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    logging.basicConfig(level=logging.DEBUG)
    main(loop)