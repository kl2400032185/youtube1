from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=8,
    slug="kadanes-max-subarray-sum",
    title="Kadane's Algorithm — Maximum Subarray Sum (+ print it)",
    meta="Striver A2Z · Arrays Playlist #8 · 20:09 · youtube.com/watch?v=AHZpyENo7k4",
    tag="ARRAYS · PART 8",
    topic="Kadane's algorithm and printing the subarray",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Return the largest possible sum of a **contiguous** subarray. "
        "`{-2,1,-3,4,-1,2,1,-5,4}` -> `6` (the subarray `{4,-1,2,1}`).")

    P.h2("1 · Brute — all subarrays", color=RED)
    P.bullets(["Two loops with a running sum, track the max. `O(n^2)`, O(1) space. Your fallback story."])

    P.h2("2 · Optimal — Kadane's algorithm", color=GREEN)
    P.p("Walk the array carrying a running sum. The one insight: a **negative running sum can never help "
        "the future**, so the moment it goes below 0, drop it and restart the subarray right here.")
    P.code("cpp", """
long long sum = 0, maxi = LLONG_MIN;
for (int i = 0; i < n; i++) {
    sum += arr[i];
    maxi = max(maxi, sum);      // every position is a possible END of the answer
    if (sum < 0) sum = 0;       // a negative prefix is poison -> restart
}
return maxi;
""", caption="O(n) time · O(1) space · works for all-negative too (maxi is updated BEFORE the reset)")
    P.callout("gotcha", "all-negative arrays",
              "`{-3,-1,-2}` must return `-1`, not 0. The update-then-reset order above handles it; "
              "if your version resets first, seed `maxi` with `arr[0]` instead of `LLONG_MIN` and double-check.")

    P.h2("3 · Printing the subarray (not just the sum)", color=GREEN)
    P.bullets([
        "Remember `start` = the index where the current run began. When `sum` hits 0 (restart), "
        "set `start = i + 1`.",
        "Whenever `sum` beats the global `maxi`, save `ansStart = start, ansEnd = i`.",
    ])
    P.code("cpp", """
int start = 0, ansStart = -1, ansEnd = -1;
long long sum = 0, maxi = LLONG_MIN;
for (int i = 0; i < n; i++) {
    if (sum == 0) start = i;            // a new run begins here
    sum += arr[i];
    if (sum > maxi) { maxi = sum; ansStart = start; ansEnd = i; }
    if (sum < 0) sum = 0;
}
// answer subarray = arr[ansStart .. ansEnd]
""", caption="same O(n); now you can PRINT it")
    P.dryrun("Dry run on {-2,1,-3,4,-1,2,1,-5,4}",
             ["i", "arr[i]", "sum", "maxi", "window"],
             [["0", "-2", "0(reset)", "-2", "[]"],
              ["1", "1", "1", "1", "[1]"],
              ["2", "-3", "0(reset)", "1", "[]"],
              ["3", "4", "4", "4", "[4]"],
              ["4", "-1", "3", "4", "[4,-1]"],
              ["5", "2", "5", "5", "[4,-1,2]"],
              ["6", "1", "6", "6", "[4,-1,2,1]"],
              ["7", "-5", "1", "6", "..."],
              ["8", "4", "5", "6", "answer stays [4,-1,2,1] = 6"]],
             "maxi is only overwritten when strictly beaten — rows 3..6 build the winner.")
    P.arr([-2, 1, -3, 4, -1, 2, 1, -5, 4], marks={3: GREEN, 6: GREEN},
          captions={3: "ansStart", 6: "ansEnd"}, label="arr[]")
    P.callout("trick", "the mental model",
              "Think of `sum` as a streak. You keep extending the streak while it is helping; "
              "the instant it turns toxic (<0) you cut it. `maxi` photographs the best streak ever seen.")
    P.chips(["brute O(n^2)", "Kadane O(n)/O(1)", "print = track start/end"])
    P.divider()
    P.h2("Cheat sheet — video 8", color=PURPLE)
    P.table(["Task", "Method", "TC/SC"],
            [["Max sum", "Kadane (update max, then reset if <0)", "O(n)/O(1)"],
             ["Max sum + the subarray itself", "Kadane + start/ansStart/ansEnd bookkeeping", "O(n)/O(1)"],
             ["All-negative input", "same code — update maxi BEFORE resetting", "O(n)/O(1)"]],
            fracs=[0.32, 0.46, 0.22])
    P.quote("A negative prefix helps nothing. Drop it and start over — that one line IS Kadane's algorithm.")
