import numpy as np
from mzi import SimulatedMZI
from alice import Alice, PHASE_TABLE, INPUT_STATE
from protocol import BB84

np.random.seed(42)

def part1_mzi_physics():
    print("=" * 60)
    print("PART 1: Mach-Zehnder Interferometer Physics")
    print("=" * 60)

    mzi = SimulatedMZI()
    phases = [
        (0,         "0",     "basis 0, bit 0"),
        (np.pi,     "π",     "basis 0, bit 1"),
        (np.pi / 2, "π/2",   "basis 1, bit 0"),
        (3*np.pi/2, "3π/2",  "basis 1, bit 1"),
    ]

    for phi, label, desc in phases:
        out = mzi.apply_phase(phi, INPUT_STATE)
        p0, p1 = np.abs(out[0])**2, np.abs(out[1])**2
        print(f"\n  φ = {label:>4s}  ({desc})")
        print(f"    output state: [{out[0]:.4f}, {out[1]:.4f}]")
        print(f"    P(det 0) = {p0:.4f},  P(det 1) = {p1:.4f}")

    print()

def part2_key_distribution():
    """Run BB84 and show key distribution statistics."""
    print("=" * 60)
    print("PART 2: BB84 Key Distribution")
    print("=" * 60)

    bb84 = BB84()
    result = bb84.distribute_key(n_photons=200)
    stats = result["stats"]

    print(f"\n  Photons sent:       {stats['photons_sent']}")
    print(f"  Basis matches:      {stats['basis_matches']} ({stats['match_rate']})")
    print(f"  Sifted key length:  {stats['sifted_key_length']}")
    print(f"  Keys agree:         {stats['key_agreement']}")
    print(f"\n  Alice's key (first 20): {result['alice_key'][:20]}")
    print(f"  Bob's key   (first 20): {result['bob_key'][:20]}")
    print()

def part3_secure_message():
    """Send 'Hello Bob' encrypted with a quantum-distributed key."""
    print("=" * 60)
    print("PART 3: Secure Message — 'Hello Bob'")
    print("=" * 60)

    bb84 = BB84()
    result = bb84.send_secure_message("Hello Bob")

    print(f"\n  Original:    {result['original']}")
    print(f"  Ciphertext:  {result['ciphertext_preview']}...")
    print(f"  Decrypted:   {result['decrypted']}")
    print(f"  Key length:  {result['key_stats']['sifted_key_length']}")
    print(f"  Keys agree:  {result['key_stats']['key_agreement']}")

    if result["success"]:
        print("\n  *** SUCCESS — Bob read the message! ***")
    else:
        print("\n  *** FAILURE — message corrupted ***")
    print()

if __name__ == "__main__":
    part1_mzi_physics()
    part2_key_distribution()
    part3_secure_message()