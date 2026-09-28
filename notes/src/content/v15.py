from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=15,
    slug="rotate-matrix-90",
    title="Rotate Matrix / Image by 90 Degrees (in place)",
    meta="Striver A2Z · Arrays Playlist #15 · 17:47 · youtube.com/watch?v=Z0R2u6gd3GU",
    tag="ARRAYS · PART 15",
    topic="transpose + reverse = 90° rotation",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Rotate an `n x n` matrix 90 degrees **clockwise**, in place. "
        "Rule: `mat[i][j]` must land at `res[j][n-1-i]`.")

    P.h2("1 · Brute — extra matrix with the mapping", color=RED)
    P.code("cpp", """
vector<vector<int>> res(n, vector<int>(n));
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        res[j][n - 1 - i] = mat[i][j];      // top row becomes right column
""", caption="O(n^2) time · O(n^2) space · memorise the index mapping")

    P.h2("2 · Optimal — TRANSPOSE then REVERSE each row", color=GREEN)
    P.p("Clockwise rotation = mirror over the main diagonal (transpose) + flip every row horizontally.")
    P.flow(["transpose: swap mat[i][j] <-> mat[j][i] (i<j)", "reverse each row", "= rotated 90 CW"])
    P.code("cpp", """
for (int i = 0; i < n; i++)                 // transpose (only upper triangle!)
    for (int j = i + 1; j < n; j++)
        swap(mat[i][j], mat[j][i]);
for (int i = 0; i < n; i++)
    reverse(mat[i].begin(), mat[i].end());  // mirror rows
""", caption="O(n^2) time · O(1) space")
    P.matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], label="start")
    P.matrix([[1, 4, 7], [2, 5, 8], [3, 6, 9]], label="after transpose")
    P.matrix([[7, 4, 1], [8, 5, 2], [9, 6, 3]], label="after reversing rows = answer")
    P.callout("trick", "the four variations",
              "**clockwise** = transpose + reverse rows. **anti-clockwise** = transpose + reverse columns. "
              "180 = reverse rows + reverse columns. Know all three, they are free.")
    P.callout("gotcha", "transpose loop bounds",
              "Swap only for `j > i` (upper triangle). A full `j = 0..n` loop swaps everything twice and "
              "silently returns the original matrix — classic bug.")
    P.chips(["brute O(n^2) space", "optimal O(1) space"])
    P.divider()
    P.h2("Cheat sheet — video 15", color=PURPLE)
    P.table(["Rotation", "Recipe", "Space"],
            [["90 CW", "transpose + reverse each row", "O(1)"],
             ["90 CCW", "transpose + reverse each column", "O(1)"],
             ["180", "reverse rows + reverse columns", "O(1)"]],
            fracs=[0.24, 0.5, 0.26])
