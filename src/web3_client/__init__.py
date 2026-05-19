import os
from web3 import AsyncWeb3
from web3.providers.async_rpc import AsyncHTTPProvider
from dotenv import load_dotenv

load_dotenv()

class MonadClient:
    def __init__(self):
        # Defaulting to a local/devnet RPC if environment variable isn't set
        self.rpc_url = os.getenv("MONAD_RPC_URL", "http://127.0.0.1:8545")
        self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc_url))

    async def check_connection(self) -> bool:
        try:
            return await self.w3.is_connected()
        except Exception:
            return False

    async def get_latest_block(self) -> int:
        if not await self.check_connection():
            raise ConnectionError("Unable to connect to the network RPC.")
        return await self.w3.eth.block_number
