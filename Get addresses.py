from eth_account import Account
from mnemonic import Mnemonic
import binascii
import pandas as pd
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def get_primary_address_from_seed(seed_phrase):
    try:
        # Normalize the seed phrase
        seed_phrase = seed_phrase.strip().lower()
        
        # Validate the seed phrase
        if not Mnemonic("english").check(seed_phrase):
            raise ValueError("Invalid seed phrase")
        
        # Generate seed
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        
        # Create BIP44 object
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
        
        # Derive the first account (m/44'/60'/0'/0/0)
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        
        # Get the address
        address = bip44_acc_ctx.PublicKey().ToAddress()
        
        return address
    except Exception as e:
        print(f"Error processing seed phrase: {e}")
        return None

def get_address_from_seed(seed_phrase):
    try:
        # Normalize the seed phrase
        seed_phrase = seed_phrase.strip().lower()
        
        # Validate the seed phrase
        if not Mnemonic("english").check(seed_phrase):
            raise ValueError("Invalid seed phrase")
        
        # Generate seed
        seed = Mnemonic("english").to_seed(seed_phrase)
        
        # Create a private key from the seed
        private_key = binascii.hexlify(seed[:32]).decode('ascii')
        
        # Generate an Ethereum account
        account = Account.from_key(private_key)
        
        return account.address
    except Exception as e:
        print(f"Error processing seed phrase: {e}")
        return None

# List of seed phrases
seed_phrases = [
    "seed phase 1",
    "Seed phase 2",
    # Add more seed phrases as needed
]

df_out = pd.DataFrame(columns=['Wallet', 'Seed Phrase', 'Address', 'Error'])
# Process each seed phrase and get the address
for i, seed_phrase in enumerate(seed_phrases, 1):
    address = get_primary_address_from_seed(seed_phrase)  # Use the new function here
    if address:
        temp_list = [i, seed_phrase, address, 'False']
        df_temp = pd.DataFrame(data=[temp_list], columns=['Wallet', 'Seed Phrase', 'Address', 'Error'])
        df_out = pd.concat([df_out, df_temp], ignore_index=True)
        print(f"Wallet {i}:")
        print(f"  Seed Phrase: {seed_phrase}")
        print(f"  Address: {address}")
        print()
    else:
        temp_list = [i, '', '', 'True']
        df_temp = pd.DataFrame(data=[temp_list], columns=['Wallet', 'Seed Phrase', 'Address', 'Error'])
        df_out = pd.concat([df_out, df_temp], ignore_index=True)
        print(f"Failed to generate address for Wallet {i}")
        print()
df_out.to_csv('data.csv', index=False)