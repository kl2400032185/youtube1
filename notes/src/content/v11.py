from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=11,
    slug="next-permutation",
    title="Next Permutation (lexicographically next arrangement)",
    meta="Striver A2Z · Arrays Playlist #11 · 28:15 · youtube.com/watch?v=JDOXKqF60RQ",
    tag="ARRAYS · PART 11",
    topic="in-place next permutation in O(n)",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Rearrange the array into the **next greater permutation** in dictionary order; if it is already "
        "the largest, wrap to the smallest (sorted ascending). Must be **in place**. "
        "`{1,3,2}` -> `{2,1,3}`; `{3,2,1}` -> `{1,2,3}`.")

    P.h2("1 · Brute — generate & find", color=RED)
    P.bullets([
        "Generate all n! permutations sorted and take the next one. Absurd, but it defines the goal.",
        "C++ has `next_permutation(begin, end)` — in an interview you must re-derive what it does.",
    ])

    P.h2("2 · Optimal — the 3-step observation", color=GREEN)
    P.p("Look at the tail. From the right, the array is non-increasing until some position `i` — the "
        "**break point** where `a[i] < a[i+1]`. Everything right of `i` is already the maximum it can be, "
        "so the next permutation must change position `i`.")
    P.numbered([
        "Find the largest `i` with `a[i] < a[i+1]` (scan from the right). If none -> reverse whole array.",
        "In the right part, find the **smallest element greater than a[i]** (scan from right, first one > a[i]) and swap.",
        "Reverse the suffix `i+1 .. n-1` to make it the smallest possible tail.",
    ])
    P.code("cpp", """
int i = n - 2;
while (i >= 0 && arr[i] >= arr[i + 1]) i--;          // step 1: break point
if (i < 0) { reverse(arr.begin(), arr.end()); return; }
int j = n - 1;
while (arr[j] <= arr[i]) j--;                        // step 2: just-bigger partner
swap(arr[i], arr[j]);
reverse(arr.begin() + i + 1, arr.end());             // step 3: minimal tail
""", caption="O(n) time · O(1) space · 3 scans")
    P.dryrun("Dry run on {2, 1, 5, 4, 3, 0, 0}",
             ["step", "what we see", "array"],
             [["find i", "tail 5,4,3,0,0 falls; a[1]=1 < a[2]=5 -> i=1", "{2,1,5,4,3,0,0}"],
              ["find j", "rightmost value > 1 is 3 at j=4; swap", "{2,3,5,4,1,0,0}"],
              ["reverse tail", "suffix 5,4,1,0,0 -> 0,0,1,4,5", "{2,3,0,0,1,4,5}"]],
             "Answer {2,3,0,0,1,4,5} — the immediate next arrangement.")
    P.arr([2, 1, 5, 4, 3, 0, 0], marks={1: RED, 4: GREEN}, captions={1: "break i", 4: "swap j"},
          label="before")
    P.callout("trick", "why reversing the suffix is correct",
              "After the swap the suffix is still non-increasing (the swap preserved that property), and "
              "the smallest arrangement of those digits is ascending — one reverse gives exactly that.")
    P.callout("gotcha", "edge cases",
              "Fully descending input -> i not found -> reverse to sorted (wrap around). "
              "Duplicates: use `>=` in the first scan and `<=` in the second — strict inequalities avoid "
              "swapping with an equal element.")
    P.chips(["O(n) time", "O(1) space", "3 passes, no sorting"])
    P.divider()
    P.h2("Cheat sheet — video 11", color=PURPLE)
    P.table(["Step", "Scan direction", "Condition", "Purpose"],
            [["1 break point", "right -> left", "a[i] < a[i+1]", "where a change is possible"],
             ["2 partner", "right -> left", "first > a[i]", "smallest possible bump"],
             ["3 reverse tail", "i+1 .. end", "-", "make the tail minimal"]],
            fracs=[0.22, 0.24, 0.26, 0.28])
    P.quote("The suffix is already 'maxed out'; bump the last possible digit, then reset the tail.")
