import asyncio
import logging
from src.web3_client import MonadClient
from src.engine.agents import PlanningAgent, ExecutionAgent, VerificationAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmongentEngine")

class ExecutionEngine:
    def __init__(self):
        self.client = MonadClient()
        self.is_running = False
        
        # Instantiate the autonomous agent team
        self.planner = PlanningAgent()
        self.executor = ExecutionAgent()
        self.verifier = VerificationAgent()

    async def process_autonomous_cycle(self, payload: dict):
        """Coordinates the multi-agent pipeline from planning to settlement verification."""
        try:
            logger.info("--- Beginning Autonomous Agent Cycle ---")
            
            # Phase 1: Planning
            state = await self.planner.execute(payload)
            
            # Phase 2: Execution
            state = await self.executor.execute(state)
            
            # Phase 3: Verification / Attestation
            final_state = await self.verifier.execute(state)
            
            logger.info(f"--- Cycle Complete. Status: {final_state['status']} | Tx: {final_state['tx_hash']} ---")
            return final_state
        except Exception as e:
            logger.error(f"Multi-agent workflow pipeline breached: {str(e)}")
            return {"status": "FAILED", "error": str(e)}

    async def start(self):
        self.is_running = True
        logger.info("Emongent Execution Engine successfully initialized.")
        
        while self.is_running:
            try:
                connected = await self.client.check_connection()
                if connected:
                    block = await self.client.get_latest_block()
                    logger.info(f"Active network sync at Block height: {block}")
                    
                    # Mock payload acting as incoming transactions or agent triggers
                    mock_job = {"target_block": block, "timestamp": asyncio.get_event_loop().time()}
                    await self.process_autonomous_cycle(mock_job)
                else:
                    logger.warning("Network connection offline. Retrying...")
            except Exception as e:
                logger.error(f"Engine cycle error: {str(e)}")
            
            await asyncio.sleep(12)

    async def stop(self):
        logger.info("Shutting down execution engine...")
        self.is_running = False
