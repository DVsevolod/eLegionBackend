import aiohttp
import asyncio

async def main():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://0.0.0.0:8000/ws') as ws:
        print("Started")
        async for msg in ws:
            print(msg)
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close cmd':
                    await ws.close()
                    break
                else:
                    key = input('>')
                    if key:
                        await ws.send_str('{"id": "213c63df-81d0-450d-8396-62db726d2e1b", "text":' + key + '}')
                    else:
                        await ws.send_str('{"id": "213c63df-81d0-450d-8396-62db726d2e1b", "text": "hello"}')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
    print("End")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
