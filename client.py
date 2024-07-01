import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8080/advert",
                                json={'title': 'sell garage', 'description': 'The best garage', 'owner': 'John Smit'},
                                ) as response:
            print(response.status)
            print(await response.text())

        async with session.get("http://127.0.0.1:8080/advert/1") as response:
            print(response.status)
            print(await response.text())

        async with session.get("http://127.0.0.1:8080/advert/2") as response:
            print(response.status)
            print(await response.text())

        async with session.delete("http://127.0.0.1:8080/advert/1") as response:
            print(response.status)
            print(await response.text())

        async with session.get("http://127.0.0.1:8080/advert/1") as response:
            print(response.status)
            print(await response.text())


asyncio.run(main())