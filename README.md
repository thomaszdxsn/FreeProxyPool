# 免费代理池

同时爬取多个列有免费代理清单的网站，包括

- https://www.kuaidaili.com/free/intr/
- http://www.xicidaili.com/nt/
- http://www.data5u.com/free/gnpt/index.shtml
- http://www.ip3366.net
- http://www.66ip.cn/index.html
- https://www.us-proxy.org
- https://proxydb.net
- https://www.cool-proxy.net/proxies/http_proxy_list/sort:update_time/direction:desc
- https://proxylist.me/?sort=-updated

利用aiohttp，能够在1分钟内爬取完毕..一次大约有1000个代理.保存到Mongo中

然后使用`ipcheck.py`，通过一个检查IP地址的API检查代理是否可用，如果可用，则
增加权重值；否则减少权重值，在权重值少于0的时候，删除这个代理。

在完成检查步骤以后，可以使用的代理还剩100+个。

程序能够在2分钟以内运行完毕。

## TODO

- 定时任务，维护代理池

- 编写一个helper，随机获取可用的代理