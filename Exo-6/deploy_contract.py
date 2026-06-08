from web3 import Web3
import json

RPC_URL = "http://10.229.43.182:8545"
PRIVATE_KEY = "8a6440245c9ade760f100d9e58b3b79d70f08bddc078d6fa74ea210ba7526fda"
ACCOUNT = "0x3fA1da90Cf4F5990023D3954f7eded7c8B6C0421"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

with open("MerydianNFT.abi") as f:
    abi = json.load(f)

with open("MerydianNFT.bin") as f:
    bytecode = f.read().strip()

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

tx = contract.constructor().build_transaction({
    "from": ACCOUNT,
    "nonce": w3.eth.get_transaction_count(ACCOUNT),
    "gas": 3000000,
    "gasPrice": w3.to_wei("1", "gwei")
})

signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contrat déployé à : {receipt.contractAddress}")