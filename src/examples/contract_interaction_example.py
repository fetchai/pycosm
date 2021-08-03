""" ERC1155 contract deployment and interaction example """

from cosm.crypto.keypairs import PrivateKey
from examples.clients import SigningCosmWasmClient

# ID and amount of tokens to be minted in contract
TOKEN_ID = "1234"
AMOUNT = "1"

# Path to smart contract
CONTRACT_FILENAME = "../../contracts/cw_erc1155.wasm"

# Node config
ENDPOINT_ADDRESS = "localhost:9090"
CHAIN_ID = "testing"

# Private key of sender's account
VALIDATOR_PK = PrivateKey(
    bytes.fromhex(
        "0ba1db680226f19d4a2ea64a1c0ea40d1ffa3cb98532a9fa366994bb689a34ae"
    )
)

# Create client
client = SigningCosmWasmClient(VALIDATOR_PK, ENDPOINT_ADDRESS, CHAIN_ID)

# Store contract
code_id = client.store_contract(CONTRACT_FILENAME)
print(f"Contract stored, code ID: {code_id}")

# Init contract
contract_address = client.instantiate(code_id, {})
print(f"Contract address: {contract_address}")

# Create token with ID TOKEN_ID
create_single_msg = \
    {
        "create_single":
            {
                "item_owner": str(client.address),
                "id": TOKEN_ID,
                "path": "some_path",
            }
    }
response = client.execute(contract_address, create_single_msg)
print(f"Created token with ID {TOKEN_ID}")

# Mint 1 token with ID TOKEN_ID and give it to validator
mint_single_msg = \
    {
        "mint_single":
            {
                "to_address": str(client.address),
                "id": TOKEN_ID,
                "supply": AMOUNT,
                "data": "some_data",
            },
    }
response = client.execute(contract_address, mint_single_msg)
print(f"Minted 1 token with ID {TOKEN_ID}")

# Query validator's balance of token TOKEN_ID
msg = {"balance": {
    "address": str(client.address),
    "id": TOKEN_ID,
}}
res = client.query_contract_state(contract_address=contract_address,
                                  msg=msg)

# Check if balance of token with ID TOKEN_ID of validator is correct
assert res["balance"] == AMOUNT
print("All done!")
