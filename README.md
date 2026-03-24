# Linear algebra applications calculator

Small Python utilities for working through homework-style problems: **Markov chains and PageRank**, **singular value decomposition (SVD)** (including image compression), **classical substitution ciphers** (Caesar, affine, Vigenère, and helpers), and **shared helpers** for arrays, images, and cipher-related mappings.

## Installation

From the project root:

```bash
pip install -r requirements_calc.txt
```

`requirements_calc.txt` pins NumPy, matplotlib, and Pillow with a platform marker (`arm64`). If nothing installs on your machine, install the same packages directly:

```bash
pip install numpy matplotlib pillow
```

## Module overview

| Module | Role |
| --- | --- |
| [supplemental_functions.py](supplemental_functions.py) | Build reshaped arrays, load/save images as matrices, letter/binary dictionaries, and block/stream helpers for ciphers. |
| [markov_chains.py](markov_chains.py) | `Markoff_chainz` class: powers of a transition matrix, state evolution, steady state, PageRank-style Google matrix. |
| [SVD.py](SVD.py) | `SVD` class: least squares, \(A^TA\) / \(AA^T\), SVD factors, reconstruction, rank/energy experiments, image compression. |
| [cipher.py](cipher.py) | `cipher` class: Caesar, affine, and Vigenère encode/decode, plus brute-force helpers; uses `blocker` / `hill_scrambler_key` from `supplemental_functions`. |

Import examples:

```python
import numpy as np
from supplemental_functions import numpy_array, image_to_matrix, matrix_to_image
from markov_chains import Markoff_chainz
from SVD import SVD
from cipher import cipher
```

## Quick start

### Markov chain: state after \(n\) steps

Use a **column-stochastic** transition matrix \(A\) (columns sum to 1) and an initial state vector `initial` (same dimension as rows of `A`).

```python
import numpy as np
from markov_chains import Markoff_chainz

A = np.array([
    [0.7, 0.2, 0.0],
    [0.2, 0.5, 0.2],
    [0.1, 0.3, 0.8],
])
x0 = np.array([1.0, 0.0, 0.0])

chain = Markoff_chainz(A)
x5 = chain.time_step_with_initial(5, x0, rounding=4, show=True)
```

### SVD on a small matrix

```python
import numpy as np
from SVD import SVD

A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
svd = SVD(A)
U, s, Vh = svd.checker(show=False)  # same as np.linalg.svd(A)
rebuilt = svd.reconstructor(show=False)
```

### Image compression pipeline (optional)

Use a path to your own image file.

```python
from supplemental_functions import image_to_matrix
from SVD import SVD

# Grayscale: single matrix
gray = image_to_matrix("photo.png", color=False, info=True)
svd_gray = SVD(gray)
svd_gray.image_compression(k=20, color=False, show=True, save=False)

# Color: list of three channel matrices (R, G, B)
channels = image_to_matrix("photo.png", color=True, info=True)
svd_color = SVD(channels)
svd_color.image_compression(k=30, color=True, show=True, save=False)
```

### Classical ciphers (optional)

```python
from cipher import cipher

c = cipher()
encoded = c.ceaser_encode("Hello", 3, show=True)
decoded = c.ceaser_decode(encoded, 3, show=True)

# Affine: multiplier a must be coprime to 26 for decode to work
text = c.affine_encode("affine", my_offset=5, a=7, show=True)
c.affine_decode(text, offset=5, a=7, show=True)
```

---

## supplemental_functions.py

### Arrays

- **`numpy_array(*args, shape, show=True)`**  
  Packs positional scalars into a 1D array, then **`reshape`s** to `shape`. You must pass `shape` as a keyword argument (e.g. `shape=(2, 3)`). Returns the reshaped `ndarray`. If `show=True`, prints the array.

### Images

- **`image_to_matrix(image_file, color=True, info=True)`**  
  Opens an image with Pillow.  
  - `color=True`: returns a **list of three** 2D arrays (R, G, B), each min–max scaled to 0–255.  
  - `color=False`: returns one **grayscale** 2D array (mean across channels).  
  If `info=True`, prints shape information.

- **`matrix_to_image(matrix, color=True, show=True, save=False)`**  
  Builds a Pillow image from a matrix or list of channel matrices (matching `image_to_matrix` conventions). Normalizes per channel, converts to `uint8`, and optionally displays with **matplotlib** (`plt.imshow` / `plt.show()`). If `save=True`, writes **`file_compressed.jpg`** in the current working directory (fixed filename). Returns the Pillow `Image` object.

### Letter and binary maps

All of these use the English alphabet only.

- **`alpha_num_dict(lower=True, upper=False)`** — map letter → index 0–25 (lowercase and/or uppercase).
- **`num_alpha_dict(lower=True, upper=False)`** — map index → letter.
- **`alpha_bin_dict(lower=False, upper=False)`** — letter → 8-bit binary string.
- **`bin_alpha_dict(lower=False, upper=False)`** — binary string → letter.

If both `lower` and `upper` are false, the dict functions follow their `else` branches (see source for which mappings are returned).

### Blocks and stream helpers

- **`blocker(word, block_size, show=True)`** — encodes **lowercase a–z** letters to indices, pads with zeros, and returns a 2D array of shape `(ceil(n/block_size), block_size)` (row layout after padding). Prints the matrix if `show=True`.

- **`hill_scrambler_key(size, show=True)`** — random `size × size` matrix of lowercase letters (for Hill-cipher-style experiments).

- **`stream_scambeler(length=16, show=True)`** — list of `length` random 8-bit binary strings from `alpha_bin_dict(lower=True)`.

- **`brute_reccurance(array)`** — walks prefix lengths and tries to form square matrices; prints shapes and a parity of determinants (exploratory helper).

Minimal extra example:

```python
from supplemental_functions import numpy_array, blocker

M = numpy_array(1, 2, 3, 4, 5, 6, shape=(2, 3), show=False)
B = blocker("abc", 3, show=False)
```

---

## markov_chains.py — `Markoff_chainz`

**Constructor:** `Markoff_chainz(A)`  
`A` should be a square **NumPy** array. The code assumes **column-stochastic** semantics: new state is `A @ initial` (and the Google step uses columns for dangling nodes).

| Method | Purpose |
| --- | --- |
| `matrix_power(power, show=True)` | Returns \(A^{\text{power}}\) by repeated multiplication. Prints result if `show=True`. |
| `time_step_with_initial(time_steps, initial, rounding=4, show=True)` | Returns \(\text{round}(A^{\text{time\_steps}} \cdot \text{initial})\) with `rounding` decimal places. |
| `eigens()` | Prints eigenvalues and eigenvectors of `A`. (For programmatic use of the arrays, prefer `np.linalg.eig` directly.) |
| `steady_state(rounding=4, show=True)` | Finds an eigenvector for eigenvalue \(\approx 1\), normalizes it, returns the **real** part rounded. |
| `smallest_k(num_iters, initial, rounding=4)` | Tries step counts `0 … num_iters-1` until the state matches the steady state; prints the smallest such `k` or a message to increase iterations. |
| `Google(alpha, dangling_node=True, show=True)` | Builds \(G = \alpha \cdot \frac{1}{n}\mathbf{1}\mathbf{1}^T + (1-\alpha) A\). If `dangling_node` is true, **any column of `A` with sum zero is replaced** by a uniform column — this **mutates `self.A` in place**. Returns `G`. |
| `Google_steady_state(alpha, show=True)` | Steady state (eigenvalue 1) of the matrix from `Google`, same style as `steady_state`. |
| `PageRank(alpha, show=True)` | Uses `Google_steady_state`, then returns a **list of page indices from 1 to n**, sorted by descending score (highest rank first). |

---

## cipher.py — `cipher`

**Constructor:** `cipher()` (no required state; methods are stateless aside from printing).

Implements several **substitution ciphers** on Latin letters. Non-letters are copied through unchanged. Uppercase and lowercase are preserved per letter. Method names use the project’s spelling (`ceaser`, `vigenre`) — import and call them exactly as in the source.

| Method | Purpose |
| --- | --- |
| `ceaser_encode(my_message, my_offset, show=True)` | Caesar-style shift. Returns the encoded string. |
| `ceaser_decode(message, offset, show=True)` | Inverse with the same `offset` you used for encoding. Returns the decoded string. |
| `affine_encode(my_message, my_offset, a, show=True)` | Affine map \(x \mapsto \bigl(a \cdot x + \text{offset}\bigr) \bmod 26\) on letter indices. Returns the ciphertext. |
| `affine_decode(message, offset, a, show=True)` | Affine decode using the modular inverse of `a` modulo 26. If `a` has no inverse mod 26, prints a message and returns `None`. |
| `vigenre_encode(new_message, keyword_phrase, show=True)` | Vigenère with the keyword as repeated shifts (only alphabetic keyword letters contribute shifts). |
| `vigenre_decode(new_message, keyword_phrase, show=True)` | Vigenère decryption with the same keyword. |
| `hill(message, key, size)` | Builds a block matrix from `message` via `blocker` and a random `hill_scrambler_key(size)`; **does not use the `key` argument** or return a Hill cipher result in the current implementation. |
| `streamer(message, encrypt=True, show=True)` | **Incomplete** in the current file: only tokenizes and prints partial output when `encrypt=True`. |
| `brutus_breaker(message)` | Prints all 26 Caesar decodes (one `offset` per line) for inspection. |
| `affine_breaker(message)` | Prints affine decodes for all pairs `(a, n)` with `a` and `n` in `0 … 25` where `affine_decode` succeeds (skips `a` with no inverse). |

---

## SVD.py — `SVD`

**Constructor:** `SVD(A)`  
- For matrix experiments, `A` is a 2D NumPy `ndarray`.  
- For **`image_compression(..., color=True)`**, pass **`A` as a list of three** 2D channel matrices (as returned by `image_to_matrix(..., color=True)`).

| Method | Purpose |
| --- | --- |
| `least(b)` | `np.linalg.lstsq(self.A, b)` — ordinary least squares. |
| `ATA(show=True)` | Returns \(A^T A\); optional print. |
| `AAT(show=True)` | Returns \(A A^T\); optional print. |
| `eigens(show=True)` | Eigenpairs of \(A^TA\) and \(AA^T\); returns `(right_eigenvalue, right_eigenvector, left_eigenvalue, left_eigenvector)`. |
| `norm()` | `np.linalg.norm(self.A)` (Frobenius norm for 2D arrays). |
| `checker(show=True)` | `U, S, V = np.linalg.svd(self.A)` (NumPy’s third matrix is \(V^H\) / `Vh` in newer NumPy docs). |
| `U(show=True)` | Left singular vectors from `checker`. |
| `S(recon_matrix=None, show=True)` | If `recon_matrix` is `None`, builds a full \(\Sigma\) with singular values on the diagonal (same shape as `A`). If you pass a 1D array of singular values, it fills the diagonal the same way. |
| `V(show=True)` | Third factor from `checker`. |
| `reconstructor(reduced_S=None, show=True)` | Computes `U @ S @ V` with optional **custom** diagonal `reduced_S` (full-sized \(\Sigma\)). |
| `smallest_reduction(norm_value, show=True)` | Zeros smallest singular values iteratively until \(\|A - A_k\|\) drops below `norm_value`; prints the last error, index, and \(A_k\) (does not return a value in the current implementation). |
| `min_singular_compression(target_percent, singular_values=None, show=True)` | Uses **squared** singular values as energy; drops smallest until a printed “quality retained” crosses the strategy implied by `target_percent`. |
| `k_many_reduction_variance(k, singular_values=None, rebuild=True, show=True)` | Reports variance/energy retained when keeping `k` singular values (squared-energy accounting); with default SVD and `rebuild=True`, may return a list of singular-value-related values for rebuilding (see source for branches). |
| `image_compression(k, color=False, show=True, save=False)` | **Grayscale:** runs SVD on `self.A` and rebuilds through `reconstructor` / `matrix_to_image`. **Color:** runs SVD **per channel**, keeps the **top `k`** singular values per channel, stacks channels, then calls `matrix_to_image(..., color=True)`. |

---

## Caveats and naming

- **Spelling:** Some names are informal in the source (`Markoff_chainz`, `ceaser`, `vigenre`, etc.); use those exact spellings in imports and calls.
- **`Google` mutates `A`:** After `Google(..., dangling_node=True)`, your original transition matrix columns may have been overwritten for dangling nodes. Work on a **copy** if you need to preserve `A`.
- **Fixed save path:** `matrix_to_image(..., save=True)` always saves as **`file_compressed.jpg`** in the current directory.
- **`show` flags:** Many methods print intermediate results when `show=True` in addition to returning values; set `show=False` for quiet use.
- **Cipher helpers:** `blocker` expects **lowercase** letters; other character sets are not handled.
- **`cipher` methods:** Names are spelled `ceaser` / `vigenre` in code. **`hill`** and **`streamer`** are not finished implementations; prefer Caesar, affine, and Vigenère methods for end-to-end demos.
