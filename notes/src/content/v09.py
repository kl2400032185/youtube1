from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=9,
    slug="rearrange-by-sign",
    title="Rearrange Array Elements by Sign (both varieties)",
    meta="Striver A2Z · Arrays Playlist #9 · 21:37 · youtube.com/watch?v=h4aBagy4Uok",
    tag="ARRAYS · PART 9",
    topic="interleave positives and negatives keeping relative order",
)


def build(P):
    P.h2("Variety 1 — equal count, start positive, keep order", color=RED)
    P.p("Equal number of + and -. Output must alternate `+, -, +, - ...` starting with positive, "
        "keeping the **relative order** of positives and of negatives. "
        "`{1,2,-4,-5}` -> `{1,-4,2,-5}`.")
    P.h3("Optimal — two write pointers into an answer array")
    P.bullets([
        "Positives go to even indices `0,2,4..`, negatives to odd indices `1,3,5..`.",
        "Scan once; `pos` starts at 0, `neg` starts at 1; both jump by 2. Relative order is automatic.",
        "True O(1) space is impossible: order constraints mean you cannot decide placements in place.",
    ])
    P.code("cpp", """
vector<int> ans(n);
int pos = 0, neg = 1;
for (int x : arr) {
    if (x >= 0) { ans[pos] = x; pos += 2; }
    else        { ans[neg] = x; neg += 2; }
}
""", caption="O(n) time · O(n) space (the answer array)")
    P.arr([1, 2, -4, -5], marks={0: GREEN, 2: RED, 1: GREEN, 3: RED},
          captions={0: "pos idx 0", 1: "neg idx 1"}, label="writing pattern")

    P.h2("Variety 2 — UNEQUAL counts", color=RED)
    P.p("Example `{1,2,-4,-5,3,4}` (four +, two -). Alternate while both kinds last, "
        "then append the leftover kind **in order** at the tail.")
    P.code("cpp", """
vector<int> p, q;                       // positives, negatives
for (int x : arr) (x >= 0 ? p : q).push_back(x);
vector<int> ans;
int i = 0, j = 0, k = 0;
while (i < p.size() && j < q.size()) {  // alternate
    ans.push_back(k % 2 == 0 ? p[i++] : q[j++]);
    k++;
}
while (i < p.size()) ans.push_back(p[i++]);   // leftovers keep their order
while (j < q.size()) ans.push_back(q[j++]);
""", caption="O(n) time · O(n) space")
    P.dryrun("Dry run on {1,2,-4,-5,3,4}",
             ["step", "ans", "note"],
             [["alt", "1,-4,2,-5", "take from p,q in turn"],
              ["leftover", "1,-4,2,-5,3,4", "the extra positives simply continue"]],
             "The leftover part does NOT alternate any more — and that is exactly what is asked.")
    P.callout("note", "why not in-place O(1)?",
              "Keeping relative order for both groups while interleaving needs rotations for every "
              "placement — you end up O(n^2). The interviewer accepts O(n) space; defend it calmly.")
    P.chips(["both varieties O(n) time", "O(n) space", "order preserved"])
    P.divider()
    P.h2("Cheat sheet — video 9", color=PURPLE)
    P.table(["Variety", "Idea", "Pointers"],
            [["Equal counts", "pos->even idx, neg->odd idx", "0 and 1, step 2"],
             ["Unequal counts", "alternate then flush leftovers", "two lists + merge tail"]],
            fracs=[0.28, 0.44, 0.28])
