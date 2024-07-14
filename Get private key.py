from eth_account import Account
from mnemonic import Mnemonic
import binascii
import pandas as pd
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def get_primary_wallet_from_seed(seed_phrase):
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
        
        # Get the private key and address
        private_key = bip44_acc_ctx.PrivateKey().Raw().ToHex()
        address = bip44_acc_ctx.PublicKey().ToAddress()
        
        return private_key, address
    except Exception as e:
        print(f"Error processing seed phrase: {e}")
        return None, None

# List of seed phrases
seed_phrases = [
    "Seed phase 1" ,
    # Add more valid seed phrases as needed
]

df_out = pd.DataFrame(columns=['Wallet', 'Seed Phrase', 'Private Key', 'Address', 'Error'])
# Process each seed phrase and get the address and private key
for i, seed_phrase in enumerate(seed_phrases, 1):
    private_key, address = get_primary_wallet_from_seed(seed_phrase)
    if address and private_key:
        temp_list = [i, seed_phrase, private_key, address, 'False']
        df_temp = pd.DataFrame(data=[temp_list], columns=['Wallet', 'Seed Phrase', 'Private Key', 'Address', 'Error'])
        df_out = pd.concat([df_out, df_temp], ignore_index=True)
        print(f"Wallet {i}:")
        print(f"  Seed Phrase: {seed_phrase}")
        print(f"  Private Key: {private_key}")
        print(f"  Address: {address}")
        print()
    else:
        temp_list = [i, '', '', '', 'True']
        df_temp = pd.DataFrame(data=[temp_list], columns=['Wallet', 'Seed Phrase', 'Private Key', 'Address', 'Error'])
        df_out = pd.concat([df_out, df_temp], ignore_index=True)
        print(f"Failed to generate wallet for Seed Phrase {i}")
        print()

df_out.to_csv('wallet_data.csv', index=False)