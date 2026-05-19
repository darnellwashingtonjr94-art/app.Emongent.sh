import os
import logging
from eth_account import Account
from src.web3_client import MonadClient
from src.contracts.abi import ERC20_MINIMAL_ABI

logger = logging.getLogger("EmongentContracts")

class TokenManager:
    def __init__(self, client: MonadClient):
        self.client = client
        self.private_key = os.getenv("SIGNER_PRIVATE_KEY")
        self.chain_id = int(os.getenv("CHAIN_ID", 10143))
        
        if self.private_key:
            self.account = Account.from_key(self.private_key)
            logger.info(f"Signer wallet initialized: {self.account.address}")
        else:
            self.account = None
            logger.warning("No SIGNER_PRIVATE_KEY detected. Read-only actions enabled.")

    async def get_token_balance(self, token_address: str, wallet_address: str) -> int:
        """Queries the contract state for a specific address balance."""
        checksum_token = self.client.w3.to_checksum_address(token_address)
        checksum_wallet = self.client.w3.to_checksum_address(wallet_address)
        
        contract = self.client.w3.eth.contract(address=checksum_token, abi=ERC20_MINIMAL_ABI)
        try:
            return await contract.functions.balanceOf(checksum_wallet).call()
        except Exception as e:
            logger.error(f"Failed to query token balance: {str(e)}")
            return 0

    async def execute_transfer(self, token_address: str, recipient_address: str, amount: int) -> str:
        """Builds, signs, and broadcasts an asynchronous token mutation transaction."""
        if not self.account:
            raise ValueError("Signer wallet completely uninitialized. Cannot write to state.")

        token_checksum = self.client.w3.to_checksum_address(token_address)
        recipient_checksum = self.client.w3.to_checksum_address(recipient_address)
        
        contract = self.client.w3.eth.contract(address=token_checksum, abi=ERC20_MINIMAL_ABI)
        nonce = await self.client.w3.eth.get_transaction_count(self.account.address)
        
        # Build transaction payload
        tx_build = await contract.functions.transfer(recipient_checksum, amount).build_transaction({
            'chainId': self.chain_id,
            'gas': 100000,  # Base safe estimation parameter
            'maxFeePerGas': self.client.w3.to_wei('50', 'gwei'),
            'maxPriorityFeePerGas': self.client.w3.to_wei('2', 'gwei'),
            'nonce': nonce,
        })
        
        # Cryptographic signing sequence
        signed_tx = self.client.w3.eth.account.sign_transaction(tx_build, private_key=self.private_key)
        
        # Broadcast raw transaction payload to the network nodes
        tx_hash = await self.client.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        logger.info(f"Transaction successfully broadcasted. Hash: {tx_hash.hex()}")
        return tx_hash.hex()
