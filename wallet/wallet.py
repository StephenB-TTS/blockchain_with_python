# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
from bipwallet import wallet
from web3 import Web3
from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
 
 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = f'./derive -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --format=json' --cols=path,address,privkey,pubkey --form
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    "btc-test" : derive_wallets(mnemonic, BTCTEST, 3),
    "eth": derive_wallets(mnemonic, ETH, 3)
    }

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):

    if(coin == 'eth'):
        return Account.privateKeyToAccount(priv_key)
    elif(coin == 'btc-test'):
        return PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):

    if(coin == 'eth'):
        gas_estimate = w3.eth.estimateGas(
            {'from': account.address, 'to': to, 'value': amount}
        )
        return {
            'to': to,
            'from': account.address,
            'value': amount,
            'gas': gas_estimate,
            'gasPrice': w3.eth.gasPrice,
            'nonce': w3.eth.getTransactionCount(account.address),
            'chainID': w3.net.chainId
				
        }
    elif(coin == 'btc-test'):
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):

    raw_tx = create_tx(coin, account, to, amount)
    signed = account.sign_transaction(raw_tx)

    if(coin == 'eth'):
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    elif(coin == 'btc-test'):
        return NetworkAPI.broadcast_tx_testnet(signed)

# ETH transaction
send_tx(ETH, eth_sender_account, eth_recipient_address, 1)

# BTCTEST transaction
send_tx(BTCTEST, btctest_sender_account, btctest_recipient_address. 0.001)