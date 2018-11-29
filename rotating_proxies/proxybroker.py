import asyncio
import logging
import time
from threading import Thread

from proxybroker import Broker

log = logging.getLogger(__name__)


class ProxyBroker:
    proxies = []

    def __init__(self):
        log.info('Search for proxies.')
        proxies = asyncio.Queue()
        broker = Broker(proxies, timeout=3, max_conn=200, max_tries=2, verify_ssl=False)
        tasks = asyncio.gather(
            broker.find(types=[('HTTP', ('Anonymous', 'High')), ], limit=7000),
            self.add_proxies(proxies))

        loop = asyncio.get_event_loop()

        def start_worker():
            loop.run_until_complete(tasks)

        worker = Thread(target=start_worker)
        worker.start()

        while len(self.proxies) < 100:
            time.sleep(1)

    async def add_proxies(self, proxies):
        while True:
            proxy = await proxies.get()

            if proxy is None:
                break

            log.debug('Found proxy: %s' % proxy)
            self.proxies.append(f"http://{proxy.host}:{proxy.port}")
