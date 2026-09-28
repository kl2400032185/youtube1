from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=14,
    slug="set-matrix-zeroes",
    title="Set Matrix Zeroes (down to O(1) space)",
    meta="Striver A2Z · Arrays Playlist #14 · 30:07 · youtube.com/watch?v=N0MgLvceX7M",
    tag="ARRAYS · PART 14",
    topic="zeroing rows/columns with marker tricks",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("If `mat[i][j] == 0`, set its whole row i and column j to 0 — **in place**.")
    P.matrix([[1, 1, 1], [1, 0, 1], [1, 1, 1]], marks={(1, 1)}, label="3x3 example")
    P.matrix([[1, 0, 1], [0, 0, 0], [1, 0, 1]], label="result")

    P.h2("1 · Brute — mark with a sentinel", color=RED)
    P.bullets([
        "For each 0, walk its row and column setting non-zero cells to `-1` (sentinel); "
        "second pass turns every `-1` into 0. `O((n*m)*(n+m))` time, O(1) space.",
    ])

    P.h2("2 · Better — two marker arrays", color=ORANGE)
    P.bullets([
        "`row[n]` and `col[m]` flags; pass 1 marks them, pass 2 zeroes marked rows/cols.",
        "`O(n*m)` time, `O(n+m)` space.",
    ])
    P.code("cpp", """
vector<int> row(n, 0), col(m, 0);
for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
        if (mat[i][j] == 0) { row[i] = 1; col[j] = 1; }
for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
        if (row[i] || col[j]) mat[i][j] = 0;
""", caption="the 'obvious good' solution")

    P.h2("3 · Optimal — use row 0 and col 0 AS the marker arrays", color=GREEN)
    P.p("The first row can store `col[]` and the first column can store `row[]` — but they share cell "
        "`mat[0][0]`, so keep one separate flag `col0` for column 0.")
    P.numbered([
        "Pass 1: for `mat[i][j]==0` -> `mat[i][0] = 0` and `mat[0][j] = 0` (if j==0, set `col0 = 0`).",
        "Pass 2 (i from 1, j from 1): if `mat[i][0]==0 || mat[0][j]==0` -> `mat[i][j]=0`.",
        "Finally fix row 0 (if `mat[0][0]==0`) and column 0 (if `col0==0`).",
    ])
    P.code("cpp", """
int col0 = 1;
for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
        if (mat[i][j] == 0) {
            mat[i][0] = 0;
            if (j) mat[0][j] = 0; else col0 = 0;
        }
for (int i = 1; i < n; i++)
    for (int j = 1; j < m; j++)
        if (mat[i][0] == 0 || mat[0][j] == 0) mat[i][j] = 0;
if (mat[0][0] == 0) for (int j = 0; j < m; j++) mat[0][j] = 0;
if (col0 == 0)      for (int i = 0; i < n; i++) mat[i][0] = 0;
""", caption="O(n*m) time · O(1) space")
    P.matrix([[1, 0, 0, 1], [0, 1, 1, 0], [1, 1, 1, 1]], marks={(0, 1), (1, 0)},
             label="markers live in row 0 / col 0")
    P.callout("gotcha", "why the last two steps come LAST and in THIS order",
              "If you zero row 0 too early, its marker information (`mat[0][j]`) is destroyed before pass 2 "
              "reads it. Handle the interior first, then row 0, then column 0.")
    P.callout("note", "sentinel -1 needs a guard",
              "The brute trick only works when you know original values are never negative... if they can "
              "be, you cannot use -1 as 'will become zero'. Markers (arrays or row0/col0) never have this bug.")
    P.chips(["brute O((nm)(n+m))", "better O(nm)/O(n+m)", "optimal O(nm)/O(1)"])
    P.divider()
    P.h2("Cheat sheet — video 14", color=PURPLE)
    P.table(["Approach", "Storage for markers", "TC / SC"],
            [["Sentinel -1", "the matrix itself", "O(nm(n+m))/O(1)"],
             ["Marker arrays", "row[] + col[]", "O(nm)/O(n+m)"],
             ["row0/col0 + col0 flag", "the matrix's own borders", "O(nm)/O(1)"]],
            fracs=[0.3, 0.42, 0.28])
