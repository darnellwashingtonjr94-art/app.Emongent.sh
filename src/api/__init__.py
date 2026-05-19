from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.engine import ExecutionEngine
from src.contracts import TokenManager

app = FastAPI(
    title="app.Emongent.sh Core API",
    description="High-performance control interface for autonomous multi-agent Web3 execution.",
    version="1.0.0"
)

# Shared Core State Engines
engine = ExecutionEngine()
token_manager = TokenManager(engine.client)

# Data Schemas for API Requests
class BalanceRequest(BaseModel):
    token_address: str = Field(..., description="EVM/Monad compliant contract address")
    wallet_address: str = Field(..., description="Target wallet address to query")

class TriggerCycleRequest(BaseModel):
    payload: dict = Field(default_factory=dict, description="Custom context metadata to pass to agents")


@app.get("/health")
async def health_check():
    """Returns the comprehensive operating status of the network client and background engine."""
    connected = await engine.client.check_connection()
    current_block = None
    if connected:
        try:
            current_block = await engine.client.get_latest_block()
        except Exception:
            pass

    return {
        "status": "healthy",
        "network": {
            "rpc_connected": connected,
            "latest_block_height": current_block,
            "chain_id": token_manager.chain_id
        },
        "engine": {
            "active": engine.is_running,
            "agent_team": [
                {"name": engine.planner.name, "role": engine.planner.role},
                {"name": engine.executor.name, "role": engine.executor.role},
                {"name": engine.verifier.name, "role": engine.verifier.role}
            ]
        }
    }


@app.post("/wallet/balance")
async def get_token_balance(data: BalanceRequest):
    """Direct routing to query an ERC-20 token balance on-chain via the Contract layer."""
    try:
        balance = await token_manager.get_token_balance(data.token_address, data.wallet_address)
        return {
            "token_address": data.token_address,
            "wallet_address": data.wallet_address,
            "raw_balance": str(balance)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contract execution query failed: {str(e)}")


@app.post("/engine/trigger")
async def trigger_agent_cycle(data: TriggerCycleRequest):
    """Manually forces the Multi-Agent orchestrator to execute an autonomous routing & verification cycle."""
    # Ensure network connectivity exists before locking agent tasks
    if not await engine.client.check_connection():
        raise HTTPException(status_code=503, detail="RPC Node connection offline. Execution barred.")
    
    # Run a localized execution sweep
    result = await engine.process_autonomous_cycle(data.payload)
    
    if result.get("status") == "FAILED":
        raise HTTPException(status_code=422, detail=result)
        
    return {
        "message": "Autonomous pipeline executed successfully.",
        "execution_summary": result
    }
