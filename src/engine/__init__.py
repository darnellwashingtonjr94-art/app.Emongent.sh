import asyncio
import logging
from src.web3_client import MonadClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmongentEngine")

class ExecutionEngine:
    def __init__(self):
        self.client = MonadClient()
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info("Emongent Execution Engine successfully initialized.")
        
        # Loop simulating background tracing or state monitoring
        while self.is_running:
            try:
                connected = await self.client.check_connection()
                if connected:
                    block = await self.client.get_latest_block()
                    logger.info(f"Processing state at Block height: {block}")
                else:
                    logger.warning("Network connection offline. Retrying...")
            except Exception as e:
                logger.error(f"Engine cycle error: {str(e)}")
            
            await asyncio.sleep(10)  # Polling interval

    async def stop(self):
        logger.info("Shutting down execution engine...")
        self.is_running = False
