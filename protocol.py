from __future__ import annotations
import numpy as np
from alice import Alice
from bob import Bob
from channel import QuantumChannel, ClassicalChannel

class BB84:
    def __init__(self, error_rate: float = 0.0):
        self.alice = Alice()
        self.bob = Bob()
        self.quantum_channel = QuantumChannel(error_rate=error_rate)
        self.classical_channel = ClassicalChannel()

    def distribute_key(
        self, n_photons: int = 200, required_bits: int | None = None
    ) -> dict:

        # Step 1 — Alice generates random bits and bases
        alice_bits = self.alice.random_bits(n_photons)
        alice_bases = self.alice.random_bits(n_photons)

        # Step 2 — Bob chooses random measurement bases
        bob_bases = self.bob.random_bases(n_photons)

        # Step 3 — Alice prepares & sends; Bob measures
        bob_bits = np.zeros(n_photons, dtype=int)
        for i in range(n_photons):
            photon = self.alice.prepare_photon(int(alice_bits[i]), int(alice_bases[i]))
            transmitted = self.quantum_channel.transmit(photon)
            bob_bits[i] = self.bob.measure_photon(transmitted, int(bob_bases[i]))

        # Step 4 — Basis reconciliation (classical channel)
        announced_bases = self.classical_channel.send_bases(alice_bases)
        matching = announced_bases == bob_bases

        # Step 5 — Sift: keep only matching-basis bits
        alice_key = [int(alice_bits[i]) for i in range(n_photons) if matching[i]]
        bob_key = [int(bob_bits[i]) for i in range(n_photons) if matching[i]]

        # Step 6 — (Optional) trim to required length
        if required_bits is not None:
            alice_key = alice_key[:required_bits]
            bob_key = bob_key[:required_bits]

        stats = {
            "photons_sent": n_photons,
            "basis_matches": int(matching.sum()),
            "match_rate": f"{matching.mean():.1%}",
            "sifted_key_length": len(alice_key),
            "key_agreement": alice_key == bob_key,
        }
        return {"alice_key": alice_key, "bob_key": bob_key, "stats": stats}

    def send_secure_message(self, message: str, n_photons: int = 0) -> dict:
        msg_bits_needed = len(message) * 8

        # Need ~4× message bits (expect ~50% basis match)
        if n_photons == 0:
            n_photons = max(200, msg_bits_needed * 4)

        result = self.distribute_key(n_photons, required_bits=msg_bits_needed)
        alice_key = result["alice_key"]
        bob_key = result["bob_key"]

        # Encrypt with Alice's key
        ciphertext = self.alice.encrypt_message(message, alice_key)

        # Transmit over classical channel
        received = self.classical_channel.send_bits(ciphertext)

        # Decrypt with Bob's key
        decrypted = self.bob.decrypt_message(received, bob_key)

        return {
            "original": message,
            "decrypted": decrypted,
            "success": message == decrypted,
            "ciphertext_preview": ciphertext[:32],
            "key_stats": result["stats"],
        }