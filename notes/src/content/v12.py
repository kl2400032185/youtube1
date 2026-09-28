from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=12,
    slug="leaders-in-array",
    title="Leaders in an Array",
    meta="Striver A2Z · Arrays Playlist #12 · 11:53 · youtube.com/watch?v=cHrH9CQ8pmY",
    tag="ARRAYS · PART 12",
    topic="right-to-left scan with a running maximum",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("An element is a **leader** if it is greater than everything to its RIGHT. The rightmost element "
        "is always a leader. Example `{4,7,1,0}`: 4 is beaten by 7 (not a leader), but 7, 1 and 0 are "
        "leaders -> answer `{7,1,0}`.")
    P.arr([4, 7, 1, 0], marks={1: RED, 2: RED, 3: RED}, captions={1: "leader", 2: "leader", 3: "leader"},
          label="{4,7,1,0}")

    P.h2("1 · Brute — for each, scan its right side", color=RED)
    P.bullets(["For every element walk everything right of it -> `O(n^2)` time, O(1) space."])

    P.h2("2 · Optimal — walk from the RIGHT with a max", color=GREEN)
    P.p("Leadership is about the **suffix maximum**. Walk right-to-left carrying `maxi`; anything bigger "
        "than `maxi` is a leader and becomes the new `maxi`.")
    P.code("cpp", """
int maxi = INT_MIN;
vector<int> leaders;
for (int i = n - 1; i >= 0; i--) {
    if (arr[i] > maxi) { leaders.push_back(arr[i]); maxi = arr[i]; }
}
reverse(leaders.begin(), leaders.end());   // if output must be left->right
""", caption="O(n) time · O(1) extra (answer aside)")
    P.dryrun("Dry run on {10,22,12,3,0,6} right to left",
             ["i", "arr[i]", "maxi", "leader?"],
             [["5", "6", "-inf", "YES (rightmost)"],
              ["4", "0", "6", "no"],
              ["3", "3", "6", "no"],
              ["2", "12", "6", "YES"],
              ["1", "22", "12", "YES"],
              ["0", "10", "22", "no"]],
             "Collected right-to-left {6,12,22}; reversed for left-to-right answer {22,12,6}.")
    P.callout("note", "direction decides everything",
              "Left-to-right you would need to know the future. Right-to-left, the future IS the past — "
              "that inversion is the algorithm.")
    P.chips(["brute O(n^2)", "optimal O(n)"])
    P.divider()
    P.h2("Cheat sheet — video 12", color=PURPLE)
    P.table(["Approach", "Idea", "TC/SC"],
            [["Nested scan", "check whole right side", "O(n^2)/O(1)"],
             ["Suffix max", "right-to-left, update maxi", "O(n)/O(1)"]],
            fracs=[0.3, 0.44, 0.26])
