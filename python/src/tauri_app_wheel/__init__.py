from os import environ
environ["_PYTAURI_DIST"] = "pytauri-wheel"

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from anyio import create_task_group, sleep
from anyio.abc import TaskGroup
from anyio.from_thread import start_blocking_portal
from pydantic.alias_generators import to_camel
from pytauri_wheel.lib import builder_factory, context_factory

SRC_TAURI_DIR = Path(__file__).parent.absolute()
TAURI_APP_WHEEL_DEV = environ.get("TAURI_APP_WHEEL_DEV") == "0"
import sys

from pydantic import BaseModel
from pytauri import (
    AppHandle,
    Commands,
)
from pytauri_plugins.notification import NotificationExt

commands: Commands = Commands()


class Person(BaseModel):
    name: str


class Greeting(BaseModel):
    message: str


@commands.command()
async def greet(body: Person, app_handle: AppHandle) -> Greeting:
    notification_builder = NotificationExt.builder(app_handle)
    notification_builder.show(title="Greeting", body=f"Hello, {body.name}!")

    return Greeting(
        message=f"Hello keren, {body.name}! You've been greeted from Python {sys.version}!"
    )

def main() -> int:
    """Run the tauri-app."""
    global task_group
    with (
        start_blocking_portal("asyncio") as portal,
        portal.wrap_async_context_manager(portal.call(create_task_group)) as tg
    ):
        task_group = tg
        
        tauri_config = json.dumps({
            "build": {
                "frontendDist": "http://localhost:1420" if TAURI_APP_WHEEL_DEV else None,
            },
        }) if TAURI_APP_WHEEL_DEV else None

        app = builder_factory().build(
            context=context_factory(SRC_TAURI_DIR, tauri_config=tauri_config),
            invoke_handler=commands.generate_handler(portal),
        )
        return app.run_return()

if __name__ == "__main__":
    exit(main())