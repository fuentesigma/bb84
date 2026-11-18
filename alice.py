from __future__ import annotations
import numpy as np
from mzi import SimulatedMZI

# BB84 phase-encoding table
# (basis, bit) -> phase phi_A
PHASE_TABLE = {
    (0, 0): 0,
    (0, 1): np.pi,
    (1, 0): np.pi / 2,
    (1, 1): 3 * np.pi / 2,
}

# Photon always enters port 0
INPUT_STATE = np.array([1, 0], dtype=complex)

class Alice:
    def __init__(self, mzi: SimulatedMZI | None = None):
        self.mzi = mzi or SimulatedMZI()

    def random_bits(self, n: int) -> np.ndarray:
        return np.random.randint(0, 2, size=n)

    def prepare_photon(self, bit: int, basis: int) -> np.ndarray:
        phase = PHASE_TABLE[(basis, bit)]
        return self.mzi.apply_phase(phase, INPUT_STATE)

    @staticmethod
    def text_to_bits(text: str) -> list[int]:
        bits = []
        for ch in text:
            byte = format(ord(ch), '08b')
            bits.extend(int(b) for b in byte)
        return bits

    @staticmethod
    def encrypt_message(message: str, key: list[int]) -> list[int]:
        msg_bits = Alice.text_to_bits(message)
        if len(key) < len(msg_bits):
            raise ValueError(
                f"Key too short: need {len(msg_bits)} bits, have {len(key)}"
            )
        return [m ^ k for m, k in zip(msg_bits, key)]