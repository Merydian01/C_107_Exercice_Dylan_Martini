from web3 import Web3
import json

RPC_URL = "http://10.229.43.182:8545"
PRIVATE_KEY = "8a6440245c9ade760f100d9e58b3b79d70f08bddc078d6fa74ea210ba7526fda"
ACCOUNT = "0x3fA1da90Cf4F5990023D3954f7eded7c8B6C0421"
CONTRACT_ADDRESS = "0x99EE451b6272e7AECA2F195984D8bf18cc70285C"
IMAGE_URL = "https://i.imgur.com/8nOlEUa.jpeg"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

with open("MerydianNFT.abi") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Activer le mint
tx = contract.functions.toggleIsMintEnabled().build_transaction({
    "from": ACCOUNT,
    "nonce": w3.eth.get_transaction_count(ACCOUNT),
    "gas": 100000,
    "gasPrice": w3.to_wei("1", "gwei")
})
signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)
print("Mint activé !")

# Mint du NFT
tx = contract.functions.mint(IMAGE_URL).build_transaction({
    "from": ACCOUNT,
    "nonce": w3.eth.get_transaction_count(ACCOUNT),
    "gas": 300000,
    "gasPrice": w3.to_wei("1", "gwei"),
    "value": w3.to_wei("0.05", "ether")
})
signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"NFT minté ! Transaction : {tx_hash.hex()}")

