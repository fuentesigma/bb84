"""Mach-Zehnder Interferometer — the physics engine.

Only file that changes when swapping simulated ↔ real hardware.
"""
from abc import ABC, abstractmethod
import numpy as np

class MZI(ABC):
    @abstractmethod
    def apply_phase(self, phase: float, input_state: np.ndarray) -> np.ndarray:
        """Propagate *input_state* through the MZI with the given phase shift."""

    @abstractmethod
    def detect(self, output_state: np.ndarray) -> int:
        """Born-rule measurement → detector index (0 or 1)."""

class SimulatedMZI(MZI):
    BS = (1 / np.sqrt(2)) * np.array([[1, 1j], [1j, 1]], dtype=complex)

    @staticmethod
    def phase_shifter(phi: float) -> np.ndarray:
        return np.array([[1, 0], [0, np.exp(1j * phi)]], dtype=complex)

    def apply_phase(self, phase: float, input_state: np.ndarray) -> np.ndarray:
        M = self.BS @ self.phase_shifter(phase) @ self.BS
        return M @ input_state

    def detect(self, output_state: np.ndarray) -> int:
        probs = np.abs(output_state) ** 2
        probs /= probs.sum()
        return int(np.random.choice(len(probs), p=probs))