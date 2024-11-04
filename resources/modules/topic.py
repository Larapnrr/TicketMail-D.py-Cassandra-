from database.ac import Cassandra
from typing import Optional, List


class TicketTopic:
    def __init__(self, guild_id: int, topic: str, roles: int):
        self.guild_id = guild_id
        self.topic = topic
        self.roles = roles
    
    @staticmethod
    async def getAll(guild_id: int) -> List["TicketTopic"]:
        """
        Get all Ticket-panel Topics
        """

        async with Cassandra(
            "SELECT * FROM ticket_topics WHERE gid = %s;",
            [
                guild_id
            ]
        ) as cassandra:
            payload = await cassandra.execute()
        if not payload:
            return None
        return [
            TicketTopic(
                payload["gid"],
                payload["topic"],
                payload["roles"]
            ) for payload in payload
        ]
    
    async def add(self):
        """
        Add Topic.
        """
        async with Cassandra(
            "INSERT INTO ticket_topics (gid, name, roles) VALUES (%s, %s, %s);",
            (
                self.guild_id,
                self.topic,
                self.roles
            )
        ) as cassandra:
            return await cassandra.execute()
    
    async def update(self):
        """
        Update Topic.
        """
        async with Cassandra(
            "UPDATE ticket_topics SET topic = %s, roles = %s WHERE gid = %s;",
            (
                self.topic,
                self.roles,
                self.guild_id
            )
        ) as cassandra:
            return await cassandra.execute()
        
    async def delete(self):
        """
        Delete Topic.
        """
        async with Cassandra(
            "DELETE FROM ticket_topics WHERE gid = %s AND topic = %s;",
            (
                self.guild_id,
                self.topic
            )
        ) as cassandra:
            return await cassandra.execute()
