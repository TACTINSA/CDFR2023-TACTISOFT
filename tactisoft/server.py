import asyncio
import functools

import websockets

from tactisoft.cli import NonBlockingCLI


async def serve(websocket, cli: NonBlockingCLI):
    try:
        async for message in websocket:
            cli.process_command(message)
    finally:
        cli.process_command("stop")


def run_forever(cli: NonBlockingCLI):
    async def wrapper():
        async with websockets.serve(functools.partial(serve, cli=cli), "", 7933):
            await asyncio.Future()  # run forever
            cli.process_command("stop")  # stop the robot in case the server disconnects

    asyncio.run(wrapper())
