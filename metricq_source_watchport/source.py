import asyncio
import serial_asyncio
import re

import metricq

logger = metricq.logging.get_logger()


class WatchPortSource(metricq.IntervalSource):
    def __init__(self, *args, **kwargs):
        logger.info("initializing WatchPortSource")
        super().__init__(*args, **kwargs)
        self.period = None

    @metricq.rpc_handler('config')
    async def _on_config(self, **config):
        logger.info('WatchPortSource config: {}', config)
        rate = config['rate']
        self.metric_name = config['metric']
        await self.serial_connect(config['path'])

        self.period = 1 / rate
        meta = {
           'rate': rate,
           'unit': '℃',
        }
        await self.declare_metrics({self.metric_name: meta})

    async def update(self):
        temp = await self.read_temperature()
        logger.debug('Read temperature from device: {} C', temp)
        await self[self.metric_name].send(metricq.Timestamp.now(), temp)

    async def serial_connect(self, path):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(loop=self.event_loop, url=path, baudrate=115200)

        await self.serial_send('I\r')
        ident = await self.reader.read(n=100)
        logger.info('Device identification: {}', ident.decode())

    async def serial_send(self, msg):
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def read_temperature(self):
        await self.serial_send('T\r')
        temperature_line = await self.reader.read(n=60)

        match = re.search(r"(\d+.\d+)C", temperature_line.decode())

        return float(match.group(1))
