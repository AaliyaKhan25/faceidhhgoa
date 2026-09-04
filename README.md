# 🌴 HHGOA 2026 — Task 3 [Face Identification & Blockchain Verification]

## 📌 Overview
An automated end-to-end pipeline built for **Hacker House Goa 2026** that extracts local photo EXIF metadata, executes live visual reverse web searches for social profiles, and anchors cryptographic proof on the Ethereum Sepolia blockchain.

---

## ⚡ Key Features

### 📸 EXIF Parsing
Extracts image dimensions, camera make/model, format, and timestamp locally using `PIL.ExifTags`.

### 🔍 Live Web Profiling
Performs real-time reverse image lookup without hardcoded mock results using `SerpApi` (Google Lens engine).

### 🔐 Payload Hashing
Computes deterministic `bytes32` cryptographic digests (`keccak256`) of target profile data using `Web3.py`.

### ⛓️ On-Chain Anchoring
Signs and broadcasts proof transactions directly to smart contract state storage on the Ethereum Sepolia Testnet.

### 🎨 HHGoa Retro UI
Interactive dashboard styled with signature forest green (`#0b4f2c`), hot-pink (`#ff007a`), and yellow (`#ffe600`) tropical branding built with Streamlit.

---

## 🚀 Quickstart

### 1. Prerequisites
Ensure you have **Python 3.10 or higher** installed.

### 2. Installation
Clone the repository and install required packages:

    git clone https://github.com/AaliyaKhan25/faceidhhgoa.git
    cd faceidhhgoa
    pip install -r requirements.txt

### 3. Environment Setup
Create a `.env` file in the root project directory:

    SERPAPI_KEY=your_serpapi_key_here
    IMGBB_API_KEY=your_imgbb_key_here
    RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
    PRIVATE_KEY=your_sepolia_private_key
    CONTRACT_ADDRESS=your_deployed_contract_address

### 4. Run the Pipeline
Launch the interactive local web dashboard:

    python -m streamlit run app.py

Navigate to `http://localhost:8501` in your browser.

### 5. System Architecture 
[ Input Photo ]
│
├──► 1. Local EXIF Extractor ──► Dimensions, Camera Model, Timestamp
│
├──► 2. Cloud Upload Stream  ──► Hosted Payload Endpoint
│
└──► 3. Google Lens Query ───► Verified Social Profile URL & Metadata
│
▼
4. Keccak256 Hashing
│
▼
5. Ethereum Sepolia Smart Contract
(anchorMatch / verifyMatch)

---

## ⛓️ On-Chain Verification

### 1. Execute Pipeline
Upload a target image and hit **🚀 RUN GOA PIPELINE**.

### 2. Extract Hashes
Copy the generated **Transaction Hash** or **Data Hash** (`bytes32`).

### 3. Inspect Block Explorer
Open Sepolia Etherscan (https://sepolia.etherscan.io/) and inspect the transaction logs.

### 4. Query Contract State
Interact with the deployed contract's `verifyMatch` view function using the payload digest to confirm state matching.

---

⚠️ Known Limitations & Troubleshooting
📈 SerpApi Rate Limits: Free-tier API accounts are limited to 250 queries per month. If you receive a 429 error, check your dashboard usage.
⏱️ Sepolia Block Latency: On-chain write confirmation times depend on testnet block times (~12–15 seconds). The UI may hang briefly while waiting for the transaction receipt.
🖼️ EXIF Stripping: Photos shared via social media platforms (e.g., WhatsApp, Discord, Instagram) usually have EXIF metadata stripped prior to processing. Use original camera files for best results.
🔌 RPC Node Failures: If your Alchemy or Infura RPC endpoint throws connection errors, ensure your API key is active and your network allows WebSocket/HTTP connections to external nodes.
