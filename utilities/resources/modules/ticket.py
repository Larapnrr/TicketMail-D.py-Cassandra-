from database.ac import Cassandra
from typing import Optional, List

class Ticket:
    def __init__(self, guild_id: int, channel_id: int, user_ids: int) -> None:
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.user_ids = user_ids
    
    @staticmethod
    async def getAll() -> List["Ticket"]:
        """
        Get all Tickets.
        """
        async with Cassandra(
            "SELECT * FROM tickets;",
            []
        ) as cassandra:
            payload = await cassandra.execute()
        
        if not payload:
            return None
        return [
            Ticket(
                payload["gid"],
                payload["chid"],
                payload["uids"]
            ) for payload in payload
        ]
    
    @staticmethod
    async def get(guild_id: int, channel_id: int) -> Optional["Ticket"]:
        """
        Get a Ticket.
        """
        async with Cassandra(
            "SELECT * FROM tickets WHERE gid = %s AND chid = %s;",
            (
                guild_id,
                channel_id
            )
        ) as cassandra:
            payload = await cassandra.execute()
            payload = payload[0] if payload else None
        if not payload:
            return None
        
        return Ticket(
            payload["gid"],
            payload["chid"],
            payload["uids"]
        )
    
    async def create(self) -> None:
        """
        Create a Ticket.
        """
        async with Cassandra(
            "INSERT INTO tickets (gid, chid, uid) VALUES (%s, %s, %s);",
            (
                self.guild_id,
                self.channel_id,
                self.user_ids
            )
        ) as cassandra:
            return await cassandra.execute()
    
    async def update(self):
        """
        Update Ticket Users.
        """
        async with Cassandra(
            "UPDATE tickets SET uids = %s WHERE gid = %s AND chid = %s;",
            (
                self.user_ids,
                self.guild_id,
                self.channel_id
            )
        ) as cassandra:
            return await cassandra.execute()
    
    async def delete(self):
        async with Cassandra(
            "DELETE FROM tickets WHERE gid = %s AND chid = %s;",
            (
                self.guild_id,
                self.channel_id
            )
        ) as cassandra:
            return await cassandra.execute()