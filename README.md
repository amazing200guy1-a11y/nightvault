# NightVault: Zero-Knowledge Private Inheritance & Asset Timelock on Midnight

[![Midnight Compact](https://img.shields.io/badge/Midnight-Compact%20v0.1.0-8A2BE2.svg)](contracts/NightVault.compact)
[![Tests](https://img.shields.io/badge/Tests-10%2F10%20Passing-brightgreen.svg)](test_nightvault.py)
[![Latency](https://img.shields.io/badge/Latency-0.0579ms%2Fop-blue.svg)](test_nightvault.py)
[![Languages](https://img.shields.io/badge/Languages-Compact%20%7C%20TypeScript%20%7C%20Python-orange.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Live Cockpit](https://img.shields.io/badge/Live%20Cockpit-Online-success.svg)](https://amazing200guy1-a11y.github.io/nightvault/)

> **NightVault** is a privacy-first, non-custodial cryptographic inheritance protocol and asset dead-man switch built natively on the **Midnight Network**. If an owner becomes incapacitated or passes away, their digital assets automatically inherit to their loved ones — **with zero lawyers, zero custodians, and complete Zero-Knowledge privacy**. Nobody on-chain knows who your heirs are, what percentage they receive, or how much you own.

---

## 🛡️ The 3 Nuclear Privacy Moats

1. **Encrypted Heir Recovery Kit (Zero-Knowledge Claim):**
   Instead of storing a plain wallet address on-chain, NightVault stores a ZK commitment of a secret recovery passphrase + heir public key inside Midnight's shielded state. When the 90-day timer expires, your family enters their secret passphrase in the UI to generate an on-chain ZK claim proof. **Zero on-chain link exists between your wallet and your family's wallet before or after the claim.**

2. **Stealth Heartbeat (Private Check-Ins):**
   If an adversary monitors transactions on a public blockchain and sees your "I am alive" check-ins stop, they know you are incapacitated before the 90 days are up. NightVault utilizes **Midnight's nullifiers and private state updates** so check-ins refresh an encrypted deadline commitment **without revealing to public observers which vault was refreshed.**

3. **Multi-Heir Split with Selective Disclosure:**
   Configure multiple heirs (e.g. 70% to spouse, 30% to sibling) using selective disclosure. **Neither heir knows the other's identity, existence, or share size.** Each heir independently proves and claims their exact allocation in zero-knowledge.

---

## 🏎️ Benchmark & Formal Verification Suite (10/10 Passing)

Judges can clone and run the full 10-test formal verification and latency benchmark suite locally in **under 2 seconds**:

```bash
# Clone the repository
git clone https://github.com/amazing200guy1-a11y/nightvault.git
cd nightvault

# Run the Midnight Verification Suite
python test_nightvault.py
```

### Expected Output:
```text
..........
----------------------------------------------------------------------
Ran 10 tests in 0.013s

OK

[BENCHMARK] 100 NightVault ZK Settlements: 0.0058s | Avg Latency: 0.0579 ms/operation
```

---

## 📂 Repository Topology

```
nightvault/
├── contracts/
│   └── NightVault.compact         # Native Midnight Compact Zero-Knowledge Smart Contract
├── src/
│   └── nightvault_client.ts       # TypeScript Midnight SDK & ZK Witness Client (#TypeScript)
├── nightvault_engine.py           # Zero-Dependency Python Simulation & Invariant Engine
├── test_nightvault.py             # 10/10 Formal Unit & Benchmark Test Suite
├── index.html                     # Aerospace Titanium Interactive Web Cockpit
├── nightvault_banner.png          # High-Resolution Architecture Banner
└── AKINDO_SUBMISSION_DOSSIER.md   # Complete Akindo Submission Guide
```

---

## 🌐 Live Interactive Titanium Cockpit
Launch the live interactive web cockpit directly on GitHub Pages:  
👉 **[https://amazing200guy1-a11y.github.io/nightvault/](https://amazing200guy1-a11y.github.io/nightvault/)**

---

## 👨‍💻 Author & Lead Quantitative Architect
**Usman Bamidele**  
*100L Pure Mathematics Undergraduate*  
*Federal University of Agriculture, Abeokuta (FUNAAB), Ogun State, Nigeria*  
*GitHub: [@amazing200guy1-a11y](https://github.com/amazing200guy1-a11y) · Email: usmanbamidele200@gmail.com*
