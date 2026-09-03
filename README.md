<div align="center">

# 🌴 Hacker House Goa 2026 — Task 3
### Decentralized Identity & On-Chain Visual Proof Pipeline

[![GitHub License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Ethereum Sepolia](https://img.shields.io/badge/network-Sepolia_Testnet-627EEA.svg)](https://sepolia.etherscan.io/)
[![Streamlit App](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)

*An automated end-to-end pipeline that extracts photo EXIF metadata, executes live visual reverse web searches for social profiles, and anchors cryptographic proof on the Ethereum Sepolia blockchain.*

[Features](#-key-features) • [Architecture](#-system-architecture) • [Quickstart](#-quickstart) • [Verification](#-on-chain-verification) • [Known Limitations](#-known-limitations)

---

</div>

## 📌 Overview

This repository contains the complete implementation for **Task 3** submitted at **Hacker House Goa 2026**. The application provides a seamless bridge between visual web intelligence and decentralized, tamper-evident proof records.

> **How it works:** A target photo is analyzed locally for technical EXIF metadata. The pipeline streams the photo to execute a live reverse web search via Google Lens, extracting real-world social footprints. The resulting match payload is hashed (`keccak256`) and anchored permanently on the Sepolia Ethereum testnet.

---

## ⚡ Key Features

| Feature | Description | Tech Stack |
| :--- | :--- | :--- |
| **EXIF Parsing** | Extracts image dimensions, camera make/model, format, and timestamp locally. | `PIL.ExifTags` |
| **Live Web Profiling** | Performs real-time reverse image lookup without hardcoded mock results. | `SerpApi` (Google Lens) |
| **Payload Hashing** | Computes deterministic `bytes32` cryptographic digests of target profile data. | `Web3.py` (`keccak256`) |
| **On-Chain Anchoring** | Signs & broadcasts proof transactions directly to smart contract state storage. | Ethereum Sepolia |
| **HHGoa Retro UI** | Interactive dashboard styled with signature green, hot-pink, and yellow branding. | Streamlit + Custom CSS |

---

## 🏗 System Architecture

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


## 🚀 Quickstart

### 1. Prerequisites

Ensure you have **Python 3.10 or higher** installed.

### 2. Installation

Clone the repository and install required packages:

```bash
git clone [https://github.com/AaliyaKhan25/faceidhhgoa.git](https://github.com/AaliyaKhan25/faceidhhgoa.git)
cd faceidhhgoa
pip install -r requirements.txt

Step 3: Environment Setup
Create a .env file in the root project directory:

# Web Search & Hosting API Keys
SERPAPI_KEY=your_serpapi_key_here
IMGBB_API_KEY=your_imgbb_key_here

# Blockchain Credentials
RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
PRIVATE_KEY=your_sepolia_private_key
CONTRACT_ADDRESS=your_deployed_contract_address
🖥️ Step 4: Run the Pipeline
Launch the interactive local web dashboard:

Bash
python -m streamlit run app.py
Navigate to http://localhost:8501 in your browser.

🔍 Verification & Constraints
⛓️ On-Chain Verification Procedure
To demonstrate re-verification of the data against the on-chain record:

1. Execute Pipeline
Upload a target image and hit 🚀 RUN GOA PIPELINE.

2. Extract Hashes
Copy the generated Transaction Hash or Data Hash (bytes32).

3. Inspect Block Explorer
Open Sepolia Etherscan and inspect the transaction logs.

4. Query Contract State
Interact with the deployed contract's verifyMatch view function using the payload digest to confirm state matching.

⚠️ Known System Limitations
📈 SerpApi Rate Limits
Free-tier keys are subject to a strict quota limit of 250 queries/month.

⏱️ Network Dynamics
Sepolia block confirmation delays (~12–15 seconds) are dependent on Ethereum testnet congestion.

🖼️ Metadata Stripping
Social media platforms (e.g., WhatsApp, X, Instagram) automatically strip EXIF metadata from uploaded photos prior to distribution.