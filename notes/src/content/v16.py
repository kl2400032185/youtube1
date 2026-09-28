from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=16,
    slug="spiral-matrix",
    title="Spiral Traversal of a Matrix",
    meta="Striver A2Z · Arrays Playlist #16 · 16:33 · youtube.com/watch?v=3Zv-s9UUrFM",
    tag="ARRAYS · PART 16",
    topic="boundary pointers walking inwards",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Print the matrix layer by layer, clockwise spiral. "
        "`{{1,2,3,4},{5,6,7,8},{9,10,11,12}}` -> `1 2 3 4 8 12 11 10 9 5 6 7`.")

    P.h2("The only idea — four shrinking boundaries", color=GREEN)
    P.bullets([
        "Keep `top, bottom, left, right`. Each side you walk, that boundary shrinks by 1.",
        "Right along `top`, then `top++`.  Down along `right`, then `right--`.",
        "Left along `bottom` **only if top <= bottom**, then `bottom--`.",
        "Up along `left` **only if left <= right**, then `left++`.",
        "Those two guards stop the double-print on thin matrices.",
    ])
    P.code("cpp", """
int top = 0, bottom = n - 1, left = 0, right = m - 1;
while (top <= bottom && left <= right) {
    for (int j = left;  j <= right; j++) ans.push_back(mat[top][j]);
    top++;
    for (int i = top;   i <= bottom; i++) ans.push_back(mat[i][right]);
    right--;
    if (top <= bottom)
        for (int j = right; j >= left; j--) ans.push_back(mat[bottom][j]);
    bottom--;
    if (left <= right)
        for (int i = bottom; i >= top; i--) ans.push_back(mat[i][left]);
    left++;
}
""", caption="O(n*m) time · O(1) extra")
    P.matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
             marks={(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)},
             label="first two walks: top row, then right column")
    P.dryrun("Walk on the 3x4 example",
             ["walk", "prints", "boundary change"],
             [["top row ->", "1 2 3 4", "top = 1"],
              ["right col |", "8 12", "right = 2"],
              ["bottom row <-", "11 10 9", "bottom = 1"],
              ["left col ^", "5", "left = 1"],
              ["top row ->", "6 7", "top = 2 > bottom, stop"]],
             "Order: 1..4, 8, 12, 11..9, 5, 6, 7 — matches the expected output.")
    P.callout("gotcha", "when the guards matter",
              "A single-row matrix `{{1,2,3}}`: after the first walk top>bottom; without the `if`, you would "
              "print the row backwards a second time. Same for a single column with the second guard.")
    P.chips(["O(n*m) exactly once each cell", "O(1) extra space"])
    P.divider()
    P.h2("Cheat sheet — video 16", color=PURPLE)
    P.table(["Side", "Loop", "Afterwards", "Guard for"],
            [["top", "left..right", "top++", "-"],
             ["right", "top..bottom", "right--", "-"],
             ["bottom", "right..left", "bottom--", "top <= bottom"],
             ["left", "bottom..top", "left++", "left <= right"]],
            fracs=[0.16, 0.28, 0.26, 0.3])
