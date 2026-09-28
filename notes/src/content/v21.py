from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=21,
    slug="four-sum",
    title="4 Sum — quadruplets adding to target",
    meta="Striver A2Z · Arrays Playlist #21 · 28:47 · youtube.com/watch?v=eD95WRfh81c",
    tag="ARRAYS · PART 21",
    topic="two fixed loops + two pointers (k-sum pattern)",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("All UNIQUE quadruplets summing to `target` (target is any integer, not just 0!). "
        "`{1,0,-1,0,-2,2}, target 0` -> `{-2,-1,1,2}, {-2,0,0,2}, {-1,0,0,1}`.")

    P.h2("1 · Brute / Better", color=RED)
    P.bullets([
        "Brute: 4 loops + set of sorted quadruplets — `O(n^4)`. Only to state and dismiss.",
        "Better: 3 loops + hashmap for the last value, de-dup via set — `O(n^3)`.",
    ])

    P.h2("2 · Optimal — sort + FIX two + two pointers", color=GREEN)
    P.p("Exactly 3-sum with one more outer loop. The pattern generalises: for k-sum, fix k-2 values "
        "with nested loops and close with two pointers.")
    P.code("cpp", """
sort(a.begin(), a.end());
for (int i = 0; i < n - 3; i++) {
    if (i > 0 && a[i] == a[i - 1]) continue;
    for (int j = i + 1; j < n - 2; j++) {
        if (j > i + 1 && a[j] == a[j - 1]) continue;     // note j > i+1
        int l = j + 1, r = n - 1;
        while (l < r) {
            long long s = (long long)a[i] + a[j] + a[l] + a[r];
            if (s < target)      l++;
            else if (s > target) r--;
            else {
                ans.push_back({a[i], a[j], a[l], a[r]});
                l++; r--;
                while (l < r && a[l] == a[l - 1]) l++;
                while (l < r && a[r] == a[r + 1]) r--;
            }
        }
    }
}
""", caption="O(n^3) · use long long — four ints CAN overflow")
    P.callout("gotcha", "three classic bugs",
              "1) `j` de-dup must be `j > i + 1` (the first j after i is always allowed). "
              "2) sum in `long long` — target up to 1e9, four values overflow int. "
              "3) skip duplicates AFTER recording, same rule as 3-sum.")
    P.dryrun("On sorted {-2,-1,0,0,1,2}, target 0",
             ["i", "j", "pair needed", "found"],
             [["0 (-2)", "1 (-1)", "3", "{1,2}"],
              ["0 (-2)", "2 (0)", "2", "{0,2}"],
              ["0 (-2)", "3 (0)", "skip (dup j)", "-"],
              ["1 (-1)", "2 (0)", "1", "{0,1}"]],
             "Three unique quadruplets, exactly the expected output.")
    P.arr([-2, -1, 0, 0, 1, 2], marks={0: RED, 1: ORANGE, 2: GREEN, 5: TEAL},
          captions={0: "i", 1: "j", 2: "l", 5: "r"}, label="sorted, one snapshot")
    P.callout("trick", "k-sum template",
              "sort; loop depth k-2; each loop skips its own duplicate (first iteration allowed); innermost "
              "is two pointers. 3-sum = depth 1, 4-sum = depth 2. You now own the whole family.")
    P.chips(["brute O(n^4)", "hash O(n^3)", "sort+2ptr O(n^3)"])
    P.divider()
    P.h2("Cheat sheet — video 21", color=PURPLE)
    P.table(["Approach", "Idea", "TC"],
            [["4 loops + set", "enumerate everything", "O(n^4 log n)"],
             ["3 loops + map", "2-sum lookup inside", "O(n^3)"],
             ["2 loops + 2 pointers", "the k-sum template", "O(n^3) but tiny constant, O(1) extra"]],
            fracs=[0.28, 0.32, 0.4])
