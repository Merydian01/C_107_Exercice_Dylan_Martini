from web3 import Web3
from dotenv import load_dotenv
import os
import sys


# CONFIGURATION


load_dotenv()

RPC_URL = "http://10.229.43.182:8545"

SENDER_ADDRESS = "0x3fA1da90Cf4F5990023D3954f7eded7c8B6C0421"

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

AMOUNT_TO_SEND = 0.1  # ETH


# VÉRIFICATIONS


if PRIVATE_KEY is None:
    print(" PRIVATE_KEY introuvable dans le fichier .env")
    sys.exit()


# CONNEXION BLOCKCHAIN


w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print(" Connecté à la blockchain")
else:
    print(" Impossible de se connecter à la blockchain")
    sys.exit()


# LECTURE DES ADRESSES


def lire_adresses(fichier):
    adresses = []

    try:
        with open(fichier, "r") as f:
            for ligne in f:
                adresse = ligne.strip()

                if w3.is_address(adresse):
                    adresses.append(
                        Web3.to_checksum_address(adresse)
                    )
                else:
                    print(f" Adresse invalide ignorée : {adresse}")

    except FileNotFoundError:
        print(f" Fichier introuvable : {fichier}")
        sys.exit()

    return adresses


# AFFICHER LES SOLDES


def afficher_soldes(adresses):

    print()

    for adresse in adresses:
        try:
            balance_wei = w3.eth.get_balance(adresse)
            balance_eth = w3.from_wei(balance_wei, "ether")

            print(f"{adresse} -> {balance_eth} ETH")

        except Exception as e:
            print(f"Erreur balance {adresse} : {e}")


# ENVOI TRANSACTION


def envoyer_eth(destinataire, montant_eth, nonce):

    transaction = {
        "nonce": nonce,
        "to": destinataire,
        "value": w3.to_wei(montant_eth, "ether"),
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    }

    # Signature
    signed_tx = w3.eth.account.sign_transaction(
        transaction,
        PRIVATE_KEY
    )

    # Envoi
    tx_hash = w3.eth.send_raw_transaction(
        signed_tx.raw_transaction
    )

    return tx_hash.hex()


# PROGRAMME PRINCIPAL


def main():

    adresses = lire_adresses("adresses.txt")

    if len(adresses) == 0:
        print(" Aucune adresse valide")
        return

    print("\n=== SOLDES AVANT ===")
    afficher_soldes(adresses)

    # Nonce actuel
    nonce = w3.eth.get_transaction_count(
        Web3.to_checksum_address(SENDER_ADDRESS),
        "pending"
    )

    print("\n=== ENVOI DES TRANSACTIONS ===\n")

    for adresse in adresses:

        try:

            tx_hash = envoyer_eth(
                adresse,
                AMOUNT_TO_SEND,
                nonce
            )

            print(f" Transaction envoyée vers : {adresse}")
            print(f" Hash : {tx_hash}\n")

            nonce += 1

        except Exception as e:

            print(f" Erreur vers {adresse}")
            print(e)
            print()

    print("\n=== SOLDES APRÈS ===")
    afficher_soldes(adresses)


# LANCEMENT


if __name__ == "__main__":
    main()