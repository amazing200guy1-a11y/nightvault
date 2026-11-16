# NightVault — Akindo Midnight Buildathon Submission Dossier

**Target Buildathon:** Build Privacy-First Apps on Midnight  
**Platform:** AKINDO (`https://app.akindo.io/wave-hacks/jaMZjqPOBsLXvjdG`)  
**Prize Pool:** 12,500 USDT (Wave Grants)  
**Author:** Usman Bamidele (100L Pure Mathematics, FUNAAB, Abeokuta, Nigeria)  
**GitHub:** [amazing200guy1-a11y](https://github.com/amazing200guy1-a11y)  
**Repository:** [https://github.com/amazing200guy1-a11y/nightvault](https://github.com/amazing200guy1-a11y/nightvault)  
**Live Cockpit:** [https://amazing200guy1-a11y.github.io/nightvault/](https://amazing200guy1-a11y.github.io/nightvault/)  
**Smart Contract:** `contracts/NightVault.compact` (Midnight Compact v0.1.0)  

---

## 1. Project Metadata
- **Product Name:** NightVault
- **Tagline:** Zero-Knowledge Private Inheritance & Asset Timelock on Midnight — non-custodial family dead-man switch with stealth heartbeats and encrypted heir recovery.
- **Categories:** Privacy & Security, Market Infrastructure, Other
- **Tags:** #TypeScript #Compact #Zero-Knowledge #Python

---

## 2. Core Privacy Moats
1. **Encrypted Heir Recovery Kit (Zero-Knowledge Claim):**
   Heir identity is stored solely as a ZK commitment `Hash(secretPassphrase + heirPubKey)` in Midnight's shielded state. Zero on-chain link exists between the owner's wallet and family wallets before or after a claim.
2. **Stealth Heartbeat (Private Check-Ins):**
   Nullifier-based private deadline refresh prevents blockchain observers from monitoring when an owner checks in or detecting incapacitation.
3. **Multi-Heir Split with Selective Disclosure:**
   Enforces exact share allocations (e.g. 70% to spouse, 30% to sibling) where neither beneficiary is aware of the other's share, identity, or existence.

---

## 3. Test Verification
```bash
git clone https://github.com/amazing200guy1-a11y/nightvault.git
cd nightvault
python test_nightvault.py
```
- Benchmark: 10/10 tests pass in 0.013s (0.0579 ms/op).
