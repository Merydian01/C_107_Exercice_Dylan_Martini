"""
Nom du fichier : metadata.py
Nom du créateur : Dylan Martini
But du fichier : Création du hash calculator
Date de création : 08.06.2026
"""


from web3 import Web3
from dotenv import load_dotenv
import os
import json

# ==========================================================
# CONFIGURATION
# ==========================================================

load_dotenv()

RPC_URL = "http://10.229.43.182:8545"

SENDER_ADDRESS = "0x3fA1da90Cf4F5990023D3954f7eded7c8B6C0421"
RECEIVER_ADDRESS = "0x0000000000000000000000000000000000000000"

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

METADATA_FILE = "metadata.json"
CHAIN_ID = 32383   # ton chainId

# ==========================================================

# CONNEXION À LA BLOCKCHAIN

# ==========================================================


w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():

    print("Connecté à la blockchain")

else:

    print("Connexion échouée")

    exit()


def charger_metadata_hex(fichier):
    """
    Lit le fichier JSON et retourne les données encodées en hex
    """
    with open(fichier, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    metadata_str = json.dumps(metadata)
    metadata_bytes = metadata_str.encode("utf-8")
    metadata_hex = w3.to_hex(metadata_bytes)

    return metadata_hex

def envoyer_metadata(metadata_hex, nonce):
    """
    Envoie une transaction contenant des métadonnées
    """

    transaction = {
        "from": SENDER_ADDRESS,
        "to": RECEIVER_ADDRESS,      # adresse nulle
        "value": 0,                  # pas d’ETH transféré
        "gas": 200000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce,
        "chainId": CHAIN_ID,
        "data": metadata_hex
    }

    signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()

def main():
    print("\n=== Envoi des métadonnées ===")

    metadata_hex = charger_metadata_hex(METADATA_FILE)
    nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)

    try:
        tx_hash = envoyer_metadata(metadata_hex, nonce)
        print("Transaction envoyée")
        print(f"Hash : {tx_hash}")
        print(f"Data (hex) : {metadata_hex}")

    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()