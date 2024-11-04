import discord

from utilities.loader.modules_loader import Modules
from utilities.loader.json_loader import Json
from database.ac import Cassandra
from discord.ext import commands

json = Json("settings", "settings", "Client")
settings = json.load()

class Client(commands.Bot):
    def __init__(self) -> None:
        """
        Initialize Client.
        """
        super().__init__(command_prefix=settings["PREFIX"], help_command=None, intents=discord.Intents.all())
        self.token = settings["TOKEN"]
        self.modul = Modules(self)
    
    async def start(self):
        return await super().start(self.token, reconnect=True)
    
    async def setup_hook(self) -> None:
        await self.modul.load()
        print("Online")
    