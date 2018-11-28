import asyncio
from proxybroker import Broker

import logging
log = logging.getLogger(__name__)


class ProxyBroker:
    proxies = []

    def __init__(self):
        log.info('Search for proxies.')
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(
            broker.find(types=['HTTP', 'HTTPS'], limit=1000, strict=True),
            self.add_proxies(proxies))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)

    async def add_proxies(self, proxies):
        while True:
            proxy = await proxies.get()

            if proxy is None:
                break

            log.debug('Found proxy: %s' % proxy)
            self.proxies.append(f"{proxy.host}:{proxy.port}")
