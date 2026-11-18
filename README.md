# BB84 Quantum Key Distribution — Mach-Zehnder Simulation

A small Python simulation of the **BB84** quantum key distribution protocol using
**phase encoding** in a Mach-Zehnder interferometer (MZI). Alice encodes random bits
as phase shifts on a single photon, Bob measures in a randomly chosen basis, and the
two sift a shared secret key that is then used as a one-time pad to send a message.

## Requirements

- Python 3.10+
- NumPy

```bash
pip install numpy
```

## Usage

```bash
python main.py
```

The demo runs in three parts (seeded with `np.random.seed(42)` for reproducibility):

1. **MZI physics** — the output state and detector probabilities for each of Alice's
   four encoding phases.
2. **Key distribution** — sends 200 photons, reconciles bases, and reports the sifted
   key length and whether Alice's and Bob's keys agree.
3. **Secure message** — distributes a key long enough to encrypt `"Hello Bob"`,
   XORs the message with it, and has Bob decrypt it.

Example output (abridged):

```
PART 2: BB84 Key Distribution
  Photons sent:       200
  Basis matches:      106 (53.0%)
  Sifted key length:  106
  Keys agree:         True

PART 3: Secure Message — 'Hello Bob'
  Original:    Hello Bob
  Decrypted:   Hello Bob
  Key length:  72
  Keys agree:  True
```

## Physics

The interferometer is modelled as two 50:50 beam splitters around a phase shifter
on one arm:

$$
M(\varphi) = B \, P(\varphi) \, B, \qquad
B = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix}, \qquad
P(\varphi) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\varphi} \end{pmatrix}
$$

The photon always enters port 0, `|ψ_in⟩ = (1, 0)`. Detection follows the Born rule:
detector *k* clicks with probability `|ψ_k|²`.

**Alice's encoding** (basis, bit) → phase:

| Basis | Bit 0 | Bit 1  |
|-------|-------|--------|
| 0     | 0     | π      |
| 1     | π/2   | 3π/2   |

**Bob's measurement** applies phase 0 (basis 0) or π/2 (basis 1) in his own MZI and
reads the detector index as the bit. When the bases match, the result is
deterministic; when they differ, it is a 50/50 coin flip, and those bits are discarded
during sifting. About half the photons survive, so `send_secure_message` sends
roughly 4× as many photons as the message has bits.

## Project structure

| File          | Role |
|---------------|------|
| `mzi.py`      | `MZI` abstract interface and `SimulatedMZI` (beam splitter / phase shifter matrices, Born-rule detection). The only file meant to change when swapping in real hardware. |
| `alice.py`    | `Alice`: random bits and bases, photon preparation, text → bits, XOR encryption. |
| `bob.py`      | `Bob`: random bases, measurement, bits → text, XOR decryption. |
| `channel.py`  | `QuantumChannel` (optional bit-flip noise via `error_rate`) and `ClassicalChannel` (public basis announcement and ciphertext transfer). |
| `protocol.py` | `BB84`: runs the full protocol (`distribute_key`, `send_secure_message`). |
| `main.py`     | Demo script. |

## Programmatic use

```python
from protocol import BB84

bb84 = BB84(error_rate=0.0)
result = bb84.distribute_key(n_photons=500)
print(result["stats"])

msg = bb84.send_secure_message("Hi")
print(msg["decrypted"], msg["success"])
```

## Limitations

- No eavesdropper (Eve) model, and no QBER estimation, error correction or privacy
  amplification. With `error_rate > 0`, Alice's and Bob's keys can differ and the
  message may decrypt incorrectly.
- Message encoding uses 8 bits per character, so only ASCII / Latin-1 text
  round-trips correctly.
