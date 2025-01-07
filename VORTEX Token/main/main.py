from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solana.keypair import Keypair
from solana.system_program import CreateAccountParams, create_account
from solana.transaction import Transaction
from solana.publickey import PublicKey
from spl.token.constants import 
from spl.token.instructions import (
    initialize_mint, 
    mint_to,
    transfer,
    create_associated_token_account
)

class VortexToken:
    def __init__(self):
        self.client = AsyncClient("https://api.mainnet-beta.solana.com")
        self.decimals = 9
        self.token_program_id = TOKEN_PROGRAM_ID
        self.mint_authority = Keypair()  # Generate new keypair for mint authority
        self.mint_account = Keypair()    # Generate new keypair for mint account
            
    async def initialize_token(self, total_supply: int):
        """
        Initialize the $VORTEX token
        """
        try:
            # Create mint account transaction
            mint_account_tx = create_account(
                CreateAccountParams(
                    from_pubkey=self.mint_authority.public_key,
                    new_account_pubkey=self.mint_account.public_key,
                    lamports=await self.client.get_minimum_balance_for_rent_exemption(82),
                    space=82,
                    program_id=self.token_program_id
                )
            )

            # Initialize mint instruction
            init_mint_ix = initialize_mint(
                program_id=self.token_program_id,
                mint_pubkey=self.mint_account.public_key,
                decimals=self.decimals,
                mint_authority_pubkey=self.mint_authority.public_key,
                freeze_authority_pubkey=self.mint_authority.public_key
            )

            # Create transaction
            transaction = Transaction()
            transaction.add(mint_account_tx)
            transaction.add(init_mint_ix)

            # Send and confirm transaction
            await self.client.send_transaction(
                transaction,
                self.mint_authority,
                opts={"commitment": Commitment.FINALIZED}
            )

            return self.mint_account.public_key

        except Exception as e:
            print(f"Error initializing token: {str(e)}")
            return None

    async def airdrop_tokens(self, recipient_pubkey: PublicKey, amount: int):
        """
        Airdrop tokens to a recipient
        """
        try:
            # Create recipient's associated token account if it doesn't exist
            ata_ix = create_associated_token_account(
                payer=self.mint_authority.public_key,
                owner=recipient_pubkey,
                mint=self.mint_account.public_key
            )

            # Create mint to instruction
            mint_ix = mint_to(
                program_id=self.token_program_id,
                mint_pubkey=self.mint_account.public_key,
                dest_pubkey=recipient_pubkey,
                mint_authority_pubkey=self.mint_authority.public_key,
                amount=amount
            )

            # Create and send transaction
            transaction = Transaction()
            transaction.add(ata_ix)
            transaction.add(mint_ix)

            await self.client.send_transaction(
                transaction,
                self.mint_authority,
                opts={"commitment": Commitment.FINALIZED}
            )

            return True

        except Exception as e:
            print(f"Error in airdrop: {str(e)}")
            return False

    async def reward_user(self, user_pubkey: PublicKey, amount: int):
        """
        Send reward tokens to a user
        """
        try:
            # Transfer tokens from reward pool to user
            transfer_ix = transfer(
                program_id=self.token_program_id,
                source=self.mint_authority.public_key,
                dest=user_pubkey,
                owner=self.mint_authority.public_key,
                amount=amount
            )

            transaction = Transaction()
            transaction.add(transfer_ix)

            await self.client.send_transaction(
                transaction,
                self.mint_authority,
                opts={"commitment": Commitment.FINALIZED}
            )

            return True

        except Exception as e:
            print(f"Error in reward distribution: {str(e)}")
            return False

    async def get_token_balance(self, account_pubkey: PublicKey):
        """
        Get token balance for an account
        """
        try:
            balance = await self.client.get_token_account_balance(account_pubkey)
            return balance['result']['value']['amount']
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            return None

# Example usage
async def main():
    # Initialize token
    vortex = VortexToken()
    mint_pubkey = await vortex.initialize_token(1_000_000_000)  # 1 billion tokens
    
    # Example recipient
    recipient = Keypair()
    
    # Airdrop tokens
    await vortex.airdrop_tokens(recipient.public_key, 1000)
    
    # Reward user
    await vortex.reward_user(recipient.public_key, 500)
    
    # Check balance
    balance = await vortex.get_token_balance(recipient.public_key)
    print(f"Recipient balance: {balance}")

# Run the program
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
