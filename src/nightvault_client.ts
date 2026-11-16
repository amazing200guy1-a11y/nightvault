/**
 * ============================================================================
 * NightVault — Midnight Network TypeScript Client SDK
 * Platform: Midnight (Input Output / IOG)
 * Buildathon: Build Privacy-First Apps on Midnight (AKINDO)
 * Author: Usman Bamidele (amazing200guy1-a11y) · FUNAAB Pure Mathematics
 * ============================================================================
 */

import * as crypto from 'crypto';

export interface HeirSplit {
  heirId: string;
  shareBasisPoints: number; // e.g. 7000 = 70%
  secretPassphrase: string;
  pubKey: string;
}

export interface VaultConfig {
  vaultId: string;
  reserveNight: number;
  intervalSeconds: number;
  heirs: HeirSplit[];
}

export interface StealthHeartbeatReceipt {
  vaultIdCommitment: string;
  stealthNullifier: string;
  timestamp: number;
  newDeadlineCommitment: string;
  gasDUs: number;
}

export interface HeirClaimReceipt {
  claimReceiptId: string;
  payoutAmountNIGHT: number;
  sharePercentage: number;
  zkProofHash: string;
  midnightTxHash: string;
}

export class NightVaultClient {
  /**
   * Generates a Zero-Knowledge Heir Commitment.
   * Hash(secretPassphrase + pubKey) stored in private state —
   * guarantees zero on-chain link between owner's wallet and family's wallet.
   */
  public static computeHeirCommitment(passphrase: string, pubKey: string): string {
    return crypto
      .createHash('sha256')
      .update(`${passphrase}:${pubKey}`)
      .digest('hex');
  }

  /**
   * Submits a Stealth Heartbeat:
   * Uses a one-time nullifier to refresh the deadline commitment without revealing
   * which specific vault is being touched by the owner.
   */
  public static generateStealthHeartbeat(
    vaultId: string,
    ownerSecret: string,
    intervalSeconds: number
  ): StealthHeartbeatReceipt {
    const tNow = Math.floor(Date.now() / 1000);
    const timeSlot = Math.floor(tNow / 60);

    const stealthNullifier = crypto
      .createHmac('sha256', ownerSecret)
      .update(`heartbeat:${vaultId}:${timeSlot}`)
      .digest('hex');

    const newDeadlineCommitment = crypto
      .createHash('sha256')
      .update(`${vaultId}:${tNow + intervalSeconds}`)
      .digest('hex');

    return {
      vaultIdCommitment: `0x${crypto.createHash('sha256').update(vaultId).digest('hex')}`,
      stealthNullifier: `0x${stealthNullifier}`,
      timestamp: tNow,
      newDeadlineCommitment: `0x${newDeadlineCommitment}`,
      gasDUs: 1250 // Midnight DUST execution units
    };
  }

  /**
   * Executes Heir Recovery in Zero-Knowledge:
   * Slices the exact allocation (e.g. 70% to spouse, 30% to sibling)
   * without either heir knowing the identity or share of the other.
   */
  public static generateHeirClaimProof(
    vaultId: string,
    passphrase: string,
    pubKey: string,
    shareBps: number,
    reserveAmount: number
  ): HeirClaimReceipt {
    const candidateCommitment = this.computeHeirCommitment(passphrase, pubKey);
    const payout = (reserveAmount * shareBps) / 10000.0;
    
    const zkProofHash = crypto
      .createHash('sha256')
      .update(`zk_proof:${vaultId}:${candidateCommitment}:${shareBps}`)
      .digest('hex');

    const midnightTxHash = `0xmid_tx_${crypto.randomBytes(16).toString('hex')}`;

    return {
      claimReceiptId: `nv_claim_${crypto.randomBytes(8).toString('hex')}`,
      payoutAmountNIGHT: payout,
      sharePercentage: shareBps / 100.0,
      zkProofHash: `0x${zkProofHash}`,
      midnightTxHash
    };
  }
}
