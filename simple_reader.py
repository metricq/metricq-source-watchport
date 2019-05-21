import asyncio
import serial_asyncio
import re


class WatchPortConnection(object):
    async def connect(self, path):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(
            url=path, baudrate=115200
        )

        await self.send("I\r")
        ident = await self.reader.read(n=100)
        print("Device identification: {}".format(ident.decode()))

    async def send(self, msg):
        self.writer.write(msg.encode())
        await asyncio.sleep(0.5)

    async def read_temperature(self):
        await self.send("T\r")
        temperature_line = await self.reader.read(n=60)

        match = re.search(r"(\d+.\d+)C", temperature_line.decode())

        return float(match.group(1))

    async def main(self, path):
        await self.connect(path)
        while True:
            temp = await self.read_temperature()
            print("{} C".format(temp))

            await asyncio.sleep(1)


if __name__ == "__main__":
    port = WatchPortConnection()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(port.main("/dev/ttyUSB0"))
    loop.close()
