from web3 import Web3
import json

RPC_URL = "http://10.229.43.182:8545"
CONTRACT_ADDRESS = "0x99EE451b6272e7AECA2F195984D8bf18cc70285C"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

with open("MerydianNFT.abi") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

total = contract.functions.totalSupply().call()
print(f"Total NFTs mintés : {total}")

uri = contract.functions.tokenURI(1).call()
print(f"URI du NFT : {uri}")