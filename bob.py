from __future__ import annotations
import numpy as np
from mzi import SimulatedMZI

# Bob's phase for each basis choice
BOB_PHASE = {0: 0, 1: np.pi / 2}

class Bob:
    def __init__(self, mzi: SimulatedMZI | None = None):
        self.mzi = mzi or SimulatedMZI()

    def random_bases(self, n: int) -> np.ndarray:
        return np.random.randint(0, 2, size=n)

    def measure_photon(self, state: np.ndarray, basis: int) -> int:
        output = self.mzi.apply_phase(BOB_PHASE[basis], state)
        return self.mzi.detect(output)
    
    @staticmethod
    def bits_to_text(bits: list[int]) -> str:
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            chars.append(chr(int(''.join(str(b) for b in byte), 2)))
        return ''.join(chars)

    @staticmethod
    def decrypt_message(encrypted_bits: list[int], key: list[int]) -> str:
        msg_bits = [c ^ k for c, k in zip(encrypted_bits, key)]
        return Bob.bits_to_text(msg_bits)