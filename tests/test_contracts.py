import pytest
from unittest.mock import AsyncMock, patch
from src.web3_client import MonadClient
from src.contracts import TokenManager

@pytest.mark.asyncio
async def test_token_balance_query_routing():
    client = MonadClient()
    manager = TokenManager(client)
    
    mock_balance = 5000000000000000000  # 5 Tokens in base denomination
    
    # Mocking call return path to prevent external networking dependency during pipeline checks
    with patch("web3.contract.async_contract.AsyncContractFunction.call", AsyncMock(return_value=mock_balance)):
        balance = await manager.get_token_balance(
            "0x0000000000000000000000000000000000000000", 
            "0x0000000000000000000000000000000000000000"
        )
        assert balance == mock_balance
