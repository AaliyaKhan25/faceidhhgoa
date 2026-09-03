import os
import json
import sys
import requests
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

CONTRACT_ABI = json.loads('''[
    {"inputs":[{"internalType":"string","name":"_postUrl","type":"string"},{"internalType":"bytes32","name":"_dataHash","type":"bytes32"}],"name":"anchorMatch","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"bytes32","name":"_dataHash","type":"bytes32"}],"name":"verifyMatch","outputs":[{"internalType":"bool","name":"isVerified","type":"bool"},{"internalType":"string","name":"postUrl","type":"string"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"}
]''')

def process_and_search(image_path: str) -> dict:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    print(f"\n[1/3] Processing local image: {image_path}...")
    
    # Upload local image to free temporary host so Google Lens can access it
    print("  Uploading image to temp host for visual search...")
    with open(image_path, 'rb') as f:
        response = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": f})
        
    if response.status_code != 200:
        raise Exception("Failed to upload local image for web search.")
        
    upload_data = response.json()
    # Format direct download URL for tmpfiles.org
    raw_url = upload_data["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")
    print(f"✔ Temp Public URL generated: {raw_url}")

    print("[2/3] Searching web via SerpApi (Google Lens)...")
    params = {
        "engine": "google_lens",
        "url": raw_url,
        "api_key": SERPAPI_KEY
    }
    
    lens_resp = requests.get("https://serpapi.com/search", params=params).json()
    
    if "error" in lens_resp:
        raise Exception(f"SerpApi Error: {lens_resp['error']}")

    matches = lens_resp.get("visual_matches", [])
    if not matches:
        raise Exception("No visual matches or social profiles found for this face.")

    # Return top matched link
    top_match = matches[0]
    matched_data = {
        "title": top_match.get("title", "Matched Profile"),
        "post_url": top_match.get("link")
    }
    print(f"\n🎯 ACTUAL MATCH FOUND:")
    print(f"   • Title: {matched_data['title']}")
    print(f"   • Profile/Source URL: {matched_data['post_url']}")
    return matched_data


def anchor_and_verify(matched_data: dict):
    print("\n[3/3] Anchoring fingerprint on Sepolia Testnet...")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    contract_addr = w3.to_checksum_address(CONTRACT_ADDRESS)
    account = w3.eth.account.from_key(PRIVATE_KEY)
    contract = w3.eth.contract(address=contract_addr, abi=CONTRACT_ABI)

    payload = f"{matched_data['post_url']}:{matched_data['title']}".encode('utf-8')
    data_hash = w3.solidity_keccak(['bytes'], [payload])

    tx = contract.functions.anchorMatch(matched_data['post_url'], data_hash).build_transaction({
        'chainId': 11155111,
        'gas': 200000,
        'maxFeePerGas': w3.to_wei('30', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('25', 'gwei'),
        'nonce': w3.eth.get_transaction_count(account.address),
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    raw_tx = getattr(signed_tx, 'raw_transaction', getattr(signed_tx, 'rawTransaction', None))
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    
    tx_hex = w3.to_hex(tx_hash)
    print(f"✔ Transaction Broadcasted! Tx Hash: {tx_hex}")
    print("  Waiting for Sepolia block confirmation...")
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✔ Confirmed in block {receipt.blockNumber}!")
    print(f"🔗 Etherscan Link: https://sepolia.etherscan.io/tx/{tx_hex}")


if __name__ == "__main__":
    # Expect image path from command line arguments
    if len(sys.argv) > 1:
        IMAGE_PATH = sys.argv[1]
    else:
        IMAGE_PATH = input("Drag and drop your image file here and press Enter: ").strip('"')

    matched_post = process_and_search(IMAGE_PATH)
    anchor_and_verify(matched_post)