from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=18,
    slug="pascals-triangle",
    title="Pascal's Triangle — three varieties incl. nCr in O(r)",
    meta="Striver A2Z · Arrays Playlist #18 · 26:45 · youtube.com/watch?v=bR7mQgwQ_o8",
    tag="ARRAYS · PART 18",
    topic="pascal triangle: element, row, whole triangle",
)


def build(P):
    P.h2("The triangle and its law", color=TEAL)
    P.bullets([
        "Row r (1-indexed), position c: value = `C(r-1, c-1)`.  Each inner cell = sum of the two above.",
        "Row r has r elements; first and last are always 1.",
    ])
    P.flow(["1", "1 1", "1 2 1", "1 3 3 1", "..."])

    P.h2("Variety 1 — one element, i.e. nCr, in O(r)", color=RED)
    P.p("Multiplicative formula, computed left to right so nothing overflows early: "
        "`C(n,r) = n*(n-1)*...*(n-r+1) / r!` — but divide at EVERY step to keep numbers small.")
    P.code("cpp", """
long long nCr(int n, int r) {
    long long res = 1;
    for (int i = 1; i <= r; i++) {
        res = res * (n - r + i) / i;     // divisible at every step - guaranteed
    }
    return res;
}
""", caption="O(r) time · O(1) space · no factorial arrays")
    P.dryrun("C(5,3) step by step",
             ["i", "multiply by", "divide by", "res"],
             [["1", "3", "1", "3"],
              ["2", "4", "2", "6"],
              ["3", "5", "3", "10"]],
             "res stays an integer at every step — the division is always exact.")

    P.h2("Variety 2 — print row r in O(r)", color=ORANGE)
    P.p("Row elements are running products: after the leading 1, "
        "`next = prev * (r-1-i) / (i+1)`. This is variety 1 unrolled into one row.")
    P.code("cpp", """
vector<long long> row(int r) {
    vector<long long> ans = {1};
    long long cur = 1;
    for (int i = 1; i < r; i++) {
        cur = cur * (r - i) / i;
        ans.push_back(cur);
    }
    return ans;
}
""", caption="row 5 -> {1,4,6,4,1}")

    P.h2("Variety 3 — print n rows (the triangle)", color=GREEN)
    P.bullets(["Each row = previous row with neighbours summed, 1s glued to both ends. `O(n^2)` total."])
    P.code("cpp", """
vector<vector<int>> tri;
for (int r = 0; r < n; r++) {
    vector<int> row(r + 1, 1);
    for (int c = 1; c < r; c++)
        row[c] = tri[r - 1][c - 1] + tri[r - 1][c];
    tri.push_back(row);
}
""", caption="O(n^2) time · O(n^2) output space")
    P.flow(["row r built from row r-1", "row[c] = up-left + up-right", "ends stay 1"])
    P.callout("trick", "why divide-while-multiplying is exact",
              "The product of any k consecutive integers is divisible by k! — so after i steps you hold "
              "C(n-r+i, i) exactly. Integer arithmetic, zero floating point.")
    P.callout("interview", "complexity cheats",
              "Element: O(r). Row: O(r). Triangle: O(n^2). Space for element/row: O(1) besides the answer.")
    P.chips(["nCr O(r)", "row O(r)", "triangle O(n^2)"])
    P.divider()
    P.h2("Cheat sheet — video 18", color=PURPLE)
    P.table(["Variety", "Input", "Tool", "TC"],
            [["single element", "(row, col)", "multiplicative nCr", "O(col)"],
             ["one row", "r", "running product", "O(r)"],
             ["whole triangle", "n", "sum of two above", "O(n^2)"]],
            fracs=[0.26, 0.2, 0.32, 0.22])
