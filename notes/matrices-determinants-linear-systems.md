# Matrices, Determinants & Linear Systems — Detailed Notes

---

## 1. Matrices — Basics

**Definition.** An *m × n matrix* is a rectangular array of numbers with `m` rows and `n` columns.

$$
A=\begin{pmatrix}a_{11}&a_{12}&\cdots&a_{1n}\\ a_{21}&a_{22}&\cdots&a_{2n}\\ \vdots&\vdots&\ddots&\vdots\\ a_{m1}&a_{m2}&\cdots&a_{mn}\end{pmatrix}
$$

- `a_ij` = entry in row *i*, column *j*.
- **Square matrix**: `m = n`.
- **Row vector**: `1 × n`; **column vector**: `m × 1`.
- **Zero matrix** `0`: all entries 0.
- **Identity matrix** `I_n`: 1s on the main diagonal, 0s elsewhere.
- **Diagonal matrix**: nonzero entries only on the main diagonal.
- **Triangular**: upper (all entries below diagonal are 0) or lower (all entries above diagonal are 0).
- **Symmetric**: `Aᵀ = A`. **Skew-symmetric**: `Aᵀ = −A` (diagonal entries must be 0).

### 1.1 Matrix Operations

| Operation | Condition | Rule |
|---|---|---|
| Addition `A + B` | same size | add entry by entry |
| Scalar multiple `cA` | any | multiply every entry by `c` |
| Product `AB` | `cols(A) = rows(B)` | `(AB)_ij = Σ_k a_ik b_kj` |
| Transpose `Aᵀ` | any | rows become columns: `(Aᵀ)_ij = a_ji` |

**Row-by-column rule (product).** Entry `(i, j)` of `AB` is the dot product of row *i* of `A` with column *j* of `B`.

**Key properties**

- `A + B = B + A` (commutative)
- `A(B + C) = AB + AC` (distributive)
- `(AB)C = A(BC)` (associative)
- `AB ≠ BA` in general — **matrix multiplication is NOT commutative**.
- `AB = 0` does **not** imply `A = 0` or `B = 0`.
- `(AB)ᵀ = BᵀAᵀ` (order reverses)
- `(A + B)ᵀ = Aᵀ + Bᵀ`, `(cA)ᵀ = cAᵀ`

**Example.**

$$
\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix}=\begin{pmatrix}2&1\\4&3\end{pmatrix}
$$

Check: entry (1,1) = 1·0 + 2·1 = 2; entry (1,2) = 1·1 + 2·0 = 1.

---

## 2. Inverse of a Matrix

**Definition.** A square matrix `A` is *invertible* (non-singular) if there exists `A⁻¹` with

$$
AA^{-1}=A^{-1}A=I.
$$

**2×2 formula.** For `A = [[a, b], [c, d]]`:

$$
A^{-1}=\frac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix},\qquad \text{valid iff } ad-bc\neq 0.
$$

**Properties**

- `(A⁻¹)⁻¹ = A`
- `(AB)⁻¹ = B⁻¹A⁻¹` (order reverses!)
- `(Aᵀ)⁻¹ = (A⁻¹)ᵀ`
- Inverse is unique when it exists.

**Invertibility checklist (equivalent statements for an n×n matrix A):**
1. `A` is invertible.
2. `det(A) ≠ 0`.
3. `Ax = 0` has only the trivial solution.
4. `Ax = b` has a unique solution for every `b`.
5. `rank(A) = n`.
6. `A` is row-equivalent to `I_n`.
7. Columns (and rows) of `A` are linearly independent.
8. `0` is not an eigenvalue of `A`.

---

## 3. Determinants

The **determinant** is a scalar associated with a square matrix. It measures how the linear map scales **area/volume** and tells whether the matrix is invertible.

### 3.1 Notation & small cases

$$
\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc
$$

$$
\det\begin{pmatrix}a_{11}&a_{12}&a_{13}\\a_{21}&a_{22}&a_{23}\\a_{31}&a_{32}&a_{33}\end{pmatrix}
$$

**Sarrus' rule (3×3 only):** add the products of the three down-right diagonals, subtract the products of the three down-left diagonals.

### 3.2 Cofactor expansion (Laplace expansion)

- **Minor** `M_ij`: determinant of the matrix after deleting row *i* and column *j*.
- **Cofactor** `C_ij = (−1)^(i+j) M_ij`.
- **Expansion along row i:** `det(A) = Σ_j a_ij C_ij`.
- Can expand along *any* row or column. **Tip:** pick the row/column with the most zeros.

**Example.**

$$
\det\begin{pmatrix}2&0&1\\3&1&0\\1&2&4\end{pmatrix}
$$

Expand along row 1:

= 2·det[[1,0],[2,4]] − 0·(…) + 1·det[[3,1],[1,2]]
= 2(4 − 0) + 1(6 − 1)
= 8 + 5 = **13**

### 3.3 Properties (very important for exams)

| Property | Effect |
|---|---|
| Swap two rows (or columns) | det changes **sign** |
| Multiply a row by `c` | det is multiplied by `c` |
| Add a multiple of one row to another | det **unchanged** |
| Two equal rows (or columns) | det = 0 |
| A zero row (or column) | det = 0 |
| Row/column proportional | det = 0 |
| `det(Aᵀ) = det(A)` | |
| `det(AB) = det(A)·det(B)` | |
| `det(cA) = cⁿ det(A)` for n×n `A` | (common trap: not `c·det A`) |
| `det(A⁻¹) = 1 / det(A)` | |
| Triangular / diagonal matrix | det = product of diagonal entries |
| `det(A) = 0` | A is **singular** |

**Strategy:** use row operations (only "add multiple of a row" and careful sign tracking for swaps) to reach triangular form, then multiply the diagonal.

### 3.4 Cramer's Rule (for a unique solution)

For `Ax = b` with `det(A) ≠ 0`:

$$
x_i=\frac{\det(A_i)}{\det(A)}
$$

where `A_i` is `A` with column *i* replaced by `b`. Good for small systems; too slow for large ones.

### 3.5 Adjugate formula for the inverse

$$
A^{-1}=\frac{1}{\det(A)}\,\operatorname{adj}(A),\qquad \operatorname{adj}(A)=C^{T}
$$

where `C` is the matrix of cofactors.

---

## 4. Linear Systems

A **linear system** of `m` equations in `n` unknowns:

$$
\begin{cases}a_{11}x_1+\cdots+a_{1n}x_n=b_1\\ \vdots\\ a_{m1}x_1+\cdots+a_{mn}x_n=b_m\end{cases}\quad\Longleftrightarrow\quad Ax=b
$$

- **Coefficient matrix** `A` (m×n).
- **Augmented matrix** `[A | b]`.

### 4.1 Classification of solutions

| Case | Condition | Solutions |
|---|---|---|
| Unique | `rank A = rank [A|b] = n` | exactly one |
| Infinitely many | `rank A = rank [A|b] < n` | free variables → parametric family |
| Inconsistent | `rank A < rank [A|b]` | **no solution** |

- **Homogeneous** system `Ax = 0` always has the trivial solution `x = 0`. It has a nontrivial solution iff `det(A) = 0` (square case) or `rank A < n`.
- **General solution** = particular solution + general solution of `Ax = 0`.

### 4.2 Gaussian elimination

**Elementary row operations**

1. Swap two rows.
2. Multiply a row by a nonzero scalar.
3. Add a multiple of one row to another.

These do **not** change the solution set.

**Algorithm**

1. Write the augmented matrix `[A | b]`.
2. Forward elimination: create zeros below each pivot → **row echelon form (REF)**.
3. Back substitution: solve from the last equation upward.
4. (Optional) Continue to **reduced row echelon form (RREF)** — leading 1s, zeros above and below each leading 1 — by Gauss–Jordan elimination.

**Pivot / leading entry**: first nonzero entry in a row. Pivot columns ↔ basic variables; non-pivot columns ↔ free variables.

**Rank** = number of pivots in REF.

### 4.3 Worked example

Solve

$$
\begin{cases}x+2y-z=3\\ 2x+5y+z=10\\ -x+y+2z=0\end{cases}
$$

Augmented matrix:

$$
\left[\begin{array}{ccc|c}1&2&-1&3\\2&5&1&10\\-1&1&2&0\end{array}\right]
$$

- R2 ← R2 − 2R1: `[0 1 3 | 4]`
- R3 ← R3 + R1: `[0 3 1 | 3]`
- R3 ← R3 − 3R2: `[0 0 −8 | −9]`

So `z = 9/8`. Then `y = 4 − 3z = 4 − 27/8 = 5/8`. Then `x = 3 − 2y + z = 3 − 5/4 + 9/8 = 25/8`.

**Solution:** `(x, y, z) = (25/8, 5/8, 9/8)`, unique.

### 4.4 LU decomposition (quick idea)

If `A = LU` (L lower triangular with 1s on diagonal, U upper triangular), then solve `Ly = b` (forward substitution), then `Ux = y` (back substitution). Efficient when solving many systems with the same `A`.

---

## 5. Rank, Linear Independence & Span

- **Linear independence:** `c₁v₁ + … + cₖvₖ = 0` only when all `cᵢ = 0`.
- **Rank** = maximum number of linearly independent rows = maximum number of linearly independent columns = number of pivots.
- **Rank–nullity theorem:** for an `m × n` matrix `A`,

$$
\operatorname{rank}(A)+\dim\operatorname{Null}(A)=n.
$$

- **Column space** = span of columns; **null space** = `{x : Ax = 0}`.

---

## 6. Special Cases & Common Mistakes

| Mistake | Correct idea |
|---|---|
| `AB = BA` | Not true in general |
| `(AB)⁻¹ = A⁻¹B⁻¹` | Correct: `B⁻¹A⁻¹` |
| `det(A+B) = det A + det B` | False |
| Row operation "multiply row by c" changes det by `c` only once | Yes — but "add row" does NOT change det |
| Swapping rows forgets the minus sign | Each swap flips the sign |
| `det(cA) = c·det A` | Actually `cⁿ·det A` |
| Dividing by a zero pivot | Swap rows first (partial pivoting) |
| Assuming a system always has a unique solution | Check rank / determinant |
| Forgetting that a consistent system with `rank < n` has free variables | Write the parametric solution |

---

## 7. Quick Reference Summary

- **Matrix multiplication:** row × column; not commutative.
- **Inverse (2×2):** swap diagonal, negate off-diagonal, divide by `ad − bc`.
- **Determinant:** `det ≠ 0` ⇔ invertible ⇔ unique solution of `Ax = b`.
- **Row ops:** swap → sign flips; scale row by c → det × c; add multiple → det unchanged.
- **Cramer's rule:** `xᵢ = det(Aᵢ)/det(A)`.
- **Gaussian elimination:** REF then back-substitute; RREF via Gauss–Jordan.
- **Solution types:** unique / infinite / none, decided by `rank A` vs `rank [A|b]` vs `n`.

---

## 8. Practice Checklist

- [ ] Compute a 3×3 determinant by cofactor expansion and by row reduction; compare.
- [ ] Find the inverse of a 3×3 matrix using `adj(A)/det(A)` and by Gauss–Jordan.
- [ ] Solve a 3×3 system by Gaussian elimination, Cramer's rule, and (if available) matrix inverse.
- [ ] Identify the case (unique / infinite / none) for a system with a parameter `k`, e.g. find the values of `k` where `det(A) = 0`.
- [ ] Verify `det(AB) = det(A)det(B)` on two 2×2 matrices.
