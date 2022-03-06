import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/infura_API_KEY")) #infura API키 입력.
print(w3.isConnected())

key="private_Key" #Metamask의 private Key 입력.
acct = w3.eth.account.privateKeyToAccount(key)


truffleFile = json.load(open('./build/contracts/greeter.json')) #컴파일 후 생성된 ".json"파일의 위치 입력.
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract= w3.eth.contract(bytecode=bytecode, abi=abi)

construct_txn = contract.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})

signed = acct.signTransaction(construct_txn)

tx_hash=w3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed At:", tx_receipt['contractAddress'])