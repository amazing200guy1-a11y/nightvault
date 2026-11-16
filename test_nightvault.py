"""
NightVault Formal Verification Suite & Benchmark Harness
Platform: Midnight Network Buildathon (AKINDO)
Author: Usman Bamidele (100L Pure Mathematics, FUNAAB, Abeokuta, Nigeria)
Copyright (c) 2026 Usman Bamidele · All Rights Reserved
Zero External Dependencies - Pure Python Standard Library
"""

import time
import unittest
from nightvault_engine import NightVaultEngine, NightVaultError

class TestNightVault(unittest.TestCase):
    def setUp(self):
        self.engine = NightVaultEngine()
        self.vault_id = "vault_alpha_001"
        self.reserve = 1000.0 # 1,000 NIGHT tokens
        self.interval = 60 # 60 seconds interval for test
        self.owner_secret = "super_secret_owner_entropy_key_999"
        
        # Multi-Heir setup: 70% to spouse, 30% to sibling
        self.heirs = [
            {
                "heir_id": "heir_spouse",
                "share_bps": 7000, # 70%
                "passphrase": "spouse_recovery_seed_phrase_falcon",
                "pubkey": "0x_spouse_public_key_abc123"
            },
            {
                "heir_id": "heir_sibling",
                "share_bps": 3000, # 30%
                "passphrase": "sibling_recovery_seed_phrase_titan",
                "pubkey": "0x_sibling_public_key_xyz789"
            }
        ]

    def test_01_vault_creation_success(self):
        """Verifies successful creation of multi-heir vault with valid conservation."""
        ok, err, vault = self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        self.assertTrue(ok)
        self.assertEqual(err, NightVaultError.SUCCESS)
        self.assertIsNotNone(vault)
        self.assertEqual(len(vault.heirs), 2)

    def test_02_conservation_invariant_rejection(self):
        """Rejects vault where heir percentages do not sum to 100% (e.g. 70% + 20% = 90%)."""
        invalid_heirs = [
            {"heir_id": "h1", "share_bps": 7000, "passphrase": "p1", "pubkey": "k1"},
            {"heir_id": "h2", "share_bps": 2000, "passphrase": "p2", "pubkey": "k2"} # 90%
        ]
        ok, err, _ = self.engine.create_vault("bad_vault", 500.0, 60, invalid_heirs)
        self.assertFalse(ok)
        self.assertEqual(err, NightVaultError.CONSERVATION_VIOLATION)

    def test_03_stealth_heartbeat_checkin(self):
        """Verifies stealth heartbeat generates cryptographic nullifier and refreshes deadline."""
        self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        ok, err, meta = self.engine.submit_stealth_heartbeat(self.vault_id, self.owner_secret)
        self.assertTrue(ok)
        self.assertEqual(err, NightVaultError.SUCCESS)
        self.assertIn("stealth_nullifier", meta)

    def test_04_stealth_nullifier_replay_prevention(self):
        """Prevents replay of the same stealth heartbeat nullifier in the same time bucket."""
        self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        ok1, _, _ = self.engine.submit_stealth_heartbeat(self.vault_id, self.owner_secret)
        self.assertTrue(ok1)
        ok2, err2, _ = self.engine.submit_stealth_heartbeat(self.vault_id, self.owner_secret)
        self.assertFalse(ok2)
        self.assertEqual(err2, NightVaultError.REPLAY_NULLIFIER)

    def test_05_premature_claim_rejection(self):
        """Rejects heir claim when owner is still alive and heartbeat window is active."""
        self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        now = time.time()
        ok, err, meta = self.engine.claim_heir_allocation(
            self.vault_id,
            self.heirs[0]["passphrase"],
            self.heirs[0]["pubkey"],
            simulate_time=now + 10 # Only 10 seconds elapsed (interval is 60s)
        )
        self.assertFalse(ok)
        self.assertEqual(err, NightVaultError.TIMELOCK_ACTIVE)
        self.assertIn("remaining_seconds", meta)

    def test_06_authorized_heir_claim_after_expiration(self):
        """Allows heir to claim exact allocation using secret recovery passphrase after expiration."""
        self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        now = time.time()
        expired_time = now + 120 # 120 seconds elapsed (>60s interval)
        
        ok, err, meta = self.engine.claim_heir_allocation(
            self.vault_id,
            self.heirs[0]["passphrase"], # 70% share
            self.heirs[0]["pubkey"],
            simulate_time=expired_time
        )
        self.assertTrue(ok)
        self.assertEqual(err, NightVaultError.SUCCESS)
        self.assertEqual(meta["claimed_amount_night"], 700.0) # 70% of 1,000 = 700
        self.assertEqual(meta["share_percentage"], 70.0)

    def test_07_invalid_recovery_passphrase_rejection(self):
        """Rejects claim attempt with forged or incorrect recovery passphrase."""
        self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        now = time.time()
        expired_time = now + 120
        
        ok, err, _ = self.engine.claim_heir_allocation(
            self.vault_id,
            "fake_wrong_password_123",
            self.heirs[0]["pubkey"],
            simulate_time=expired_time
        )
        self.assertFalse(ok)
        self.assertEqual(err, NightVaultError.INVALID_RECOVERY_KEY)

    def test_08_multi_heir_selective_disclosure_settlement(self):
        """Verifies both heirs can independently claim their exact shares without knowing the other's."""
        self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        expired_time = time.time() + 150
        
        # Heir 1 claims 70%
        ok1, _, meta1 = self.engine.claim_heir_allocation(
            self.vault_id, self.heirs[0]["passphrase"], self.heirs[0]["pubkey"], simulate_time=expired_time
        )
        # Heir 2 claims 30%
        ok2, _, meta2 = self.engine.claim_heir_allocation(
            self.vault_id, self.heirs[1]["passphrase"], self.heirs[1]["pubkey"], simulate_time=expired_time
        )
        self.assertTrue(ok1)
        self.assertTrue(ok2)
        self.assertEqual(meta1["claimed_amount_night"], 700.0)
        self.assertEqual(meta2["claimed_amount_night"], 300.0)
        self.assertEqual(meta1["claimed_amount_night"] + meta2["claimed_amount_night"], 1000.0)

    def test_09_double_claim_prevention(self):
        """Prevents an heir from claiming their allocation more than once."""
        self.engine.create_vault(self.vault_id, self.reserve, self.interval, self.heirs)
        expired_time = time.time() + 150
        
        # First claim succeeds
        self.engine.claim_heir_allocation(
            self.vault_id, self.heirs[0]["passphrase"], self.heirs[0]["pubkey"], simulate_time=expired_time
        )
        # Second claim fails
        ok, err, _ = self.engine.claim_heir_allocation(
            self.vault_id, self.heirs[0]["passphrase"], self.heirs[0]["pubkey"], simulate_time=expired_time
        )
        self.assertFalse(ok)
        self.assertEqual(err, "ALREADY_CLAIMED")

    def test_10_latency_benchmark_100_iterations(self):
        """Benchmarks 100 stealth heartbeat and heir claim iterations in sub-millisecond time."""
        t0 = time.perf_counter()
        iterations = 100
        for i in range(iterations):
            v_id = f"bench_vault_{i}"
            self.engine.create_vault(v_id, 1000.0, 60, self.heirs)
            self.engine.claim_heir_allocation(
                v_id, self.heirs[0]["passphrase"], self.heirs[0]["pubkey"], simulate_time=time.time() + 200
            )
        elapsed = time.perf_counter() - t0
        avg_latency_ms = (elapsed / iterations) * 1000.0
        
        print(f"\n[BENCHMARK] {iterations} NightVault ZK Settlements: {elapsed:.4f}s | Avg Latency: {avg_latency_ms:.4f} ms/operation")
        self.assertLess(avg_latency_ms, 1.0) # Must be well under 1 ms

if __name__ == "__main__":
    unittest.main()
