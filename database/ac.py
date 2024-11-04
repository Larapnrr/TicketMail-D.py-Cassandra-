from cassandra.query import SimpleStatement, dict_factory
from cassandra.auth import PlainTextAuthProvider
from utilities.loader.json_loader import Json
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from aiocassandra import aiosession
from dataclasses import dataclass

config = Json("settings", "settings", "Cassandra")
config = config.load()


@dataclass
class Cassandra:
    query: str
    params: tuple | list
    target: str = None

    def __post_init__(self):
        self.cluster = None
        self.session = None

    async def __aenter__(self):
        auth_provider = PlainTextAuthProvider(config["USER"], config["PASSWORD"])
        self.cluster = Cluster([config["HOST"]], auth_provider=auth_provider)
        self.session = self.cluster.connect(config["KEYSPACE"])
        self.session.row_factory = dict_factory
        aiosession(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.cluster:
            self.cluster.shutdown()
        return

    async def execute(self):
        statement = SimpleStatement(self.query, consistency_level=ConsistencyLevel.ONE)
        if self.query.lower().startswith(("insert", "update", "delete", "create", "list", "describe")):
            return await self.session.execute_future(statement, self.params) or False
        else:
            results = await self.session.execute_future(statement, self.params)
            if self.target:
                try:
                    return results[0][self.target]
                except (IndexError, KeyError):
                    return None
            else:
                if not results:
                    return None
                return list(results) if results else None
