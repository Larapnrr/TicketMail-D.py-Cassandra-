from database.ac import Cassandra
from typing import Optional


class TicketSetup:
    def __init__(self, guild_id: int, channel_id: int, message_id: int, create_ui_type: str, ticket_ui_type: str, auto_delete: int = 7):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_id = message_id
        self.create_ui_type = create_ui_type
        self.ticket_ui_type = ticket_ui_type
        self.auto_delete = auto_delete # Default is 7 Days
    
    @staticmethod
    async def get(guild_id: int) -> Optional["TicketSetup"]:
        """
        Get TicketSetup.
        """
        async with Cassandra(
            "SELECT * FROM ticket_setups WHERE gid = %s;",
            [
                guild_id
            ]
        ) as cassandra:
            payload = await cassandra.execute()
            payload = payload[0] if payload else None
        if not payload:
            return None
        return TicketSetup(
            payload["gid"],
            payload["chid"],
            payload["mid"],
            payload["create_ui_type"],
            payload["ticket_ui_type"],
            payload["auto_delete"]
        )
    
    async def setup(self):
        """
        Setup Ticket-panel
        """
        async with Cassandra(
            "INSERT INTO ticket_setups (gid, chid, mid, create_ui_type, ticket_ui_type, auto_delete) VALUES (%s, %s, %s, %s, %s, %s);",
            (
                self.guild_id,
                self.channel_id,
                self.message_id,
                self.create_ui_type,
                self.ticket_ui_type,
                self.auto_delete
            )
        ) as cassandra:
            return await cassandra.execute()
    
    async def update(self):
        """
        Update Ticket-panel.
        """
        async with Cassandra(
            "UPDATE ticket_setups SET chid = %s, mid = %s, create_ui_type = %s, ticket_ui_type = %s, auto_delete = %s WHERE gid = %s;",
            (
                self.channel_id,
                self.message_id,
                self.create_ui_type,
                self.ticket_ui_type,
                self.auto_delete,
                self.guild_id
            )
        ) as cassandra:
            return await cassandra.execute()
    
    async def delete(self):
        """
        Delete Ticket-panel.
        """
        async with Cassandra(
            "DELETE FROM ticket_setups WHERE gid = %s",
            [
                self.guild_id
            ]
        ) as cassandra:
            return await cassandra.execute()
        