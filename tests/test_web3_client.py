import pytest
from unittest.mock import AsyncMock, patch
from src.web3_client import MonadClient

@pytest.mark.asyncio
async def test_client_connection_handling():
    client = MonadClient()
    
    # Force mock a disconnected state
    with patch.object(client.w3, 'is_connected', AsyncMock(return_value=False)):
        connected = await client.check_connection()
        assert connected is False

    # Force mock a connected state
    with patch.object(client.w3, 'is_connected', AsyncMock(return_value=True)):
        connected = await client.check_connection()
        assert connected is True
