import os


class Modules:
    def __init__(self, client):
        self.client = client

    async def load(self):
        await self.modules()

    async def modules(self):
        for module in os.listdir("modules"):
            if module.endswith(".py"):
                await self.client.load_extension(f"modules.{module[:-3]}")
