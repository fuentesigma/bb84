import numpy as np

class QuantumChannel:
    def __init__(self, error_rate: float = 0.0):
        self.error_rate = error_rate

    def transmit(self, state: np.ndarray) -> np.ndarray:
        if self.error_rate > 0 and np.random.random() < self.error_rate:
            return state[::-1].copy()
        return state.copy()

class ClassicalChannel:
    @staticmethod
    def send_bases(bases: np.ndarray) -> np.ndarray:
        return bases.copy()

    @staticmethod
    def send_bits(bits: list[int]) -> list[int]:
        return list(bits)