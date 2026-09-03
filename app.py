import os
import json
import base64
import requests
import streamlit as st
from dotenv import load_dotenv
from web3 import Web3
from PIL import Image
from PIL.ExifTags import TAGS

load_dotenv()

st.set_page_config(
    page_title="HHGOA 2026 | Task 3 Pipeline",
    page_icon="🌴",
    layout="wide"
)

# --- RETRO GOA BANNER VIBE CSS (#0b4f2c Green + Pink + Yellow) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Space+Mono:wght@700&display=swap');
    
    /* Lush Forest Green Background */
    .stApp {
        background-color: #0b4f2c;
        color: #ffffff;
        font-family: 'Space Mono', monospace;
    }
    
    /* Top Signboard Banner */
    .goa-banner {
        background-color: #ffe600;
        color: #000000;
        border: 4px solid #000000;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 6px 6px 0px #000000;
        margin-bottom: 30px;
    }
    
    .goa-title {
        font-family: 'Fredoka', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #ff007a;
        text-shadow: 2px 2px 0px #000;
        margin: 0;
        text-transform: uppercase;
    }
    
    .goa-tag {
        background-color: #ff007a;
        color: #ffffff;
        font-weight: 700;
        padding: 4px 12px;
        border: 2px solid #000000;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
        font-size: 0.85rem;
    }
    
    /* Yellow & Pink Directional Cards */
    .sign-yellow {
        background-color: #ffe600;
        color: #000000;
        border: 3px solid #000000;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 4px 4px 0px #000000;
    }
    
    .sign-pink {
        background-color: #ff007a;
        color: #ffffff;
        border: 3px solid #000000;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 4px 4px 0px #000000;
    }
    
    /* File Uploader Box Customization */
    .stFileUploader {
        background-color: #0d5f35;
        border: 3px dashed #ffe600;
        border-radius: 10px;
        padding: 10px;
    }

    /* Hot Pink Action Button */
    .stButton>button {
        width: 100%;
        background-color: #ff007a;
        color: #ffffff;
        border: 3px solid #000000;
        border-radius: 8px;
        padding: 14px;
        font-family: 'Fredoka', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        box-shadow: 4px 4px 0px #000000;
        transition: all 0.1s ease;
    }
    .stButton>button:hover {
        background-color: #ffe600;
        color: #000000;
        box-shadow: 2px 2px 0px #000000;
        transform: translate(2px, 2px);
    }
    
    /* Code overrides */
    code {
        background-color: #000000 !important;
        color: #ffe600 !important;
        border-radius: 4px;
        padding: 2px 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Top Banner Header ---
st.markdown("""
    <div class="goa-banner">
        <span class="goa-tag">🌴 HACKER HOUSE GOA 2026 , PRESENTED BY TEAM - GIT COMMITTED</span>
        <h1 class="goa-title">TASK 3: VERIFICATION PIPELINE</h1>
        <p style="font-weight:700; margin-top:5px;">REVERSE SEARCH • METADATA • SEPOLIA ANCHORING</p>
    </div>
""", unsafe_allow_html=True)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
IMGBB_KEY = os.getenv("IMGBB_API_KEY")
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

CONTRACT_ABI = json.loads('''[
    {"inputs":[{"internalType":"string","name":"_postUrl","type":"string"},{"internalType":"bytes32","name":"_dataHash","type":"bytes32"}],"name":"anchorMatch","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"nonpayable","type":"function"}
]''')

def extract_exif_metadata(img_file) -> dict:
    meta = {
        "dimensions": f"{img_file.width}x{img_file.height} px",
        "format": str(img_file.format).upper(),
        "color_mode": img_file.mode
    }
    try:
        exif = img_file._getexif()
        if exif:
            for tag, val in exif.items():
                name = TAGS.get(tag, tag)
                if name in ["Make", "Model", "DateTimeOriginal", "Software"]:
                    meta[str(name).lower()] = str(val)
    except Exception:
        pass
    return meta

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="sign-yellow"><b>🛵 STEP 1: DROP TARGET PHOTO</b></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        pil_img = Image.open(uploaded_file)
        st.image(pil_img, use_container_width=True)
        
        st.markdown('<div class="sign-yellow" style="margin-top:15px;"><b>📊 EXIF IMAGE METADATA</b></div>', unsafe_allow_html=True)
        st.json(extract_exif_metadata(pil_img))

with col2:
    st.markdown('<div class="sign-pink"><b>🌊 STEP 2: EXECUTE VERIFICATION PIPELINE</b></div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        if st.button("🚀 RUN GOA PIPELINE", type="primary"):
            try:
                # 1. Cloud Host Upload
                with st.spinner("Uploading photo payload..."):
                    uploaded_file.seek(0)
                    if IMGBB_KEY:
                        b64_img = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                        res = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_KEY, "image": b64_img}, timeout=10)
                        image_public_url = res.json()["data"]["url"]
                    else:
                        res = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": uploaded_file.getvalue()}, timeout=10)
                        image_public_url = res.json()["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")

                # 2. SerpApi Web Profile Match
                with st.spinner("Searching Google Lens index..."):
                    params = {"engine": "google_lens", "url": image_public_url, "api_key": SERPAPI_KEY}
                    lens_resp = requests.get("https://serpapi.com/search", params=params, timeout=12).json()
                    matches = lens_resp.get("visual_matches", [])

                    if not matches:
                        st.error("❌ No visual match found in web index.")
                        st.stop()

                    top_match = matches[0]
                    post_url = top_match.get("link", "Unknown Link")
                    title = top_match.get("title", "Matched Profile")
                    domain = top_match.get("source", "Unknown Domain")

                st.markdown(f"""
                <div class="sign-yellow">
                    <h3 style="margin:0 0 10px 0; color:#ff007a;">🎯 PERSON / PROFILE MATCHED</h3>
                    <p style="margin:2px 0;"><b>TARGET:</b> {title}</p>
                    <p style="margin:2px 0;"><b>PLATFORM:</b> {domain}</p>
                    <p style="margin:2px 0;"><b>LINK:</b> <a href="{post_url}" target="_blank" style="color: #000; text-decoration: underline;">{post_url}</a></p>
                </div>
                """, unsafe_allow_html=True)

                # 3. Sepolia On-Chain Write
                with st.spinner("Anchoring proof on Sepolia..."):
                    w3 = Web3(Web3.HTTPProvider(RPC_URL))
                    contract_addr = w3.to_checksum_address(CONTRACT_ADDRESS)
                    account = w3.eth.account.from_key(PRIVATE_KEY)
                    contract = w3.eth.contract(address=contract_addr, abi=CONTRACT_ABI)

                    payload = f"{post_url}:{title}".encode('utf-8')
                    data_hash = w3.solidity_keccak(['bytes'], [payload])

                    tx = contract.functions.anchorMatch(post_url, data_hash).build_transaction({
                        'chainId': 11155111,
                        'gas': 200000,
                        'maxFeePerGas': w3.to_wei('35', 'gwei'),
                        'maxPriorityFeePerGas': w3.to_wei('30', 'gwei'),
                        'nonce': w3.eth.get_transaction_count(account.address),
                    })

                    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
                    raw_tx = getattr(signed_tx, 'raw_transaction', getattr(signed_tx, 'rawTransaction', None))
                    tx_hash = w3.eth.send_raw_transaction(raw_tx)
                    tx_hex = w3.to_hex(tx_hash)

                st.balloons()
                st.markdown(f"""
                <div class="sign-pink">
                    <h3 style="margin:0 0 10px 0;">⛓️ SEPOLIA PROOF ANCHORED!</h3>
                    <p><b>TX HASH:</b> <code>{tx_hex}</code></p>
                    <p><b>DATA HASH:</b> <code>{w3.to_hex(data_hash)}</code></p>
                    <a href="https://sepolia.etherscan.io/tx/{tx_hex}" target="_blank" style="color: #ffe600; font-weight:700; text-decoration: underline;">
                        👉 View Confirmed Proof on Sepolia Etherscan
                    </a>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Pipeline Error: {e}")