import asyncio
from aiohttp import web
from motor import motor_asyncio as ma

from settings import MONGO_HOST, MONGO_DB_NAME, HOST, PORT
from routing import routings
from aiohttp.web import middleware


@middleware
async def db_handler(request, handler):
    if request.path.startswith('/static/') or request.path.startswith('/_debugtoolbar'):
        response = await handler(request)
        return response
    request.db = app.db
    response = await handler(request)
    return response


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, app, runner):
    print("Server is shutting down")
    server.close()
    await server.wait_closed()
    app.client.close()
    await app.shutdown()
    await app.cleanup()


async def init(loop):
    app = web.Application(middlewares=[db_handler])

    for r in routings:
        app.router.add_route(r.method, r.path, r.controller, name=r.title)

    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]
    app['websockets'] = []
    app.on_shutdown.append(on_shutdown)

    runner = app.make_handler()

    serv_generator = loop.create_server(runner, HOST, PORT)
    print("Server is created for HOST:" + str(HOST) + " PORT:" + str(PORT))
    return serv_generator, runner, app


loop = asyncio.get_event_loop()
serv_generator, appRunner, app = loop.run_until_complete(init(loop))
serv = loop.run_until_complete(serv_generator)

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Interupt")
    pass
finally:
    loop.run_until_complete(shutdown(serv, app, appRunner))
    loop.close()
