from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=23,
    slug="merge-overlapping-intervals",
    title="Merge Overlapping Intervals",
    meta="Striver A2Z · Arrays Playlist #23 · 22:35 · youtube.com/watch?v=IexN60k62jo",
    tag="ARRAYS · PART 23",
    topic="sort by start, fold with a running end",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Merge all intervals that overlap/touch. `{{1,3},{2,6},{8,10},{15,18}}` -> "
        "`{{1,6},{8,10},{15,18}}`.")

    P.h2("1 · Brute — compare every pair", color=RED)
    P.bullets([
        "For each interval, scan all others and merge overlapping ones, marking visited -> `O(n^2 log n)` "
        "with sorting inside. Mention, then move on.",
    ])

    P.h2("2 · Optimal — sort by START, fold greedily", color=GREEN)
    P.p("After sorting by start, the answer's intervals are also sorted, and a new interval either "
        "extends the current merged one (`start <= current_end`) or starts a fresh one.")
    P.code("cpp", """
sort(iv.begin(), iv.end());
vector<vector<int>> ans;
for (auto &it : iv) {
    if (ans.empty() || it[0] > ans.back()[1])
        ans.push_back(it);                                   // no overlap -> new block
    else
        ans.back()[1] = max(ans.back()[1], it[1]);           // swallow it
}
""", caption="O(n log n) sort + O(n) scan · O(1) extra besides answer")
    P.callout("gotcha", "why max() on the end",
              "`{[1,10],[2,3]}`: the inner interval adds nothing — blindly taking `it[1]` would SHRINK the "
              "end to 3. Always `max(current_end, it[1])`.")
    P.dryrun("On {{1,3},{2,6},{8,10},{15,18}}",
             ["interval", "vs current [?,?]", "ans"],
             [["[1,3]", "start new", "[[1,3]]"],
              ["[2,6]", "2 <= 3 -> merge, end=max(3,6)", "[[1,6]]"],
              ["[8,10]", "8 > 6 -> new", "[[1,6],[8,10]]"],
              ["[15,18]", "15 > 10 -> new", "[[1,6],[8,10],[15,18]]"]],
             "Touching counts as overlapping too: [1,3],[3,6] merge (3 <= 3).")
    P.flow(["[1,3]", "[2,6] merges -> [1,6]", "[8,10] new", "[15,18] new"])
    P.callout("interview", "in-place vs output list",
              "The output-list version above is the clean one. In-place uses the same logic writing into the "
              "front of the array with an index pointer; both O(n log n).")
    P.chips(["O(n log n) time", "O(n) answer space"])
    P.divider()
    P.h2("Cheat sheet — video 23", color=PURPLE)
    P.table(["Case", "Condition", "Action"],
            [["first / gap", "ans empty or it[0] > back end", "push it"],
             ["overlap", "it[0] <= back end", "back end = max(back end, it[1])"]],
            fracs=[0.24, 0.4, 0.36])
