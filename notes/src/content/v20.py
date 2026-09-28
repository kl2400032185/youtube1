from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=20,
    slug="three-sum",
    title="3 Sum — triplets with zero sum (no duplicates)",
    meta="Striver A2Z · Arrays Playlist #20 · 38:25 · youtube.com/watch?v=DhFh8Kw7ymk",
    tag="ARRAYS · PART 20",
    topic="sort + fix one + two pointers, skipping duplicates",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Find all UNIQUE triplets with sum 0. `{-1,0,1,2,-1,-4}` -> `{-1,-1,2}, {-1,0,1}`. "
        "No duplicate triplets in the answer — that is the real difficulty.")

    P.h2("1 · Brute — three loops + a set", color=RED)
    P.bullets([
        "Triple loop, insert sorted triplets into a `set` to de-duplicate. `O(n^3 log n)` with set overhead.",
        "Better: two loops + hashmap for the third value (like 2-sum) -> `O(n^2)` time, O(n) space, "
        "plus sorting each triplet for the de-dup set.",
    ])

    P.h2("2 · Optimal — sort, FIX a, two pointers on the rest", color=GREEN)
    P.numbered([
        "Sort the array. Loop `i` over candidates for the FIRST element.",
        "Skip duplicates: `if (i > 0 && a[i] == a[i-1]) continue;`",
        "Two pointers `j = i+1, k = n-1`; target for the pair = `-a[i]`.",
        "Sum too small -> `j++`; too big -> `k--`; equal -> record, then move BOTH past duplicates.",
    ])
    P.code("cpp", """
sort(a.begin(), a.end());
for (int i = 0; i < n - 2; i++) {
    if (i > 0 && a[i] == a[i - 1]) continue;          // same first element as before
    int j = i + 1, k = n - 1;
    while (j < k) {
        int s = a[i] + a[j] + a[k];
        if (s < 0)      j++;
        else if (s > 0) k--;
        else {
            ans.push_back({a[i], a[j], a[k]});
            j++; k--;
            while (j < k && a[j] == a[j - 1]) j++;    // skip dup second
            while (j < k && a[k] == a[k + 1]) k--;    // skip dup third
        }
    }
}
""", caption="O(n^2) total · O(1) extra (sort space aside)")
    P.dryrun("On sorted {-4,-1,-1,0,1,2}",
             ["i", "fixed a[i]", "j,k walk", "triplets found"],
             [["0", "-4", "needs pair sum 4 -> (2,?) none", "-"],
              ["1", "-1", "(-1,2) then (0,1)", "{-1,-1,2}, {-1,0,1}"],
              ["2", "-1", "SKIPPED (a[2]==a[1])", "-"],
              ["3", "0", "needs 0 from two of {1,2} -> none", "-"]],
             "The i-skip is what prevents the duplicate {-1,0,1}.")
    P.arr([-4, -1, -1, 0, 1, 2], marks={1: RED, 2: GRAY, 4: GREEN, 5: GREEN},
          captions={1: "i used", 2: "i skipped", 4: "j..k window"}, label="sorted arr")
    P.callout("gotcha", "skip AFTER recording, not before",
              "The `while a[j]==a[j-1]` skips run AFTER pushing a valid triplet and advancing. Pre-skipping "
              "at window start would delete legitimate repeated values like the two -1s in {-1,-1,2}.")
    P.callout("trick", "two-pointer vs hashmap here",
              "Hashing struggles with 'no duplicate triplets' (needs a set of sorted triplets anyway) — "
              "sorting + pointers de-duplicates for free and uses O(1) extra. Prefer it for k-sum >= 3.")
    P.chips(["brute O(n^3)", "hash better O(n^2)", "sort+2ptr O(n^2)"])
    P.divider()
    P.h2("Cheat sheet — video 20", color=PURPLE)
    P.table(["Layer", "Pointer", "De-dup rule"],
            [["first element", "loop i", "skip if a[i]==a[i-1] and i>0"],
             ["second/third", "j, k from ends", "after a hit, walk j,k past equals"],
             ["window move", "sum vs 0", "sorted -> small: j++, big: k--"]],
            fracs=[0.26, 0.3, 0.44])
